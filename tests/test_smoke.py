import subprocess
import sys
import tempfile
from pathlib import Path

AVI2MP4 = [sys.executable, "-m", "avi2mp4.cli"]
FFMPEG = [
    "ffmpeg",
    "-y",
    "-f",
    "lavfi",
    "-i",
    "testsrc=duration=1:size=64x48:rate=10",
    "-f",
    "lavfi",
    "-i",
    "anullsrc=r=44100:cl=mono",
    "-c:v",
    "libx264",
    "-c:a",
    "aac",
    "-t",
    "1",
]


def make_avi(dir: Path, name: str = "test.avi") -> Path:
    path = dir / name
    subprocess.run(
        FFMPEG + [str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return path


def test_no_input_files():
    with tempfile.TemporaryDirectory() as tmp:
        inp = Path(tmp) / "input"
        out = Path(tmp) / "output"
        arc = Path(tmp) / "archive"
        inp.mkdir()
        out.mkdir()
        arc.mkdir()
        r = subprocess.run(
            AVI2MP4 + ["-i", str(inp), "-o", str(out), "-a", str(arc)],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0, f"expected 0, got {r.returncode}"
        assert "No .avi files" in r.stdout


def test_dry_run():
    with tempfile.TemporaryDirectory() as tmp:
        inp = Path(tmp) / "input"
        out = Path(tmp) / "output"
        arc = Path(tmp) / "archive"
        inp.mkdir()
        out.mkdir()
        arc.mkdir()
        make_avi(inp)
        r = subprocess.run(
            AVI2MP4 + ["-i", str(inp), "-o", str(out), "-a", str(arc), "--dry-run"],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0
        assert not list(out.iterdir()), "dry-run should not create output"
        assert not list(arc.iterdir()), "dry-run should not archive"


def test_single_conversion():
    with tempfile.TemporaryDirectory() as tmp:
        inp = Path(tmp) / "input"
        out = Path(tmp) / "output"
        arc = Path(tmp) / "archive"
        inp.mkdir()
        out.mkdir()
        arc.mkdir()
        make_avi(inp)
        r = subprocess.run(
            AVI2MP4 + ["-i", str(inp), "-o", str(out), "-a", str(arc)],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0, f"stdout: {r.stdout}\nstderr: {r.stderr}"
        mp4s = list(out.glob("*.mp4"))
        assert len(mp4s) == 1, f"expected 1 mp4, got {len(mp4s)}"
        avis = list(arc.glob("*.avi"))
        assert len(avis) == 1, f"expected 1 archived avi, got {len(avis)}"


def test_batch_conversion():
    with tempfile.TemporaryDirectory() as tmp:
        inp = Path(tmp) / "input"
        out = Path(tmp) / "output"
        arc = Path(tmp) / "archive"
        inp.mkdir()
        out.mkdir()
        arc.mkdir()
        for i in range(3):
            make_avi(inp, f"clip{i}.avi")
        r = subprocess.run(
            AVI2MP4 + ["-i", str(inp), "-o", str(out), "-a", str(arc)],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0
        assert len(list(out.glob("*.mp4"))) == 3
        assert len(list(arc.glob("*.avi"))) == 3


def test_skip_existing():
    with tempfile.TemporaryDirectory() as tmp:
        inp = Path(tmp) / "input"
        out = Path(tmp) / "output"
        arc = Path(tmp) / "archive"
        inp.mkdir()
        out.mkdir()
        arc.mkdir()
        make_avi(inp)
        (out / "test.mp4").write_text("fake")
        r = subprocess.run(
            AVI2MP4 + ["-i", str(inp), "-o", str(out), "-a", str(arc)],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0
        assert not list(arc.iterdir()), "should NOT archive when output skipped"


def test_overwrite_existing():
    with tempfile.TemporaryDirectory() as tmp:
        inp = Path(tmp) / "input"
        out = Path(tmp) / "output"
        arc = Path(tmp) / "archive"
        inp.mkdir()
        out.mkdir()
        arc.mkdir()
        make_avi(inp)
        r = subprocess.run(
            AVI2MP4 + ["-i", str(inp), "-o", str(out), "-a", str(arc), "--overwrite"],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0
        assert len(list(out.glob("*.mp4"))) == 1
        assert len(list(arc.glob("*.avi"))) == 1


def test_special_chars():
    with tempfile.TemporaryDirectory() as tmp:
        inp = Path(tmp) / "input"
        out = Path(tmp) / "output"
        arc = Path(tmp) / "archive"
        inp.mkdir()
        out.mkdir()
        arc.mkdir()
        make_avi(inp, "my video (test) - [2024].avi")
        r = subprocess.run(
            AVI2MP4 + ["-i", str(inp), "-o", str(out), "-a", str(arc)],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0, f"stdout: {r.stdout}\nstderr: {r.stderr}"
        assert len(list(out.glob("*.mp4"))) == 1
        assert len(list(arc.glob("*.avi"))) == 1


def test_summary_table():
    with tempfile.TemporaryDirectory() as tmp:
        inp = Path(tmp) / "input"
        out = Path(tmp) / "output"
        arc = Path(tmp) / "archive"
        inp.mkdir()
        out.mkdir()
        arc.mkdir()
        make_avi(inp)
        r = subprocess.run(
            AVI2MP4 + ["-i", str(inp), "-o", str(out), "-a", str(arc)],
            capture_output=True,
            text=True,
        )
        assert "Conversion Summary" in r.stdout
        assert "Total files" in r.stdout
        assert "Success" in r.stdout
        assert "Duration" in r.stdout


if __name__ == "__main__":
    tests = [
        ("no_input", test_no_input_files),
        ("dry_run", test_dry_run),
        ("single", test_single_conversion),
        ("batch", test_batch_conversion),
        ("skip_existing", test_skip_existing),
        ("overwrite", test_overwrite_existing),
        ("special_chars", test_special_chars),
        ("summary", test_summary_table),
    ]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  [OK] {name}")
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1

    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
