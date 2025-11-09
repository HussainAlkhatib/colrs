# style_7.py: Gradient Wave

def run(text, color):
    """Displays a wave of characters with changing intensity."""
    chars = " ▂▃▄▅▆▇█▇▆▅▄▃▂ "
    i = 0
    while True:
        offset = i % len(chars)
        wave = "".join([chars[(i + offset) % len(chars)] for i in range(15)])
        yield f"<{color}>{{text}} {wave}</>"
        i += 1