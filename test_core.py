# tests/test_core.py

import pytest
from colrs.core import _process_text_for_printing, _strip_all_tags, colorize, COLORS

# This is the heart of the library, so we test it thoroughly.

def test_colorize_function():
    """Tests the basic colorize wrapper."""
    text = "hello"
    colored_text = colorize(text, "green")
    assert colored_text == f"{COLORS['green']}{text}{COLORS['reset']}"
    assert colorize(text) == text # Should return text as-is if no color.

def test_strip_tags():
    """Tests the tag stripping utility."""
    complex_string = "<yellow>Hello <blue>world</blue>!</yellow>"
    assert _strip_all_tags(complex_string) == "Hello world!"
    simple_string = "<green>OK</>"
    assert _strip_all_tags(simple_string) == "OK"

@pytest.mark.parametrize("input_text, expected_output_contains", [
    # Test case 1: Simple tag
    (
        "<green>Success</>",
        f"{COLORS['green']}Success{COLORS['reset']}"
    ),
    # Test case 2: Multiple tags
    (
        "Status: <green>OK</> | Memory: <red>HIGH</>",
        f"Status: {COLORS['green']}OK{COLORS['reset']} | Memory: {COLORS['red']}HIGH{COLORS['reset']}"
    ),
    # Test case 3: The critical nested tag test
    (
        "<yellow>Warning: <blue>service</blue> is down.</yellow>",
        f"{COLORS['yellow']}Warning: {COLORS['blue']}service{COLORS['reset']}{COLORS['yellow']} is down.{COLORS['reset']}"
    ),
    # Test case 4: No tags, just base color
    (
        "This is a simple message.",
        f"{COLORS['cyan']}This is a simple message.{COLORS['reset']}"
    ),
    # Test case 5: Tag with background color
    (
        "<white,bg_red> EMERGENCY </>",
        f"\033[41m{COLORS['white']} EMERGENCY {COLORS['reset']}"
    )
])
def test_process_text_for_printing(input_text, expected_output_contains):
    """Tests the main color parsing engine with various scenarios."""
    if "simple message" in input_text: # Specific check for the base color test
        assert _process_text_for_printing(input_text, color="cyan") == expected_output_contains
    else:
        assert _process_text_for_printing(input_text) == expected_output_contains