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
    }

    FALLBACKS = {
        "+": dict(name="Unresolved Chord", vibration="Dissonance", color="Muddy Brown",
                  meaning="Two things that don't know each other yet"),
        "-": dict(name="Ash", vibration=0, color="Grey", meaning="Entropy"),
        "/": dict(name="Undefined", vibration=0, color="Transparent", meaning="Numbness"),
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


# --- THE SIMULATION ---
def type_writer(text, delay=0.04):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        pause(delay)
    print("")


def run_simulation():
    print("\n" + "=" * 40)
    print("  INITIALIZING RESONANCE MATH KERNEL v9.0")
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


# --- EXECUTE ---
if __name__ == "__main__":
    run_simulation()
