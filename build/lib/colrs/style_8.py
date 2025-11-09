# style_8.py: Arrow Flow
import itertools

def run(text, color):
    """Displays arrows moving to the right."""
    arrows = itertools.cycle(['>  ', '>> ', '>>>', ' >>', '  >'])
    while True:
        yield f"<{color}>{{text}} {next(arrows)}</>"