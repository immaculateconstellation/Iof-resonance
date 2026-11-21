"""
NodeGanglion - Optical Neural Network Node
Based on 3-6-9 Sacred Geometry Connectivity
"""

import math
import random
import time

class NodeGanglion:
    def __init__(self, node_id, neighbors):
        self.id = node_id
        self.neighbors = neighbors
        self.phase = 0.0
        self.coupling_strength = 0.8
        self.local_error = 0.0
        self.step_delay = 10.0
        self.pulse_history = []

    def pulse(self, input_signal):
        # Kuramoto-inspired phase coupling
        for neighbor in self.neighbors:
            phase_diff = neighbor.phase - self.phase
            self.phase += self.coupling_strength * math.sin(phase_diff)
        
        # Adaptive rate based on error
        self.step_delay = self.map_error_to_ms(self.local_error)
        
        result = self.emit_optical_trigger(input_signal)
        self.pulse_history.append(result)
        return result

    def emit_optical_trigger(self, input_signal):
        # Optical interference pattern
        amplitude = math.sin(self.phase) * input_signal
        return {
            'node_id': self.id,
            'phase': self.phase,
            'amplitude': amplitude,
            'wavelength': 1550,  # nm (telecom C-band)
            'delay_ms': self.step_delay
        }

    def map_error_to_ms(self, error):
        # Higher error = faster pulses (more urgent processing)
        return max(1, min(50, 10 + error * 40))

def create_network():
    """Create a 3-6-9 connected neural network"""
    nodes = {}
    
    # Create all nodes first (as objects, not strings)
    # Core nodes (3)
    for i in range(3):
        nodes[f'core_{i}'] = NodeGanglion(f'core_{i}', [])
    
    # Inner ring (6)
    for i in range(6):
        nodes[f'ring1_{i}'] = NodeGanglion(f'ring1_{i}', [])
    
    # Outer ring (9)
    for i in range(9):
        nodes[f'ring2_{i}'] = NodeGanglion(f'ring2_{i}', [])
    
    # Now set neighbors using actual node objects
    for i in range(3):
        nodes[f'core_{i}'].neighbors = [nodes[f'ring1_{i*2}'], nodes[f'ring1_{(i*2+1) % 6}']]
    
    for i in range(6):
        nodes[f'ring1_{i}'].neighbors = [nodes[f'core_{i % 3}']]
    
    for i in range(9):
        nodes[f'ring2_{i}'].neighbors = [nodes[f'ring1_{i % 6}']]
    
    return nodes

def run_simulation():
    nodes = create_network()
    
    print("=" * 50)
    print("🧠 NodeGanglion Network - 3-6-9 Topology")
    print("=" * 50)
    
    # Run simulation steps
    for step in range(5):
        print(f"\n📡 Step {step + 1}")
        
        # Inject signal
        signal = random.uniform(0.5, 1.0)
        
        # Pulse core nodes first
        for i in range(3):
            result = nodes[f'core_{i}'].pulse(signal)
            print(f"   Core {i}: phase={result['phase']:.3f}, amp={result['amplitude']:.3f}")
        
        # Propagate to rings
        for i in range(6):
            nodes[f'ring1_{i}'].local_error = random.uniform(0, 0.3)
            result = nodes[f'ring1_{i}'].pulse(signal)
            print(f"   Ring1 {i}: delay={result['delay_ms']:.1f}ms")
        
        time.sleep(0.1)
    
    print("\n✅ Network synchronized via optical phase coupling")

if __name__ == "__main__":
    run_simulation()
