from __future__ import annotations
import argparse, json
from typing import List, Dict
from music21 import converter, note as m21note, chord as m21chord, interval, pitch
import colorama
from colorama import Fore, Style

colorama.init()

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

def _is_step(label):
    """Step = ±2M/±2m (ignores '→')."""
    if label == "→":
        return False
    core = label[1:] if label and label[0] in {"+", MINUS} else label
    return core.startswith("2M") or core.startswith("2m")

def _ambitus_name(midi_list):
    if not midi_list:
        return "P1"
    lo, hi = min(midi_list), max(midi_list)
    if lo == hi:
        return "P1"
    return interval.Interval(pitch.Pitch(midi=lo), pitch.Pitch(midi=hi)).name  # ex: 'P8', 'M9', etc.

def extract_intervals(path, with_stats):
    """
    Loads the file and returns:
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

    if with_stats:
        steps = sum(1 for lab in sequence if _is_step(lab))
        leaps = sum(1 for lab in sequence if (lab != "→" and not _is_step(lab)))
        counts = {}
        for lab in sequence:
            counts[lab] = counts.get(lab, 0) + 1

        out["stats"] = {
            "ambitus": _ambitus_name(midi_vals),
            "steps": steps,
            "leaps": leaps,
            "interval_counts": counts,
        }
    return out

def main():
    p = argparse.ArgumentParser(
        description="Extracts directed interval profile (+nQ/−nQ/→) and contour (↑/↓/→) from MIDI/MusicXML."
    )
    p.add_argument("input", help="File: .mid/.midi/.musicxml/.xml")
    p.add_argument("--json", action="store_true", help="Enables output in JSON format")
    p.add_argument("--stats", action="store_true", help="Enables stats (ambitus, steps/leaps, histogram)")
    p.add_argument("--out", type=str, help="Save output to file")
    args = p.parse_args()

    res = extract_intervals(args.input, with_stats=args.stats)
    if args.json:
        output = json.dumps(res, ensure_ascii=False, indent=2)
    else:
        # Colore cada símbolo do contorno conforme solicitado
        colored_contour = [
            f"{Fore.GREEN}{c}{Style.RESET_ALL}" if c == "↑"
            else f"{Fore.RED}{c}{Style.RESET_ALL}" if c == "↓"
            else f"{Fore.YELLOW}{c}{Style.RESET_ALL}" for c in res['contour']
        ]
        # Colore cada intervalo conforme o sinal
        colored_sequence = [
            f"{Fore.GREEN}{s}{Style.RESET_ALL}" if s.startswith("+")
            else f"{Fore.RED}{s}{Style.RESET_ALL}" if s.startswith("−")
            else f"{Fore.YELLOW}{s}{Style.RESET_ALL}" for s in res['sequence']
        ]
        output = (
            f"{Fore.CYAN}Interval profile:{Style.RESET_ALL} {', '.join(colored_sequence)}\n"
            f"{Fore.CYAN}Contour:{Style.RESET_ALL} {' '.join(colored_contour)}"
        )
        if args.stats and "stats" in res:
            stats = res["stats"]
            output += (
                f"\n\n{Fore.MAGENTA}Stats:{Style.RESET_ALL}"
                f"\n    {Fore.CYAN}Ambitus:{Style.RESET_ALL} {Fore.YELLOW}{stats['ambitus']}{Style.RESET_ALL}"
                f"\n    {Fore.CYAN}Steps:{Style.RESET_ALL} {Fore.YELLOW}{stats['steps']}{Style.RESET_ALL}"
                f"\n    {Fore.CYAN}Leaps:{Style.RESET_ALL} {Fore.YELLOW}{stats['leaps']}{Style.RESET_ALL}"
                f"\n    {Fore.CYAN}Interval counts:{Style.RESET_ALL} {Fore.YELLOW}{stats['interval_counts']}{Style.RESET_ALL}"
            )

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)

if __name__ == "__main__":
    main()