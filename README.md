# avi2mp4

[![CI](https://github.com/LorenzoTr-dev/avi2mp4/actions/workflows/test.yml/badge.svg)](https://github.com/LorenzoTr-dev/avi2mp4/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[English](#english) | [Italiano](#italiano)

---

## English

`avi2mp4` is a Python CLI for converting AVI files to MP4 with `ffmpeg`. It supports batch conversion, an interactive menu, safe archiving, and configurable input/output folders.

### Preview

![avi2mp4 screenshot](./Screenshot%202026-06-23%20165010.png)

### Features

- Batch conversion with Rich progress bars
- Interactive menu to change folders, theme, dry-run, and overwrite options
- Automatic archive move only after successful conversion
- Safe dry-run mode
- Simple packaging and command-line entry point

### Requirements

- Python 3.10+
- `ffmpeg` available in your `PATH`

### Installation

```bash
git clone https://github.com/LorenzoTr-dev/avi2mp4.git
cd avi2mp4
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

Install the project:

```bash
pip install .
```

For development:

```bash
pip install -e .[dev]
```

### Usage

```bash
# Default folders: ./input -> ./output, archive originals in ./archive
avi2mp4

# Custom paths
avi2mp4 -i ./my_videos -o ./converted_videos -a ./archive_folder

# Dry-run
avi2mp4 --dry-run

# Overwrite existing MP4 files
avi2mp4 --overwrite

# Interactive mode
avi2mp4 --interactive
```

### CLI Arguments

| Flag | Shortcut | Default | Description |
| --- | --- | --- | --- |
| `--input` | `-i` | `./input` | Source AVI directory |
| `--output` | `-o` | `./output` | Destination MP4 directory |
| `--archive` | `-a` | `./archive` | Archive directory for original AVIs |
| `--dry-run` | - | - | Run without converting files |
| `--overwrite` | - | - | Overwrite existing MP4 files |
| `--interactive` | `-m` | - | Launch interactive menu |

### Testing

```bash
python tests/test_smoke.py
pytest
```

## Italiano

`avi2mp4` e una CLI Python per convertire file AVI in MP4 con `ffmpeg`. Supporta conversione batch, menu interattivo, archiviazione sicura e cartelle configurabili.

### Anteprima

![screenshot di avi2mp4](./Screenshot%202026-06-23%20165010.png)

### Funzionalita

- Conversione batch con barre di avanzamento Rich
- Menu interattivo per cambiare cartelle, tema, dry-run e overwrite
- Spostamento automatico dei file originali solo dopo conversione riuscita
- Modalita dry-run sicura
- Packaging semplice e comando CLI pronto per `pip install`

### Requisiti

- Python 3.10+
- `ffmpeg` disponibile nel `PATH`

### Installazione

```bash
git clone https://github.com/LorenzoTr-dev/avi2mp4.git
cd avi2mp4
python -m venv .venv
```

Attiva l'ambiente virtuale:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

Installa il progetto:

```bash
pip install .
```

Per sviluppo:

```bash
pip install -e .[dev]
```

### Utilizzo

```bash
# Cartelle di default: ./input -> ./output, originali archiviati in ./archive
avi2mp4

# Percorsi personalizzati
avi2mp4 -i ./my_videos -o ./converted_videos -a ./archive_folder

# Dry-run
avi2mp4 --dry-run

# Sovrascrivi i file MP4 esistenti
avi2mp4 --overwrite

# Modalita interattiva
avi2mp4 --interactive
```

### Argomenti CLI

| Flag | Shortcut | Default | Descrizione |
| --- | --- | --- | --- |
| `--input` | `-i` | `./input` | Cartella sorgente AVI |
| `--output` | `-o` | `./output` | Cartella destinazione MP4 |
| `--archive` | `-a` | `./archive` | Cartella archivio per gli AVI originali |
| `--dry-run` | - | - | Esegui senza convertire i file |
| `--overwrite` | - | - | Sovrascrivi i file MP4 esistenti |
| `--interactive` | `-m` | - | Avvia il menu interattivo |

### Test

```bash
python tests/test_smoke.py
pytest
```
