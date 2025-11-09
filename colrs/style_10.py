# style_10.py: Pac-Man
import itertools

def run(text, color):
    """Displays a Pac-Man style animation."""
    pacman = itertools.cycle(['<', 'V', '>', '^'])
    dots = " · " * 5
    while True:
        yield f"<yellow>{next(pacman)}</> <white>{{text}}</> <{color}>{dots}</>"