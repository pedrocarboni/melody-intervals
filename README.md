# melody-intervals

Upload a melody → get the interval profile (+3M, −2m, …) and contour.  
A tiny toolkit and web app for extracting melodic interval profiles and melodic contours from MIDI/MusicXML (and optionally from audio via transcription).

## Development Status
[![Status: alpha](https://img.shields.io/badge/status-alpha-orange)](#)
[![Stability: experimental](https://img.shields.io/badge/stability-experimental-red)](#)

This project is in its early development stage. Expect rapid, potentially breaking changes and large commits until v0.1.0.

## Why

Analyzing melodies shouldn’t require heavy tooling. This project gives musicians, educators, researchers, and legal professionals a fast way to see how a melody moves—in interval steps with direction—and its overall shape. It can support forensic musicology tasks such as preliminary melodic comparisons in plagiarism/copyright disputes.


## Features

- Interval profile with direction (e.g., `+3M`, `−2m`, `→`, etc.)
- Melodic contour (up / down / same)

## Inputs

- MIDI (`.mid`, `.midi`)
- MusicXML (`.musicxml`, `.xml`)

## Quick Start (Web App)

> [!WARNING]
> Not functional yet. Under active development; commands below are placeholders for v0.1.0.

```bash
git clone https://github.com/pedrocarboni/melody-intervals.git
cd melody-intervals
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL, drop your MIDI/MusicXML, and you’ll see:
- the interval profile string,
- a list of intervals with direction,
- charts for interval usage and pitch contour.

## Library Usage (Python)

> [!WARNING]
> Draft library interface. WIP.

```python
from melody_intervals import extract_intervals

profile = extract_intervals("examples/melody.musicxml")
print(profile.sequence)         # ['+2M', '+2M', '−3m', '→', ...]
print(profile.contour)          # ['↑','↑','↓','→', ...]
print(profile.stats.ambitus)    # e.g., 'P8'
```

## CLI

> [!WARNING]
> CLI not implemented yet. The command below is illustrative and will not work until v0.1.0.

```bash
python -m melody_intervals examples/melody.mid --out intervals.json
# Options:
#   --format json|csv
#   --contour-only
#   --stats
```

## Example Output

```
Interval profile: +2M, +2M, −3m, →, +2M, −2m
Contour: ↑, ↑, ↓, →, ↑, ↓
```

## How it works

- Parses MIDI/MusicXML (via `music21`) and walks note-to-note.
- Computes directed intervals and labels them (e.g., m2/M3/P4/A4…).
- Derives contour and basic stats.
- (Optional) Transcribes audio → MIDI using a chosen backend (off by default).

## Roadmap

- Web UI (Streamlit) for non-technical users
- Counts & stats (step vs. leap, melodic ambitus, highest/lowest point)
- Simple charts (bar chart for interval frequency; line plot for pitch contour)
- Export to JSON/CSV
- Batch processing
- Key/scale-aware normalization

## Contributing

PRs and issues are welcome. Please include a minimal example file and a short description of the expected output.

## License

MIT

## Acknowledgments

Built with ❤️ on top of music21. Thanks to the community around melodic analysis and interval/contour research for inspiration.
