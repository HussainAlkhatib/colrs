# colorara/colrs/components.py

import sys
from .menus import get_key, hide_cursor, show_cursor, move_up, clear_line

def checkbox(
    title: str, 
    choices: list[str], 
    cursor_color: str = "cyan", 
    selected_color: str = "green",
    cursor: str = ">",
    checked_char: str = "✔",
    unchecked_char: str = " "
) -> list[str]:
    """
    Displays an interactive checkbox menu and returns a list of selected choices.
    
    - Use arrow keys (Up/Down) to navigate.
    - Use Spacebar to toggle a selection.
    - Use Enter to confirm.
    """
    selected_states = [False] * len(choices)
    current_index = 0
    
    hide_cursor()
    try:
        while True:
            # Print the title
            print(title)
            
            # Print the choices
            for i, choice in enumerate(choices):
                is_selected = selected_states[i]
                is_cursor_on = (i == current_index)

                # Determine prefix and color
                prefix = f"<{cursor_color}>{cursor}</> " if is_cursor_on else "  "
                check_box = f"[<{selected_color}>{checked_char if is_selected else unchecked_char}</>]"
                
                line = f"{prefix}{check_box} {choice}"
                print(line)

            # Wait for a key press
            key = get_key()

            # Handle key presses
            if key in [b'H', b'A']: # Up arrow
                current_index = (current_index - 1 + len(choices)) % len(choices)
            elif key in [b'P', b'B']: # Down arrow
                current_index = (current_index + 1) % len(choices)
            elif key == b' ': # Spacebar
                selected_states[current_index] = not selected_states[current_index]
            elif key == b'\r': # Enter key
                # Clear the menu from the screen
                move_up(len(choices) + 1)
                for _ in range(len(choices) + 1):
                    clear_line()
                    sys.stdout.write("\n")
                move_up(len(choices) + 1)
                
                # Return the selected items
                return [choices[i] for i, state in enumerate(selected_states) if state]
            elif key == b'\x03': # Ctrl+C
                raise KeyboardInterrupt

            # Move cursor up to overwrite the menu in the next loop
            move_up(len(choices) + 1)

    finally:
        show_cursor()