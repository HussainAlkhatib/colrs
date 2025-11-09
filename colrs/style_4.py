# style_4.py: Dual-Side Progress Bar
import itertools

def run(text, color):
    """Displays a progress bar that fills from both ends."""
    length = 40
    # Cycle through filling up to the middle
    for i in itertools.cycle(range(length // 2 + 1)):
        filled_len = i
        filled = '█' * filled_len
        empty = ' ' * (length - 2 * filled_len)
        yield f"<{color}>{{text}} [{filled}{empty}{filled}]</>"