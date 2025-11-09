# colorara/colrs/menus.py

import sys

# --- Platform-specific key press reading ---
try:
    # Windows
    import msvcrt
    
    def get_key():
        key = msvcrt.getch()
        # Arrow keys on Windows are multi-byte: b'\xe0' + key
        if key == b'\xe0':
            return msvcrt.getch()
        return key

except ImportError:
    # Unix/Linux/macOS
    import tty
    import termios
    
    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            # Arrow keys on Unix are multi-byte: '\x1b' + '[' + key
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return ch3.encode()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.encode()

# --- ANSI escape codes for cursor control ---
def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def move_up(lines):
    sys.stdout.write(f"\033[{lines}F")
    sys.stdout.flush()

def clear_line():
    sys.stdout.write("\033[K")
    sys.stdout.flush()

def menu(title: str, choices: list[str], selected_color: str = None, selected_prefix: str = "> ", unselected_prefix: str = "  ") -> str:
    """
    Displays an interactive menu and returns the selected choice.
    The user can navigate with arrow keys and select with Enter.
    """
    from .theme import get_theme
    theme = get_theme()
    selected_color = selected_color or theme.get("menu_selected", "cyan")

    selected_index = 0
    
    hide_cursor()
    try:
        while True:
            # Print the title
            print(title)
            
            # Print the choices
            for i, choice in enumerate(choices):
                if i == selected_index:
                    print(f"<{selected_color}>{selected_prefix}{choice}</>")
                else:
                    print(f"{unselected_prefix}{choice}")
            
            # Wait for a key press
            key = get_key()

            # Handle key presses
            if key in [b'H', b'A']: # Up arrow (Windows 'H', Unix 'A')
                selected_index = (selected_index - 1 + len(choices)) % len(choices)
            elif key in [b'P', b'B']: # Down arrow (Windows 'P', Unix 'B')
                selected_index = (selected_index + 1) % len(choices)
            elif key == b'\r': # Enter key
                # Clear the menu from the screen before returning
                move_up(len(choices) + 1)
                for _ in range(len(choices) + 1):
                    clear_line()
                    print() # Move to next line to clear it
                move_up(len(choices) + 1)
                return choices[selected_index]
            elif key == b'\x03': # Ctrl+C
                raise KeyboardInterrupt

            # Move cursor up to overwrite the menu in the next loop
            move_up(len(choices) + 1)

    finally:
        show_cursor()