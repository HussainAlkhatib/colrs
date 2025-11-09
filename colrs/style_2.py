# style_2.py: Spinner
import itertools

def run(text, color):
    """Displays a simple spinning line animation."""
    spinner = itertools.cycle(['|', '/', '—', '\\'])
    while True:
        char = next(spinner)
        yield f"<{color}>{{text}} {char}</>"