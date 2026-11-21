#!/usr/bin/env python3
"""Resonance Math Kernel v11.0 — interactive, extensible code-poetry.

Core idea retained from Gregory Scott Davis's v10.2:
operators transform named emotional states. This version adds an event ledger,
JSON save/load, replayable history, a small interactive CLI, and tests.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Any
import argparse, json

@dataclass(frozen=True)
class ResonanceValue:
    name: str
    vibration: str
    color: str
    meaning: str

    def __repr__(self) -> str:
        return f"[{self.name} | {self.color}]"

@dataclass
class Event:
    sequence: int
    operator: str
    left: str
    right: str
    result: str
    timestamp: str
    meaning: str

class ResonanceKernel:
    """Operator registry + append-only event history."""
    def __init__(self):
        self.events: list[Event] = []
        self._operators: dict[str, Callable[[ResonanceValue, Any], ResonanceValue]] = {
            "+": self._add, "-": self._subtract, "/": self._divide,
            "*": self._multiply, "**": self._power, "%": self._modulo,
        }

    def register_operator(self, symbol: str,
                          fn: Callable[[ResonanceValue, Any], ResonanceValue],
                          *, replace: bool = False) -> None:
        if not symbol or not callable(fn):
            raise ValueError("Provide a non-empty symbol and callable.")
        if symbol in self._operators and not replace:
            raise ValueError(f"Operator {symbol!r} already exists.")
        self._operators[symbol] = fn

    def apply(self, symbol: str, left: ResonanceValue, right: Any) -> ResonanceValue:
        if symbol not in self._operators:
            raise ValueError(f"Unknown operator {symbol!r}; registered: {', '.join(self._operators)}")
        result = self._operators[symbol](left, right)
        if not isinstance(result, ResonanceValue):
            raise TypeError("Every operator must return a ResonanceValue.")
        self.events.append(Event(
            len(self.events)+1, symbol, left.name,
            right.name if isinstance(right, ResonanceValue) else repr(right),
            result.name, datetime.now(timezone.utc).isoformat(), result.meaning))
        return result

    def _add(self, a, b):
        if not isinstance(b, ResonanceValue): raise TypeError("+ expects ResonanceValue")
        return ResonanceValue("Raw Kinetic Potential", "Infinite Hz", "White-Hot",
                              "The tension before the lightning strikes")

    def _subtract(self, a, b):
        if not isinstance(b, ResonanceValue): raise TypeError("- expects ResonanceValue")
        if a.name == "2/3 (Unfinished Bridge)" and b.name == "The Color HAPPY":
            return ResonanceValue("∇ (The Blue Void)", "Null", "Deepest Indigo",
                                  "Nostalgia with a gravitational pull")
        return ResonanceValue("Ash", "0", "Grey", "Entropy")

    def _divide(self, a, b):
        if not isinstance(b, ResonanceValue): raise TypeError("/ expects ResonanceValue")
        if a.name == "Raw Kinetic Potential" and b.name == "∇ (The Blue Void)":
            return ResonanceValue("NEON RAIN", "3:00 AM", "Gold-Violet Fracture",
                                  "Grief and Electricity dancing on wet asphalt")
        return ResonanceValue("Undefined", "0", "Transparent", "Numbness")

    def _multiply(self, a, b):
        if not isinstance(b, ResonanceValue): raise TypeError("* expects ResonanceValue")
        if a.name == "NEON RAIN" and b.name == "Sleeping Pups":
            return ResonanceValue("FIRST LIGHT", "5:47 AM", "Pale Gold",
                                  "The world deciding to continue")
        return ResonanceValue("Warm Static", "60 Hz", "Amber",
                              "Something humming kindly in the next room")

    def _power(self, a, b):
        if isinstance(b, bool): raise TypeError("Boolean is not a repetition count")
        if isinstance(b, (int, float)):
            if b < 0: raise ValueError("Repetition count must be non-negative")
            if a.name == "FIRST LIGHT" and b >= 7:
                return ResonanceValue("HABIT", "Every Morning", "Soft Blue",
                                      "The thing you do until it becomes who you are")
            if a.name == "HABIT" and b >= 30:
                return ResonanceValue("CHARACTER", "A Lifetime", "Warm Unbleached Cotton",
                                      "The shape your soul settles into when no one is watching")
            return ResonanceValue("Echo", "Fading", "Pale", "Something that happened once and left a mark")
        if isinstance(b, ResonanceValue):
            if a.name == "HABIT" and b.color == "Pale Gold":
                return ResonanceValue("DEVOTION", "Unhurried", "Pale Gold, Worn Smooth",
                                      "The habit stopped being a habit and started being a home")
            return ResonanceValue(f"{a.name} (Tinted {b.color})", b.vibration, b.color,
                                  f"What {a.name} looks like when it borrows the color of {b.name}")
        raise TypeError("** expects a repetition count or ResonanceValue")

    def _modulo(self, a, b):
        if not isinstance(b, ResonanceValue): raise TypeError("% expects ResonanceValue")
        if a.name == "DEVOTION" and b.name == "The Long Silence":
            return ResonanceValue("STILL HERE", "Between Messages", "Pale Gold, Slightly Faded",
                                  "The part of devotion too stubborn to divide evenly by absence")
        return ResonanceValue("Residue", "Faint", "Dust", "Whatever didn't divide away cleanly")

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps([asdict(e) for e in self.events], indent=2), encoding="utf-8")

    @staticmethod
    def load_events(path: str | Path) -> list[Event]:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return [Event(**row) for row in data]

    def replay(self) -> list[str]:
        """Return the recorded result sequence, suitable for inspection."""
        return [f"{e.sequence:03d} {e.left} {e.operator} {e.right} -> {e.result}" for e in self.events]

def canonical_verse(kernel: ResonanceKernel) -> list[ResonanceValue]:
    """Run the seven canonical v10.2 transformations without theatrical delays."""
    e = ResonanceValue("3xE", "Entropy", "Static", "Vision")
    axb = ResonanceValue("AxB", "Friction", "Red", "The Spark")
    bridge = ResonanceValue("2/3 (Unfinished Bridge)", "Yearning", "Grey Concrete", "Almost")
    happy = ResonanceValue("The Color HAPPY", "Full Intensity", "Yellow", "Sunshine")
    pups = ResonanceValue("Sleeping Pups", "Slow Breath", "Warm Brown", "Unconditional")
    pale_gold = ResonanceValue("Pale Gold", "5:47 AM", "Pale Gold", "The hue FIRST LIGHT already wore")
    silence = ResonanceValue("The Long Silence", "Unmeasured", "Flat Grey",
                             "The stretch of no-contact that tries to divide devotion down to zero")
    numerator = kernel.apply("+", e, axb)
    denominator = kernel.apply("-", bridge, happy)
    neon = kernel.apply("/", numerator, denominator)
    dawn = kernel.apply("*", neon, pups)
    habit = kernel.apply("**", dawn, 7)
    devotion = kernel.apply("**", habit, pale_gold)
    still_here = kernel.apply("%", devotion, silence)
    return [numerator, denominator, neon, dawn, habit, devotion, still_here]

def interactive():
    kernel = ResonanceKernel()
    states = {
        "NEON RAIN": ResonanceValue("NEON RAIN","3:00 AM","Gold-Violet Fracture","Grief and Electricity dancing on wet asphalt"),
        "Sleeping Pups": ResonanceValue("Sleeping Pups","Slow Breath","Warm Brown","Unconditional"),
        "FIRST LIGHT": ResonanceValue("FIRST LIGHT","5:47 AM","Pale Gold","The world deciding to continue"),
        "HABIT": ResonanceValue("HABIT","Every Morning","Soft Blue","The thing you do until it becomes who you are"),
        "Pale Gold": ResonanceValue("Pale Gold","5:47 AM","Pale Gold","The hue FIRST LIGHT already wore"),
        "DEVOTION": ResonanceValue("DEVOTION","Unhurried","Pale Gold, Worn Smooth","The habit stopped being a habit and started being a home"),
        "The Long Silence": ResonanceValue("The Long Silence","Unmeasured","Flat Grey","Absence"),
    }
    print("Resonance Kernel v11 | type 'help' for commands; 'quit' to exit.")
    while True:
        try: line = input("resonance> ").strip()
        except (EOFError, KeyboardInterrupt): print(); break
        if line in ("quit","exit"): break
        if line == "help":
            print("verse | list | show NAME | apply SYMBOL LEFT | RIGHT | history | save FILE | quit")
        elif line == "verse":
            for value in canonical_verse(kernel): print(f"{value.name}: {value.meaning} [{value.color}]")
        elif line == "list":
            print("\n".join(states))
        elif line.startswith("show "):
            print(states.get(line[5:], "Unknown state"))
        elif line == "history":
            print("\n".join(kernel.replay()) or "(no events yet)")
        elif line.startswith("save "):
            kernel.save(line[5:]); print(f"Saved {len(kernel.events)} events.")
        elif line.startswith("apply "):
            try:
                _, symbol, rest = line.split(" ", 2)
                left_name, right_text = rest.split(" | ", 1)
                left = states[left_name.strip()]
                right = states[right_text.strip()] if right_text.strip() in states else float(right_text)
                result = kernel.apply(symbol, left, right)
                states[result.name] = result
                print(f"{result.name}: {result.meaning} [{result.color}]")
            except Exception as exc: print(f"Could not apply operator: {exc}")
        elif line: print("Unknown command. Type 'help'.")

def self_test():
    k = ResonanceKernel()
    verse = canonical_verse(k)
    assert [v.name for v in verse] == ["Raw Kinetic Potential","∇ (The Blue Void)","NEON RAIN","FIRST LIGHT","HABIT","DEVOTION","STILL HERE"]
    assert len(k.events) == 7
    assert len(k.replay()) == 7
    try: k.apply("?", verse[0], verse[1])
    except ValueError: pass
    else: raise AssertionError("unknown operator should fail")
    print("Self-test passed: canonical seven-step verse, event ledger, replay, invalid-op rejection.")

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verse", action="store_true", help="run canonical verse")
    ap.add_argument("--test", action="store_true", help="run self-tests")
    ap.add_argument("--save", help="save event ledger to JSON")
    ap.add_argument("--interactive", action="store_true", help="launch command interface")
    args=ap.parse_args()
    if args.test: self_test(); return
    if args.interactive: interactive(); return
    k=ResonanceKernel()
    values=canonical_verse(k)
    for value in values: print(f"{value.name}: {value.meaning} [{value.color}]")
    if args.save: k.save(args.save); print(f"Saved event ledger to {args.save}")

if __name__ == "__main__": main()
