# avi2mp4

[![CI](https://github.com/Lorenzo/avi2mp4/actions/workflows/test.yml/badge.svg)](https://github.com/Lorenzo/avi2mp4/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[English](#english) | [Italiano](#italiano)

---

## English

CLI tool to convert AVI files to MP4 using `ffmpeg`. Features batch processing with progress bars, interactive CLI menu, and automated directory management (input/output/archive).

### Features
- 🚀 **Batch Processing**: Convert multiple AVI files sequentially with a beautiful Rich progress bar.
- 🎨 **Interactive Menu**: Run in interactive mode to change paths, toggle dry-run or overwrite options, customize themes, and launch conversions.
- 📂 **Smart Archiving**: Automatically moves original AVI files to an archive directory only upon successful conversion.
- 🛠️ **Configurable**: Fully customizable input, output, and archive directories.
- 🛡️ **Safe**: Optional dry-run mode and option to overwrite or skip existing files.

### Requirements
- Python 3.10+
- `ffmpeg` installed and added to your system `PATH` ([download ffmpeg](https://ffmpeg.org/download.html))

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Lorenzo/avi2mp4.git
   cd avi2mp4
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install the package**:
   ```bash
   pip install .
   ```

   *For development setup (including tests and linting tools):*
   ```bash
   pip install -e .[dev]
   ```

### Usage

#### Command Line Mode
```bash
# Default folders: ./input → ./output, original files archived in ./archive
avi2mp4

# Custom paths
avi2mp4 -i ./my_videos -o ./converted_videos -a ./archive_folder

# Dry-run (lists what would be converted without doing anything)
avi2mp4 --dry-run

# Overwrite existing MP4 files
avi2mp4 --overwrite
```

#### Interactive Menu Mode
You can launch an interactive UI/menu with:
```bash
avi2mp4 --interactive
# or
avi2mp4 -m
```

#### CLI Arguments

| Flag | Shortcut | Default | Description |
|------|----------|---------|-------------|
| `--input` | `-i` | `./input` | Source AVI directory |
| `--output` | `-o` | `./output` | Destination MP4 directory |
| `--archive` | `-a` | `./archive` | Archive directory for original AVIs |
| `--dry-run` | — | — | Run without converting files |
| `--overwrite` | — | — | Overwrite existing MP4 files |
| `--interactive` | `-m` | — | Launch interactive menu |

---

## Italiano

Strumento da riga di comando (CLI) per convertire file AVI in MP4 usando `ffmpeg`. Include elaborazione batch con barre di progresso, menu interattivo e gestione automatica delle cartelle (input/output/archive).

### Caratteristiche
- 🚀 **Elaborazione Batch**: Converte file AVI in sequenza con una barra di avanzamento avanzata.
- 🎨 **Menu Interattivo**: Avvia una modalità interattiva per modificare i percorsi, attivare il dry-run, scegliere il tema grafico e lanciare la conversione.
- 📂 **Archiviazione Sicura**: Sposta i file AVI originali nell'archivio solo a conversione riuscita.
- 🛠️ **Configurabile**: Personalizza liberamente le cartelle di input, output e archivio.
- 🛡️ **Sicuro**: Previene la sovrascrittura accidentale (attivabile con flag) e supporta la modalità dry-run.

### Requisiti
- Python 3.10+
- `ffmpeg` installato e presente nel `PATH` di sistema ([download ffmpeg](https://ffmpeg.org/download.html))

### Installazione

1. **Clona il repository**:
   ```bash
   git clone https://github.com/Lorenzo/avi2mp4.git
   cd avi2mp4
   ```

2. **Crea e attiva un ambiente virtuale**:
   ```bash
   python -m venv .venv
   # Su Windows:
   .venv\Scripts\activate
   # Su macOS/Linux:
   source .venv/bin/activate
   ```

3. **Installa il pacchetto**:
   ```bash
   pip install .
   ```

   *Per lo sviluppo (include pytest e ruff):*
   ```bash
   pip install -e .[dev]
   ```

### Sviluppo e Test

Per verificare la formattazione e l'esecuzione dei test:
```bash
# Esegui i test unitari/smoke
python tests/test_smoke.py

# Se hai installato le dipendenze dev, puoi usare pytest
pytest
```
