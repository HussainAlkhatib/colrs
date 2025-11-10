# tests/test_effects.py

import pytest
import sys
import io
import time
from colrs import effects
from colrs.core import COLORS

# We need to patch sys.stdout and time.sleep to test these functions.

@pytest.fixture
def mock_stdout(monkeypatch):
    """A pytest fixture to capture stdout and mock time.sleep."""
    output_buffer = io.StringIO()
    monkeypatch.setattr(sys.stdout, 'write', output_buffer.write)
    monkeypatch.setattr(sys.stdout, 'flush', lambda: None)
    monkeypatch.setattr(time, 'sleep', lambda x: None)
    return output_buffer

def test_typewriter_effect(mock_stdout):
    """Tests the typewriter effect by capturing stdout."""
    test_text = "Hi"
    effects.typewriter(test_text, color="red", speed=0)
    
    # The final output should be the fully colored string.
    # We check the buffer's final value.
    # The function prints the final string with a newline at the end.
    # We need to reconstruct the expected final output.
    expected_output = f"{COLORS['red']}Hi{COLORS['reset']}\n"
    
    # The buffer will contain intermediate writes, but the final state should be this.
    # This is a simplified test. We'll check if the final visible output is correct.
    # The actual buffer contains '\r' characters. Let's find the last line.
    last_line = mock_stdout.getvalue().strip().split('\r')[-1]
    assert last_line == f"{COLORS['red']}Hi{COLORS['reset']}"

def test_rainbow_effect(mock_stdout):
    """Tests the rainbow effect for a very short duration."""
    test_text = "RAINBOW"
    effects.rainbow(test_text, duration=0.1, speed=0) # Run for a very short time
    
    output = mock_stdout.getvalue()
    # Check that it produced some output and used some of our rainbow colors
    assert len(output) > 0
    assert COLORS['red'] in output or COLORS['yellow'] in output

def test_gradient_effect(mock_stdout):
    """Tests the gradient effect for a very short duration."""
    test_text = "GRADIENT"
    effects.gradient(test_text, start_color="blue", end_color="red", duration=0.1, speed=0)
    
    output = mock_stdout.getvalue()
    # Check that it produced some output and used a TrueColor ANSI code
    assert len(output) > 0
    assert "\033[38;2;" in output # Signature of a TrueColor code