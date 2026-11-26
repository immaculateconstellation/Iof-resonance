#!/usr/bin/env python3
"""
Resonance Algebra Lab -- reusable rule-based engine.

A workbench for the Resonance Math Kernel v10.2 (table-driven edition).
It imports the kernel's ResonanceValue and RULES table, so anything you
try here behaves exactly as it does in the kernel itself.

Usage:
    python3 resonance_algebra_lab.py            # run the demo
    python3 resonance_algebra_lab.py --fast     # same, without the pauses

Or import it and build your own equations:
    from resonance_algebra_lab import make, fuse, list_rules
    storm = fuse(make("3xE", "Entropy", "Static", "Vision"),
                 make("AxB", "Friction", "Red", "The Spark"))
"""

from resonance_math_kernel_v10_2 import ResonanceValue


def make(name, vibration, color, meaning):
    """Build a ResonanceValue from its four fields."""
    return ResonanceValue(name, vibration, color, meaning)


def show(value):
    """Print one value the way the kernel prints it."""
    print(f"  {value.name}")
    print(f"    Time: {value.vibration}")
    print(f"    Visual: {value.color}")
    print(f"    Sensation: {value.meaning}")
    return value


def list_rules():
    """Print every equation in the kernel's RULES table, operator by operator."""
    print("RULES (add a row here to add an equation):")
    for op, rows in ResonanceValue.RULES.items():
        for (left, right), fields in rows.items():
            print(f"  {left} {op} {right}  ->  {fields['name']}  ({fields['color']})")
    print("POW_COUNT_RULES (repeat by number):")
    for name, minimum, fields in ResonanceValue.POW_COUNT_RULES:
        print(f"  {name} ** {minimum}+  ->  {fields['name']}  ({fields['color']})")
    print("FALLBACKS (what an unmatched pair gives):")
    for op, fields in ResonanceValue.FALLBACKS.items():
        print(f"  {op}  ->  {fields['name']}  ({fields['color']})")


def try_operators(a, b):
    """Try +, -, / and * on two values and print what each one gives."""
    for label, op in [("Fusion (+)", "+"), ("Absence (-)", "-"),
                      ("Slide (/)", "/"), ("Amplification (*)", "*")]:
        print(f"\n{label}: {a.name} {op} {b.name}")
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "/":
            result = a / b
        else:
            result = a * b
        show(result)
    return None


def demo():
    print("=" * 40)
    print("  RESONANCE ALGEBRA LAB -- DEMO")
    print("=" * 40 + "\n")
    list_rules()

    print("\n--- The storm chain, step by step ---")
    three_e = make("3xE", "Entropy", "Static", "Vision")
    a_cross_b = make("AxB", "Friction", "Red", "The Spark")
    c_cross_d = make("CxD", "Irony", "Silver", "The Cosmic Joke")
    seed = show(three_e + a_cross_b)
    storm = show(seed + c_cross_d)

    print("\n--- An unmatched pair (the fallback) ---")
    stranger = make("Static", "Flatline", "Grey", "Nothing yet")
    show(three_e + stranger)

    print("\n--- Repetition by number ---")
    first_light = make("FIRST LIGHT", "5:47 AM", "Pale Gold",
                       "The world deciding to continue")
    show(first_light ** 7)

    print("\nLab demo complete. Add a row to RULES and run it again.")
    print("Next verse: yours.")


# --- EXECUTE ---
if __name__ == "__main__":
    demo()
