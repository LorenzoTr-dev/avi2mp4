import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


THEMES = {
    "azure": "#00DFFF",
    "red": "#FF5555",
    "purple": "#BD93F9",
    "green": "#50FA7B",
}
DEFAULT_THEME = "azure"
_CONFIG_FILE = Path.home() / ".avi2mp4.json"

console = Console(force_terminal=True)


def get_theme() -> str:
    try:
        cfg = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
        return cfg.get("theme_color", DEFAULT_THEME)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_THEME


def set_theme(theme: str) -> None:
    cfg = {}
    try:
        cfg = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    cfg["theme_color"] = theme
    _CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def wait_for_user(message: str = "to return to menu") -> None:
    color = THEMES.get(get_theme(), THEMES[DEFAULT_THEME])
    prompt = Text("\nPress ", style="#AAAAAA")
    prompt.append("Enter", style=f"bold {color}")
    prompt.append(f" {message}...", style="#AAAAAA")
    console.print(prompt)
    input()


def show_header(title: str) -> None:
    print("\033[H\033[2J\033[3J", end="")
    color = THEMES.get(get_theme(), THEMES[DEFAULT_THEME])
    panel = Panel(
        f"[bold white on {color}] {title} [/]",
        border_style=color,
        padding=(0, 2),
    )
    console.print(panel)


def show_splash() -> None:
    console.clear()
    theme_key = get_theme()
    color = THEMES.get(theme_key, THEMES[DEFAULT_THEME])

    panel = Panel(
        "  Welcome to avi2mp4  ",
        border_style=color,
        padding=(0, 2),
        expand=False,
    )
    console.print()
    console.print(panel)
    console.print()

    ascii_art = (
        f"[bold {color}]"
        "   _   _ _ __ ___   ___  ____  \n"
        "  / \\ | | '_ ` _ \\ / _ \\|  _ \\ \n"
        " / _ \\| | | | | | | (_) | |_) |\n"
        "/_/ \\_\\_|_| |_| |_|\\___/|____/ \n"
        "[/]"
    )
    console.print(ascii_art)

    prompt = Text("Press ", style="#AAAAAA")
    prompt.append("Enter", style=f"bold {color}")
    prompt.append(" to continue...", style="#AAAAAA")
    console.print(prompt)
    input()
