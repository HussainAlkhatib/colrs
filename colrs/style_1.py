# style_1.py: Progress Bar
import itertools

def run(text, color):
    """Displays a dynamic, multi-colored progress bar."""
    length = 40
    # This style is time-based, so it will just cycle indefinitely.
    # The controlling 'loading' function is responsible for stopping it.
    for i in itertools.cycle(range(length + 1)):
        progress = i / length
        filled = '█' * i
        empty = '─' * (length - i)
        bar_color = "green" if progress > 0.8 else "yellow" if progress > 0.4 else "red"
        yield f"<white>{{text}}</> <{bar_color}>[{filled}{empty}]</> {int(progress*100)}%"