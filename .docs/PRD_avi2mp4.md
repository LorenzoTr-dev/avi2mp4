# PRD: avi2mp4 — CLI Tool per Conversione AVI → MP4

## 1. Visione e Obiettivo

Tool CLI in Python che automatizza la conversione di uno o più file AVI in MP4 usando **ffmpeg**, con:

- Gestione di tre cartelle (input / output / archive)
- Progress bar unica per l'intero batch
- UX da CLI moderna (colori, messaggi chiari, output pulito)

Non è pensato come prodotto pubblico per ora, ma come utility personale estendibile (altri formati in futuro).

---

## 2. Use Case Principali

### UC1 – Conversione singolo file

1. L'utente mette 1 file AVI nella cartella **input**
2. Lancia il comando CLI
3. Il tool converte il file in MP4 con codec standard (H.264/AAC) tramite ffmpeg
4. Salva il file risultante in **output**
5. Sposta il file AVI originale in **archive**
6. Mostra esito (success/fail) ed eventuali errori

### UC2 – Conversione batch

1. L'utente mette N file AVI (N > 1) nella cartella **input**
2. Lancia il comando CLI
3. Il tool:
   - Conta i file in input
   - Processa uno alla volta
   - Aggiorna una progress bar globale (0–100%) basata sul numero di file completati
   - Alla fine mostra un riepilogo: numeri di successi, fallimenti, tempo totale

### UC3 – Configurazione percorsi

L'utente può:

- Passare i path di input, output e archive come argomenti CLI
- Oppure usare valori di default (es. cartelle relative alla directory corrente)
- Se una cartella non esiste, il tool la crea (se possibile) o fallisce con messaggio chiaro

---

## 3. Scope Funzionale

### 3.1 Funzionalità incluse (MVP)

| Area | Dettaglio |
|------|-----------|
| **Conversione AVI→MP4** | `ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4` — transcodifica standard H.264/AAC |
| **Batch processing** | Scansione della cartella input per file `.avi` (case-insensitive); iterazione in ordine alfabetico |
| **Gestione cartelle** | `input_dir`: sorgente AVI · `output_dir`: destinazione MP4 · `archive_dir`: archivio AVI originali post-conversione |
| **Progress bar** | Una progress bar sul numero di file convertiti (non sul progresso interno di ffmpeg per ogni file) |
| **Logging base** | Messaggi strutturati: INFO / WARN / ERROR; log su stdout con colori; riepilogo finale (file totali, successi, falliti) |

### 3.2 Fuori scope per l'MVP

- Supporto di altri formati (MKV, MOV, ecc.)
- Parametri avanzati ffmpeg (bitrate custom, preset, filtri, ecc.)
- Progress bar "per file" basata sull'output live di ffmpeg
- Config file persistente
- GUI
- Packaging in binario standalone

---

## 4. Interfaccia CLI

### 4.1 Comando principale

**Nome (provvisorio):** `avi2mp4`

```
avi2mp4 \
  --input ./input \
  --output ./output \
  --archive ./archive
```

| Parametro | Descrizione | Default |
|-----------|-------------|---------|
| `--input` / `-i` | Cartella sorgente AVI | `./input` |
| `--output` / `-o` | Cartella destinazione MP4 | `./output` |
| `--archive` / `-a` | Cartella archivio AVI | `./archive` |
| `--dry-run` | Mostra cosa farebbe senza eseguire ffmpeg | — |
| `--overwrite` | Sovrascrive file MP4 esistenti | — |

### 4.2 UX e stile "moderno"

- Libreria **rich** per: colori (verde = success, rosso = error, giallo = warn), tabella riepilogo finale, progress bar pulita
- Output minimalista: niente spam del comando ffmpeg (solo in caso di errore o con `--verbose`)
- Convenzione messaggi:

```
[INFO] Scansione cartella input...
[INFO] Trovati 5 file .avi
[INFO] Inizio conversione batch...
[ OK ] file1.avi → file1.mp4
[ERR] file2.avi → conversione fallita (vedi dettagli)
```

---

## 5. Workflow Interno

### 5.1 Flow principale

```
┌─────────────────────────────┐
│  Parse argomenti CLI        │
│  (argparse / typer)         │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  Setup:                     │
│  - path assoluti            │
│  - creazione cartelle       │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  Scansione input_dir:       │
│  lista file .avi            │
│  (se vuoto → exit)          │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  Inizializzazione           │
│  progress bar (totale = N)  │
└──────────┬──────────────────┘
           ▼
     ┌─────┴─────┐
     │  Per ogni  │
     │  file:     │
     └─────┬─────┘
           ▼
┌─────────────────────────────┐
│  Costruisci path I/O        │
│  Verifica collisioni        │
│  (--overwrite o skip)       │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│  Esegui ffmpeg (subprocess) │
└──────────┬──────────────────┘
           │
     ┌─────┴─────┐
     │  Ok?       │
     └─────┬─────┘
     │             │
     ▼             ▼
  Sposta in     Non sposta
  archive       input
     │             │
     └──────┬──────┘
           ▼
┌─────────────────────────────┐
│  Aggiorna progress bar      │
└──────────┬──────────────────┘
           ▼
     ┌─────┴─────┐
     │  Fine      │
     │  batch?    │
     └─────┬─────┘
     │             │
    NO            SÌ
     │             ▼
     │   ┌─────────────────────┐
     └──►│  Riepilogo finale   │
         │  Exit code:         │
         │  0 = tutti ok       │
         │  1 = fallimenti     │
         └─────────────────────┘
```

1. **Parse argomenti CLI**
2. **Setup**: risoluzione path assoluti, creazione cartelle se mancano
3. **Scansione input_dir**: lista file .avi; se nessun file → messaggio e exit
4. **Inizializzazione progress bar**: totale = N, current = 0
5. **Per ogni file**:
   - Costruisce path completo input e output
   - Verifica collisione output (gestita con `--overwrite` o skip)
   - Esegue ffmpeg come subprocess
   - Se ffmpeg OK → sposta input in archive_dir, segna success
   - Se ffmpeg fallisce → non sposta input, segna failure
   - Aggiorna progress bar
6. **A fine batch**: stampa riepilogo, exit code 0 (tutti ok) o 1 (fallimenti)

### 5.2 Dettagli ffmpeg

```bash
ffmpeg -i input.avi -c:v libx264 -c:a aac -y output.mp4
```

| Flag | Significato |
|------|-------------|
| `-c:v libx264` | Codec video H.264 |
| `-c:a aac` | Codec audio AAC (standard per MP4) |
| `-y` | Sovrascrive output senza chiedere (combinato con `--overwrite`) |

Per la prima versione non servono parametri avanzati (preset, crf, ecc.).

---

## 6. Requisiti Tecnici

### 6.1 Stack

| Componente | Specifica |
|------------|-----------|
| **Linguaggio** | Python 3.10+ |
| **Librerie stdlib** | `argparse` (o `typer`), `pathlib`, `subprocess`, `shutil` |
| **Librerie esterne** | `rich` (output e progress bar) |
| **Dipendenza esterna** | `ffmpeg` installato nel sistema e disponibile nel PATH |

### 6.2 Struttura dei moduli (proposta)

```
cli.py         # Entrypoint, parsing argomenti, wiring
converter.py   # convert_file(input_path, output_path) → bool
batch.py       # Scansione cartelle, loop file, progress bar, stats
utils.py       # Creazione cartelle, validazione path, logging base
```

---

## 7. Requisiti Non Funzionali

| Requisito | Dettaglio |
|-----------|-----------|
| **Robustezza** | Gestione errori ffmpeg (codice di ritorno subprocess); messaggi user-friendly per ffmpeg non trovato, permessi mancanti, file corrotti |
| **Performance** | Elaborazione sequenziale sufficiente (bottleneck è ffmpeg) |
| **Portabilità** | Target minimo: Windows e Linux (path handling con `pathlib`) |
| **Manutenibilità** | Moduli separati; facilità di aggiungere nuovi formati (mappa `input_ext → ffmpeg command`) |

---

## 8. Estensioni Future Previste

- **Supporto di più formati**: mappa configurabile `{"avi": "mp4", "mov": "mp4"}` con comandi ffmpeg associati
- **Config file**: `~/.avi2mp4/config.toml` con percorsi di default, preset ffmpeg, ecc.
- **Modalità "watch"**: watcher sulla cartella input, conversione automatica all'arrivo di nuovi file
- **Packaging**: pubblicazione su PyPI; wrapper `__main__.py` per `python -m avi2mp4`

---

## 9. Acceptance Criteria (MVP)

Un primo rilascio è considerato **accettato** se:

1. **Conversione singolo file**: da cartella vuota, creo input/output/archive, sposto `video.avi` in input e lancio `avi2mp4` → `video.mp4` in output, `video.avi` in archive, messaggio di successo

2. **Conversione batch**: con N file `.avi` in input → progress bar 0→N, riepilogo finale con tutte e tre le cartelle popolate

3. **ffmpeg non installato**: il tool rileva l'errore e stampa:
   ```
   ERROR: ffmpeg non trovato nel PATH. Installa ffmpeg prima di usare questo tool.
   ```

4. **File output già esistente (senza `--overwrite`)**: logga errore per quel file, non sovrascrive, prosegue con gli altri file
