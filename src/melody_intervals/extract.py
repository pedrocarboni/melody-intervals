from __future__ import annotations
import argparse, json
from typing import List, Dict
from music21 import converter, note as m21note, chord as m21chord, interval, pitch

MINUS = "−"

def _iter_note_pitches_midi(s):
    """
    Gather MIDI heights from real notes, excluding pauses.
    For chords, takes the highest voice.
    If nothing found, tries the 1st part explicitly.
    """
    pitches: List[int] = []
    for el in s.recurse():
        if getattr(el, "isRest", False):
            continue

        # Simple note
        if isinstance(el, m21note.Note):
            pm = getattr(getattr(el, "pitch", None), "midi", None)
            if pm is not None:
                pitches.append(int(pm))
            continue

        # Chord
        if isinstance(el, m21chord.Chord) or getattr(el, "isChord", False):
            valid = [p.midi for p in getattr(el, "pitches", []) if getattr(p, "midi", None) is not None]
            if valid:
                pitches.append(int(max(valid)))
            continue

        # Other
        pm = getattr(getattr(el, "pitch", None), "midi", None)
        if pm is not None:
            pitches.append(int(pm))

    if not pitches and hasattr(s, "parts") and len(s.parts) > 0:
        return _iter_note_pitches_midi(s.parts[0].flatten())

    return pitches

def _qnum(name):
    """'M3' -> '3M', 'P5' -> '5P', etc."""
    if not name:
        return name
    q, num = name[0], name[1:]
    return f"{num}{q}"

def _directed_label(a, b) :
    if a == b:
        return "→"
    sign = "+" if b > a else MINUS
    iv = interval.Interval(pitch.Pitch(midi=a), pitch.Pitch(midi=b))  # Corrigido!
    return f"{sign}{_qnum(iv.name)}"

def _contour(a, b):
    if b > a: return "↑"
    if b < a: return "↓"
    return "→"

def extract_intervals(path):
    """
    Carrega o arquivo e retorna:
      { 'sequence': [...], 'contour': [...], [ 'stats': {...} ] }
    """
    s = converter.parse(path)
    midi_vals = _iter_note_pitches_midi(s)

    sequence: List[str] = []
    contour: List[str] = []
    for i in range(len(midi_vals) - 1):
        a, b = midi_vals[i], midi_vals[i + 1]
        sequence.append(_directed_label(a, b))
        contour.append(_contour(a, b))

    out: Dict = {"sequence": sequence, "contour": contour}

    return out

def main():
    p = argparse.ArgumentParser(
        description="Extrai perfil de intervalos dirigidos (+nQ/−nQ/→) e contorno (↑/↓/→) de MIDI/MusicXML."
    )
    p.add_argument("input", help="Arquivo .mid/.midi/.musicxml/.xml")
    args = p.parse_args()

    res = extract_intervals(args.input)
    print(res)

if __name__ == "__main__":
    main()