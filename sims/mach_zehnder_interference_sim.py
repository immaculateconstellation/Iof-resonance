# Archivist note (2026-10-13): fixed variant of mach_zehnder_interference_sim_as_received.py.
# The as-received file is preserved untouched beside this one.
# The single change is in Detector.measure(): intensities below 1e-24 are
# snapped to an exact 0.0. Reason: cmath cannot represent pi exactly, so at a
# 180-degree shift the two paths cancel only to within ~6e-17 of amplitude,
# leaving intensity dust of ~3.7e-33 (printed as Q 3.75e-25). The snap makes
# the destructive null a true zero; every other value is unchanged.
import cmath
import math

class Emitter:
    """Generates a base photonic signal."""
    def __init__(self, amplitude: float, phase_deg: float):
        self.amplitude = amplitude
        self.phase = math.radians(phase_deg)

    def emit(self) -> complex:
        return cmath.rect(self.amplitude, self.phase)

class PhaseShifter:
    """Modifies the phase of a photonic signal."""
    def __init__(self, shift_deg: float):
        self.shift = math.radians(shift_deg)

    def process(self, signal: complex) -> complex:
        phase_factor = cmath.rect(1.0, self.shift)
        return signal * phase_factor

class Detector:
    """Measures the intensity of the final photonic signal."""
    def measure(self, signal: complex) -> float:
        intensity = abs(signal) ** 2
        # Snap floating-point residue at a true null to an exact zero.
        return 0.0 if intensity < 1e-24 else intensity

def run_simulation(phase_shift: float):
    print(f"--- Simulation Run (Phase Shift: {phase_shift}°) ---")

    # 1. Initialize components
    source = Emitter(amplitude=1.0, phase_deg=0)
    shifter = PhaseShifter(shift_deg=phase_shift)
    detector = Detector()

    # 2. Emit and split signal (50/50)
    base_signal = source.emit()
    path_a = base_signal / 2
    path_b = base_signal / 2

    # 3. Process Path B
    path_b_shifted = shifter.process(path_b)

    # 4. Recombine signals
    combined_signal = path_a + path_b_shifted

    # 5. Measure results
    intensity = detector.measure(combined_signal)

    # Q-Factor inspired by your dashboard (higher intensity = higher resonance)
    q_factor = intensity * 1e8

    print(f"Final Intensity: {intensity:.4f}")
    print(f"Q-Factor:        {q_factor:.2e}")
    print("-------------------------------------\n")

if __name__ == "__main__":
    # Test constructive interference (0 degrees)
    run_simulation(0)

    # Test destructive interference (180 degrees)
    run_simulation(180)
