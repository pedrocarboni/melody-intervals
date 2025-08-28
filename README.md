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
- Melodic contour (↑, ↓, →)

## Inputs

- MIDI (`.mid`, `.midi`)
- MusicXML (`.musicxml`, `.xml`)

## Usage

```bash
python extract.py examples/melody.mid
# Options:
#   --json       Output in JSON format
#   --out FILE   Save output to file
```

## Example Output

Plain Text
```
Interval profile: +2M, +2M, −3m, →, +2M, −2m
Contour: ↑, ↑, ↓, →, ↑, ↓
```
JSON
```
{
  "sequence": ["+2M", "+2M", "−3m", "→", "+2M", "−2m"],
  "contour":  ["↑", "↑", "↓", "→", "↑", "↓"]
}
```

## How it works

- Parses MIDI/MusicXML (via `music21`) and walks note-to-note skipping rests.
- Computes directed intervals and labels them (e.g., m2/M3/P4/A4…).


## Roadmap

- Basic stats (--stats)
- Ambitus (melodic range, min/max span)
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
