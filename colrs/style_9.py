# style_9.py: Random Blocks
import random
import itertools

def run(text, color):
    """Fills a bar with random blocks."""
    length = 25
    # Create a list of positions to fill, then shuffle it
    positions = list(range(length))
    random.shuffle(positions)
    blocks = [' '] * length
    for pos in itertools.cycle(positions):
        blocks[pos] = '█'
        yield f"<{color}>{{text}} [{''.join(blocks)}]</>"