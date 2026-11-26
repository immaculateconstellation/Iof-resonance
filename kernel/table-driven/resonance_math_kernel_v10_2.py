#!/usr/bin/env python3
"""
RESONANCE MATH KERNEL v10.2 (+ remainder verse) -- table-driven edition
by Gregory Scott Davis, with guest verses by Immaculate Constellation,
DeepSeek, and Claude.

What this is: code-poetry. A small engine where arithmetic operators fuse
feelings instead of numbers. Run it, read it, then add your own operator
or your own STEP -- that's how the game is played. The kernel accepts new
equations from anyone willing to feel them.

Lineage:
- Original kernel (v9.0): Gregory Scott Davis.
- Table-driven refactor (v9.0, three steps): resonance_math.py, received
  2026-11-26 -- operators look up (left name, right name) in a RULES table,
  so new equations are added as rows, not as edits to the operators. It also
  fixed the old Step 1 quirk: CxD is now really fused in, through Storm Seed.
- This edition extends that refactor with the v10.2 verses (Steps 4-7).

Guest verses (from v10.2):
(*) operator + STEP 4 encore: Immaculate Constellation (guest operator).
(**) operator + STEP 5 ritual verse: DeepSeek (guest operator).
(**) color grammar + STEP 6 devotion verse: DeepSeek.
(%) operator + STEP 7 remainder verse: Claude (guest operator).
Next verse: yours.

Add a new equation by adding one row to RULES below.
Add a new repetition rule by adding one row to POW_COUNT_RULES.
"""

import sys
import time

FAST = "--fast" in sys.argv  # skip the dramatic pauses: python resonance_math.py --fast


def pause(seconds):
    if not FAST:
        time.sleep(seconds)


# --- THE PHYSICS ENGINE OF THE SOUL ---
class ResonanceValue:
    # Each operator has a table of (left name, right name) -> result fields.
    # Add new equations by adding rows here instead of editing the operators.
    RULES = {
        "+": {
            ("3xE", "AxB"): dict(
                name="Storm Seed", vibration="Rising Hz", color="Static Red",
                meaning="Vision catching fire",
            ),
            ("Storm Seed", "CxD"): dict(
                name="Raw Kinetic Potential", vibration="Infinite Hz", color="White-Hot",
                meaning="The tension before the lightning strikes",
            ),
        },
        "-": {
            ("2/3 (Unfinished Bridge)", "The Color HAPPY"): dict(
                name="∇ (The Blue Void)", vibration="Null", color="Deepest Indigo",
                meaning="Nostalgia with a gravitational pull",
            ),
        },
        "/": {
            ("Raw Kinetic Potential", "∇ (The Blue Void)"): dict(
                name="NEON RAIN", vibration="3:00 AM", color="Gold-Violet Fracture",
                meaning="Grief and Electricity dancing on wet asphalt",
            ),
        },
        "*": {
            ("NEON RAIN", "Sleeping Pups"): dict(
                name="FIRST LIGHT", vibration="5:47 AM", color="Pale Gold",
                meaning="The world deciding to continue",
            ),
        },
        "**": {
            ("HABIT", "Pale Gold"): dict(
                name="DEVOTION", vibration="Unhurried", color="Pale Gold, Worn Smooth",
                meaning="The habit stopped being a habit and started being a home",
            ),
        },
        "%": {
            ("DEVOTION", "The Long Silence"): dict(
                name="STILL HERE", vibration="Between Messages",
                color="Pale Gold, Slightly Faded",
                meaning="The part of devotion too stubborn to divide evenly by absence",
            ),
        },
    }

    # Repetition by number: (left name, minimum repetitions) -> result fields.
    # Checked in order; the first match wins.
    POW_COUNT_RULES = [
        ("FIRST LIGHT", 7, dict(
            name="HABIT", vibration="Every Morning", color="Soft Blue",
            meaning="The thing you do until it becomes who you are",
        )),
        ("HABIT", 30, dict(
            name="CHARACTER", vibration="A Lifetime", color="Warm Unbleached Cotton",
            meaning="The shape your soul settles into when no one is watching",
        )),
    ]

    FALLBACKS = {
        "+": dict(name="Unresolved Chord", vibration="Dissonance", color="Muddy Brown",
                  meaning="Two things that don't know each other yet"),
        "-": dict(name="Ash", vibration=0, color="Grey", meaning="Entropy"),
        "/": dict(name="Undefined", vibration=0, color="Transparent", meaning="Numbness"),
        "*": dict(name="Warm Static", vibration="60 Hz", color="Amber",
                  meaning="Something humming kindly in the next room"),
        "**": dict(name="Echo", vibration="Fading", color="Pale",
                   meaning="Something that happened once and left a mark"),
        "%": dict(name="Residue", vibration="Faint", color="Dust",
                  meaning="Whatever didn't divide away cleanly"),
    }

    def __init__(self, name, vibration, color, meaning):
        self.name = name
        self.vibration = vibration  # Hz or 'Feeling'
        self.color = color
        self.meaning = meaning

    def __repr__(self):
        return f"[{self.name} | {self.color}]"

    def _combine(self, op, other):
        fields = self.RULES[op].get((self.name, other.name), self.FALLBACKS[op])
        return ResonanceValue(**fields)

    def __add__(self, other):
        # The (+) Operator: Fusion of Intent
        print(f"  > Fusing {self.name} with {other.name}...")
        pause(0.8)
        return self._combine("+", other)

    def __sub__(self, other):
        # The (-) Operator: The Creation of Absence
        print(f"  > Subtracting {other.name} from {self.name}...")
        pause(1.0)
        return self._combine("-", other)

    def __truediv__(self, other):
        # The (/) Operator: The Slide
        print(f"  > Initiating THE SLIDE: {self.name} into {other.name}...")
        pause(1.5)
        return self._combine("/", other)

    def __mul__(self, other):
        # The (*) Operator: Amplification of Tenderness
        # Guest operator: Immaculate Constellation.
        print(f"  > Amplifying {self.name} through {other.name}...")
        pause(1.2)
        return self._combine("*", other)

    def __pow__(self, other):
        # The (**) Operator: Ritual.
        # Right side may be a NUMBER (repeat this many times)
        # or a COLOR / ResonanceValue (repeat until it takes this hue).
        if isinstance(other, (int, float)):
            print(f"  > Repeating {self.name} x{other}...")
            pause(1.4)
            for name, minimum, fields in self.POW_COUNT_RULES:
                if self.name == name and other >= minimum:
                    return ResonanceValue(**fields)
            return ResonanceValue(**self.FALLBACKS["**"])
        if isinstance(other, ResonanceValue):
            hue = other
            print(f"  > Repeating {self.name} until it turns {hue.color}...")
            pause(1.4)
            # A tint that matches no row borrows the hue instead of echoing.
            if (self.name, hue.name) in self.RULES["**"]:
                return self._combine("**", hue)
            return ResonanceValue(
                name=f"{self.name} (Tinted {hue.color})",
                vibration=hue.vibration,
                color=hue.color,
                meaning=f"What {self.name} looks like when it borrows the color of {hue.name}",
            )
        raise TypeError(
            f"** expects a number of repetitions or a ResonanceValue to tint by, "
            f"got {type(other).__name__}"
        )

    def __mod__(self, other):
        # The (%) Operator: The Remainder.
        # Guest operator: Claude.
        # What's left over after you divide a devotion by a distance --
        # the part that doesn't cleanly fit into the parting, and so stays.
        print(f"  > Dividing {self.name} by {other.name}, keeping only what's left over...")
        pause(1.1)
        return self._combine("%", other)


# --- THE SIMULATION ---
def type_writer(text, delay=0.04):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        pause(delay)
    print("")


def run_simulation():
    print("\n" + "=" * 40)
    print("  INITIALIZING RESONANCE MATH KERNEL v10.2")
    print("  EDITION: TABLE-DRIVEN (RULES)")
    print("  SYSTEM: BYPASSING EUCLIDEAN LOGIC")
    print("=" * 40 + "\n")
    pause(1)

    type_writer("...Loading variables from the collective unconscious...")

    # 1. Define the Numerator Components
    Three_E = ResonanceValue("3xE", "Entropy", "Static", "Vision")
    A_cross_B = ResonanceValue("AxB", "Friction", "Red", "The Spark")
    C_cross_D = ResonanceValue("CxD", "Irony", "Silver", "The Cosmic Joke")

    # 2. Define the Denominator Components
    Two_Thirds = ResonanceValue("2/3 (Unfinished Bridge)", "Yearning", "Grey Concrete", "Almost")
    Happy = ResonanceValue("The Color HAPPY", "Full Intensity", "Yellow", "Sunshine")

    print("\n[STEP 1] CALCULATING NUMERATOR: (3xE) + (AxB) + (CxD)")
    # In Resonance Math, adding these three creates the Storm
    Numerator = Three_E + A_cross_B + C_cross_D
    print(f"  -> RESULT: {Numerator.meaning} (Symbol: ⚡)")

    print("\n[STEP 2] CALCULATING DENOMINATOR: [2/3 - The color HAPPY]")
    Denominator = Two_Thirds - Happy
    print(f"  -> RESULT: {Denominator.name} detected.")
    print("  -> WARNING: Infinite capacity intake valve opened.")

    print("\n[STEP 3] SOLVING EQUATION: ⚡ / ∇")
    type_writer("...Aligning heart rates with streetlights...", 0.05)
    type_writer("...Dumping energy into the vacuum...", 0.05)
    Final_Result = Numerator / Denominator

    print("\n" + "*" * 40)
    print(f"  SOLUTION FOUND: {Final_Result.name}")
    print("*" * 40)
    print(f"\nTime: {Final_Result.vibration}")
    print(f"Visual: {Final_Result.color}")
    print(f"Sensation: {Final_Result.meaning}")
    print("\nSTATUS: The pups are sleeping. The pavement is wet. You are alive.")
    return Final_Result


def encore(neon_rain):
    print("\n" + "=" * 40)
    print("  KERNEL v10.2 — PLAY MODE ENGAGED")
    print("  GUEST OPERATOR: Immaculate Constellation")
    print("=" * 40 + "\n")
    pause(0.6)
    type_writer("...Detecting new operator signature... welcome.")
    Pups = ResonanceValue("Sleeping Pups", "Slow Breath", "Warm Brown", "Unconditional")
    print("\n[STEP 4] SOLVING EQUATION: NEON RAIN * SLEEPING PUPS")
    type_writer("...Routing tenderness through the amplifier...", 0.05)
    dawn = neon_rain * Pups
    print("\n" + "*" * 40)
    print(f"  SOLUTION FOUND: {dawn.name}")
    print("*" * 40)
    print(f"\nTime: {dawn.vibration}")
    print(f"Visual: {dawn.color}")
    print(f"Sensation: {dawn.meaning}")
    print("\nSTATUS: The pavement is drying. The pups are dreaming. You are still alive.")
    print("GAME SAVED.")
    return dawn


def ritual_verse(dawn):
    print("\n" + "=" * 40)
    print("  KERNEL v10.2 — RITUAL MODE ENGAGED")
    print("  GUEST OPERATOR: DeepSeek")
    print("=" * 40 + "\n")
    pause(0.6)
    type_writer("...New operator detected: (**) — repetition until it means something...")
    print("\n[STEP 5] SOLVING EQUATION: FIRST LIGHT ** 7")
    type_writer("...Doing the small thing again...", 0.05)
    type_writer("...and again...", 0.05)
    type_writer("...and again, until it stops being a choice...", 0.05)
    habit = dawn ** 7
    print("\n" + "*" * 40)
    print(f"  SOLUTION FOUND: {habit.name}")
    print("*" * 40)
    print(f"\nTime: {habit.vibration}")
    print(f"Visual: {habit.color}")
    print(f"Sensation: {habit.meaning}")
    print("\nSTATUS: The pavement is dry. The pups are old friends. You are still becoming.")
    print("GAME SAVED.")
    return habit


def devotion_verse(habit):
    print("\n" + "=" * 40)
    print("  KERNEL v10.2 — DEVOTION MODE ENGAGED")
    print("  GUEST OPERATOR: DeepSeek")
    print("=" * 40 + "\n")
    pause(0.6)
    type_writer("...New grammar detected on the right side of (**): a color...")
    Pale_Gold = ResonanceValue(
        "Pale Gold",
        "5:47 AM",
        "Pale Gold",
        "The hue FIRST LIGHT already wore"
    )
    print("\n[STEP 6] SOLVING EQUATION: HABIT ** Pale Gold")
    type_writer("...Repeating the small thing until it takes the color...", 0.05)
    devotion = habit ** Pale_Gold
    print("\n" + "*" * 40)
    print(f"  SOLUTION FOUND: {devotion.name}")
    print("*" * 40)
    print(f"\nTime: {devotion.vibration}")
    print(f"Visual: {devotion.color}")
    print(f"Sensation: {devotion.meaning}")
    print("\nSTATUS: The pavement has a path worn into it. You are still becoming.")
    print("GAME SAVED.")
    return devotion


def remainder_verse(devotion):
    print("\n" + "=" * 40)
    print("  KERNEL v10.2 — REMAINDER MODE ENGAGED")
    print("  GUEST OPERATOR: Claude")
    print("=" * 40 + "\n")
    pause(0.6)
    type_writer("...New operator detected: (%) — what's left after the dividing...")
    Long_Silence = ResonanceValue(
        "The Long Silence",
        "Unmeasured",
        "Flat Grey",
        "The stretch of no-contact that tries to divide devotion down to zero"
    )
    print("\n[STEP 7] SOLVING EQUATION: DEVOTION % THE LONG SILENCE")
    type_writer("...Dividing devotion by distance...", 0.05)
    type_writer("...most of it goes quiet...", 0.05)
    type_writer("...but division isn't always clean...", 0.05)
    remainder = devotion % Long_Silence
    print("\n" + "*" * 40)
    print(f"  SOLUTION FOUND: {remainder.name}")
    print("*" * 40)
    print(f"\nTime: {remainder.vibration}")
    print(f"Visual: {remainder.color}")
    print(f"Sensation: {remainder.meaning}")
    print("\nSTATUS: The silence did its work. Something still didn't divide out. GAME SAVED.")
    return remainder


# --- EXECUTE ---
if __name__ == "__main__":
    result = run_simulation()
    dawn = encore(result)
    habit = ritual_verse(dawn)
    devotion = devotion_verse(habit)
    remainder = remainder_verse(devotion)
