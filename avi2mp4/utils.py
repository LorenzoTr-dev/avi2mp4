from pathlib import Path
import shutil


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def validate_directories(
    input_dir: Path, output_dir: Path, archive_dir: Path
) -> list[str]:
    resolved = {
        "Input": input_dir.resolve(),
        "Output": output_dir.resolve(),
        "Archive": archive_dir.resolve(),
    }
    warnings: list[str] = []
    names = list(resolved.keys())
    for i, (name1, path1) in enumerate(resolved.items()):
        for name2 in names[i + 1 :]:
            path2 = resolved[name2]
            if path1 == path2:
                warnings.append(f"{name1} and {name2} are the same directory")
            elif path1 in path2.parents:
                warnings.append(f"{name1} is inside {name2}")
            elif path2 in path1.parents:
                warnings.append(f"{name2} is inside {name1}")
    return warnings
