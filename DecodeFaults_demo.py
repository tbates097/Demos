# This example does not require the 'automation1' library to be installed
# because we are simulating the necessary objects.
import sys
sys.path.append(r"K:\10. Released Software\Shared Python Programs\production-2.1")
from DecodeFaults import decode_faults # Make sure DecodeFaults.py is in the same directory

# --- Step 1: Create Mock Objects to Simulate Dependencies ---

class MockLogger:
    """A fake logger that just prints messages to the console."""
    def error(self, message):
        print(f"LOGGER [ERROR]: {message}")

class MockA1Commands:
    """A fake command structure for the mock controller."""
    def acknowledgeall(self, keep_enabled_state):
        print(f"CONTROLLER: AcknowledgeAll command received (keep_enabled_state={keep_enabled_state}).")

class MockA1Runtime:
    """A fake runtime structure for the mock controller."""
    def __init__(self):
        # This nested structure mimics the real automation1 API
        class FaultAndError:
            def __init__(self):
                self.acknowledgeall = MockA1Commands().acknowledgeall
        self.commands = type('Commands', (), {'fault_and_error': FaultAndError()})()

class MockController:
    """A fake controller that mimics the automation1.Controller structure."""
    def __init__(self):
        self.runtime = MockA1Runtime()

# --- Step 2: Prepare Sample Data ---

# Create instances of our mock objects
mock_controller = MockController()
mock_logger = MockLogger()

# Define a list of axes connected to our mock controller
AXES_LIST = ['AxisX', 'AxisY', 'AxisZ']

# Create a sample dictionary of fault codes.
# A real application would get this from the controller hardware.
# - AxisX has a PositionErrorFault (1) and an AmplifierFault (64). 1 + 64 = 65.
# - AxisY has an OverCurrentFault (2).
# - AxisZ has no faults.
FAULTS_DATA = {
    'AxisX': 65,  # Represents (1 << 0) | (1 << 6)
    'AxisY': 2,   # Represents (1 << 1)
    'AxisZ': 0    # No faults
}

print("--- Starting Fault Decoding Demo ---")
print(f"Initial fault codes: {FAULTS_DATA}\n")

# --- Step 3: Instantiate and Run the Decoder ---

# Create an instance of the decode_faults class with our mock objects and data
fault_decoder = decode_faults(
    faults_per_axis=FAULTS_DATA,
    connected_axes=AXES_LIST,
    controller=mock_controller,
    fault_log=mock_logger
)

# Call the main method to decode, log, acknowledge, and get the results
decoded_results = fault_decoder.get_fault()

# --- Step 4: Display the Results ---

print("\n--- Decoding Complete ---")
print("Returned dictionary of decoded faults:")
print(decoded_results)