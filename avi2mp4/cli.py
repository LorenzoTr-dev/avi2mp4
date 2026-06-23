import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import questionary

from .batch import process_batch, print_summary, scan_avi_files
from rich.panel import Panel

from .ui import (
    THEMES,
    console,
    get_theme,
    set_theme,
    show_header,
    show_splash,
    wait_for_user,
)
from .utils import check_ffmpeg, ensure_dir, validate_directories


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert AVI files to MP4 using ffmpeg",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        default=Path("./input"),
        help="Source AVI folder (default: ./input)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("./output"),
        help="Destination MP4 folder (default: ./output)",
    )
    parser.add_argument(
        "--archive",
        "-a",
        type=Path,
        default=Path("./archive"),
        help="Archive folder for original AVIs (default: ./archive)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without converting",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing MP4 files",
    )
    parser.add_argument(
        "--interactive",
        "-m",
        action="store_true",
        help="Launch interactive menu",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()

    if args.interactive:
        interactive_menu(args)
        return

    if not check_ffmpeg():
        console.print(
            "[red]ERROR: ffmpeg not found in PATH. "
            "Install ffmpeg before using this tool.[/red]"
        )
        sys.exit(1)

    input_dir = ensure_dir(args.input)
    output_dir = ensure_dir(args.output)
    archive_dir = ensure_dir(args.archive)

    warnings = validate_directories(input_dir, output_dir, archive_dir)
    for w in warnings:
        console.print(f"[yellow]Warning: {w}[/yellow]")

    files = scan_avi_files(input_dir)

    if not files:
        console.print("[yellow]No .avi files found in input folder.[/yellow]")
        console.print(
            "[dim]Tip: use --interactive (-m) for the interactive menu.[/dim]"
        )
        sys.exit(0)

    result = process_batch(
        files=files,
        input_dir=input_dir,
        output_dir=output_dir,
        archive_dir=archive_dir,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
        console=console,
    )

    print_summary(result, console)
    sys.exit(1 if result.failed > 0 else 0)


@dataclass
class _Settings:
    input_dir: Path
    output_dir: Path
    archive_dir: Path
    dry_run: bool
    overwrite: bool


def interactive_menu(args: argparse.Namespace) -> None:
    settings = _Settings(
        input_dir=ensure_dir(args.input),
        output_dir=ensure_dir(args.output),
        archive_dir=ensure_dir(args.archive),
        dry_run=args.dry_run,
        overwrite=args.overwrite,
    )

    show_splash()

    while True:
        show_header("avi2mp4")

        ffmpeg_status = (
            "[green]\u2713[/green]" if check_ffmpeg() else "[red]\u2717[/red]"
        )
        console.print(f"  ffmpeg: {ffmpeg_status}\n")

        dry_str = "[yellow]ON[/yellow]" if settings.dry_run else "[green]OFF[/green]"
        ovw_str = "[yellow]ON[/yellow]" if settings.overwrite else "[green]OFF[/green]"

        theme_key = get_theme()
        theme_color = THEMES.get(theme_key, "#00DFFF")
        settings_panel = Panel(
            f"  [dim]Input dir:[/dim]   {settings.input_dir}\n"
            f"  [dim]Output dir:[/dim]  {settings.output_dir}\n"
            f"  [dim]Archive dir:[/dim] {settings.archive_dir}\n"
            f"  [dim]Dry-run:[/dim]     {dry_str}\n"
            f"  [dim]Overwrite:[/dim]   {ovw_str}\n",
            title="Current Configuration",
            border_style=theme_color,
        )
        console.print(settings_panel)

        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Convert AVI Files",
                "Change Input Directory",
                "Change Output Directory",
                "Change Archive Directory",
                "Toggle Dry-Run",
                "Toggle Overwrite",
                "Change Theme Color",
                "Exit",
            ],
            use_indicator=True,
        ).ask()

        if action is None:
            break

        if action == "Convert AVI Files":
            _run_interactive_batch(settings)
            wait_for_user()
        elif action == "Change Input Directory":
            path = questionary.path(
                "Input directory",
                default=str(settings.input_dir),
                only_directories=True,
            ).ask()
            if path:
                settings.input_dir = ensure_dir(Path(path))
                console.print("[green]Input directory updated![/green]")
        elif action == "Change Output Directory":
            path = questionary.path(
                "Output directory",
                default=str(settings.output_dir),
                only_directories=True,
            ).ask()
            if path:
                settings.output_dir = ensure_dir(Path(path))
                console.print("[green]Output directory updated![/green]")
        elif action == "Change Archive Directory":
            path = questionary.path(
                "Archive directory",
                default=str(settings.archive_dir),
                only_directories=True,
            ).ask()
            if path:
                settings.archive_dir = ensure_dir(Path(path))
                console.print("[green]Archive directory updated![/green]")
        elif action == "Toggle Dry-Run":
            settings.dry_run = not settings.dry_run
            status = "ON" if settings.dry_run else "OFF"
            console.print(f"[green]Dry-run toggled {status}![/green]")
        elif action == "Toggle Overwrite":
            settings.overwrite = not settings.overwrite
            status = "ON" if settings.overwrite else "OFF"
            console.print(f"[green]Overwrite toggled {status}![/green]")
        elif action == "Change Theme Color":
            _select_theme()
        elif action == "Exit":
            break


def _run_interactive_batch(settings: _Settings) -> None:
    if not check_ffmpeg():
        console.print(
            "[red]ERROR: ffmpeg not found in PATH. Install ffmpeg first.[/red]"
        )
        return

    warnings = validate_directories(
        settings.input_dir, settings.output_dir, settings.archive_dir
    )
    for w in warnings:
        console.print(f"[yellow]Warning: {w}[/yellow]")
    if warnings:
        proceed = questionary.confirm(
            "Continue with current settings?", default=False
        ).ask()
        if not proceed:
            return

    files = scan_avi_files(settings.input_dir)
    if not files:
        console.print("[yellow]No .avi files found in input folder.[/yellow]")
        return

    result = process_batch(
        files=files,
        input_dir=settings.input_dir,
        output_dir=settings.output_dir,
        archive_dir=settings.archive_dir,
        overwrite=settings.overwrite,
        dry_run=settings.dry_run,
        console=console,
    )
    print_summary(result, console)


def _select_theme() -> None:
    current = get_theme()
    theme_display = {
        "azure": "Azure Blue (Default)",
        "red": "Crimson Red",
        "purple": "Deep Purple",
        "green": "Vibrant Green",
    }
    choices = [
        {"name": display, "value": key} for key, display in theme_display.items()
    ]
    result = questionary.select(
        "Select a color theme:",
        choices=choices,
    ).ask()

    if result and result != current:
        set_theme(result)
        console.print(f"[green]Theme changed to {theme_display[result]}![/green]")


if __name__ == "__main__":
    main()
