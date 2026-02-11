# Kokoro-FastAPI German

Deutsche Text-to-Speech API basierend auf [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) und dem [Kokoro-German](https://huggingface.co/Tundragoon/Kokoro-German) Modell.

## Features

- Deutsche Sprachsynthese mit 2 Stimmen: `df_eva` (weiblich) und `dm_bernd` (männlich)
- OpenAI-kompatible Speech API (`/v1/audio/speech`)
- Integrierter Web-Player mit Wellenform-Visualisierung
- Streaming-Unterstützung
- Voice-Mixing mit gewichteten Kombinationen
- CPU- und GPU-Inferenz (PyTorch)

## Quick Start

### Voraussetzungen

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (Python Package Manager)

### Installation & Start

```powershell
# Repository klonen
git clone https://github.com/r1di/kokoro-fastapi-german.git
cd kokoro-fastapi-german

# Server starten (installiert Dependencies automatisch)
.\start-cpu.ps1
```

Der Server läuft auf **http://localhost:8880**.

### Web-Player

Öffne **http://localhost:8880/web/** im Browser:

- Text eingeben
- Deutsche Stimme auswählen (`df_eva` oder `dm_bernd`)
- Sprache auf "German" setzen
- "Generate Speech" klicken

### API-Nutzung

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8880/v1", api_key="not-needed")

with client.audio.speech.with_streaming_response.create(
    model="kokoro",
    voice="df_eva",
    input="Hallo Welt! Wie geht es Ihnen heute?"
) as response:
    response.stream_to_file("output.mp3")
```

### API-Endpunkte

| Endpunkt | Beschreibung |
|----------|-------------|
| `POST /v1/audio/speech` | Text-to-Speech Generierung |
| `GET /v1/audio/voices` | Verfügbare Stimmen auflisten |
| `GET /health` | Health-Check |
| `GET /docs` | Swagger API-Dokumentation |
| `GET /web/` | Web-Player |

## Technische Details

- **Modell**: [Kokoro-German v1.1](https://huggingface.co/Tundragoon/Kokoro-German) (~82M Parameter)
- **Sample Rate**: 24 kHz
- **Audio-Formate**: MP3 (192 kbps), WAV, FLAC, Opus, PCM
- **Phonemizer**: espeak-ng via `espeakng-loader` (keine Systeminstallation nötig)

## Credits

- [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) von remsky — FastAPI-Wrapper und Web-UI
- [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) von HexGrad — Basis-TTS-Modell
- [Kokoro-German](https://huggingface.co/Tundragoon/Kokoro-German) von Tundragoon — Deutsches Fine-Tuning
- [kokoro_german](https://github.com/Thomcle/kokoro_german) von Thomcle — Deutsche Kokoro-Fork
- [espeak-ng](https://github.com/espeak-ng/espeak-ng) — Phonemizer-Backend

## Lizenz

Apache License 2.0 — siehe [Upstream-Lizenz](https://github.com/remsky/Kokoro-FastAPI/blob/master/LICENSE).
