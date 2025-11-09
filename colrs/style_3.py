# style_3.py: Bouncing Dots

def run(text, color):
    """Displays a bouncing dots animation."""
    while True:
        for i in range(4):
            dots = '.' * i + ' ' * (3 - i)
            yield f"<{color}>{{text}}{dots}</>"