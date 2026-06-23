from pathlib import Path
import subprocess


FFMPEG_ARGS = ["-c:v", "libx264", "-c:a", "aac"]


def convert_file(
    input_path: Path,
    output_path: Path,
    timeout: int = 300,
    overwrite: bool = False,
) -> tuple[bool, str]:
    cmd = ["ffmpeg", "-i", str(input_path)]
    if overwrite:
        cmd.append("-y")
    cmd.extend(FFMPEG_ARGS)
    cmd.append(str(output_path))
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return True, ""
        stderr = result.stderr.strip() if result.stderr else ""
        return False, stderr or "ffmpeg returned a non-zero exit code"
    except subprocess.TimeoutExpired:
        return False, f"conversion timed out after {timeout}s"
    except FileNotFoundError:
        return False, "ffmpeg not found in PATH"
