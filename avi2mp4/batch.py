from dataclasses import dataclass, field
from pathlib import Path
import shutil
import time

from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from .converter import convert_file


@dataclass
class BatchResult:
    total: int = 0
    success: int = 0
    failed: int = 0
    skipped: int = 0
    would_convert: int = 0
    errors: list[tuple[str, str]] = field(default_factory=list)
    duration: float = 0.0


def scan_avi_files(input_dir: Path) -> list[Path]:
    return sorted(input_dir.glob("*.avi"))


def process_batch(
    files: list[Path],
    input_dir: Path,
    output_dir: Path,
    archive_dir: Path,
    overwrite: bool = False,
    dry_run: bool = False,
    console: Console | None = None,
) -> BatchResult:
    result = BatchResult(total=len(files))
    if console is None:
        console = Console()
    start = time.time()

    with Progress(console=console) as progress:
        task = progress.add_task("Converting...", total=len(files))

        for file_path in files:
            out_path = output_dir / file_path.with_suffix(".mp4").name
            arc_path = archive_dir / file_path.name

            if out_path.exists() and not overwrite:
                result.skipped += 1
                progress.advance(task)
                continue

            if dry_run:
                result.would_convert += 1
                progress.advance(task)
                continue

            ok, err_msg = convert_file(file_path, out_path, overwrite=overwrite)

            if ok:
                shutil.move(str(file_path), str(arc_path))
                result.success += 1
            else:
                result.failed += 1
                result.errors.append((file_path.name, err_msg))
                if out_path.exists():
                    out_path.unlink(missing_ok=True)

            progress.advance(task)

    result.duration = time.time() - start
    return result


def print_summary(result: BatchResult, console: Console) -> None:
    table = Table(title="Conversion Summary")
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Total files", str(result.total))
    if result.would_convert:
        table.add_row("Would convert", f"[cyan]{result.would_convert}[/cyan]")
    else:
        table.add_row("Success", f"[green]{result.success}[/green]")
        table.add_row("Failed", f"[red]{result.failed}[/red]")
    table.add_row("Skipped", str(result.skipped))
    table.add_row("Duration", f"{result.duration:.1f}s")

    console.print(table)

    for filename, err in result.errors:
        console.print(f"[red]  {filename}: {err}[/red]")
