# style_6.py: Clock Spinner
import itertools

def run(text, color):
    """Displays a spinning clock-hand animation."""
    clock_chars = ['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚']
    spinner = itertools.cycle(clock_chars)
    while True:
        yield f"<{color}>{{text}} {next(spinner)}</>"