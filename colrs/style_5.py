# style_5.py: Scanner Effect
import itertools

def run(text, color):
    """Displays a 'Knight Rider' style scanner."""
    length = 20
    # Create a sequence that goes 0, 1, ..., 18, 19, 18, ..., 1, 0 and repeat
    scan_sequence = itertools.cycle(list(range(length)) + list(range(length - 2, 0, -1)))
    while True:
        pos = next(scan_sequence)
        bar = ['─'] * length
        bar[pos] = '█'
        yield f"<{color}>{{text}} [{''.join(bar)}]</>"