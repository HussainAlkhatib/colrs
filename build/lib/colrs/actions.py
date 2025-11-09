# colorara/colrs/actions.py

import sys
import re
import threading
from contextlib import contextmanager

from .menus import get_key, hide_cursor, show_cursor
from .core import _process_text_for_printing, _strip_all_tags

def _enable_mouse_tracking():
    """Enables mouse tracking in the terminal."""
    sys.stdout.write('\033[?1003h\033[?1000h')
    sys.stdout.flush()

def _disable_mouse_tracking():
    """Disables mouse tracking."""
    sys.stdout.write('\033[?1003l\033[?1000l')
    sys.stdout.flush()

class ActionTagManager:
    """
    A context manager to handle interactive action tags in the terminal.
    """
    def __init__(self, actions: dict, initial_text: str = ""):
        self.actions = actions
        self.text = initial_text
        self._action_map = []
        self._stop_event = threading.Event()
        self._thread = None
        self.feedback = ""

    def update(self, new_text: str):
        """Updates the text to be displayed."""
        self.text = new_text
        self._render()

    def _render(self):
        """Renders the text and maps out action tag coordinates."""
        self._action_map.clear()
        
        # Process colors first, but keep action tags
        processed_text = _process_text_for_printing(self.text)
        
        # Regex to find action tags and their content
        action_regex = r"<action=([a-zA-Z0-9_]+)>((?:.|\n)*?)(?:</>|</action=\1>)"
        
        # We need to find the coordinates of each action
        # This is a simplified approach. A real implementation would need a more robust layout engine.
        # Let's assume single-line for now.
        
        # Print the text and store coordinates
        current_pos = 0
        last_end = 0
        
        # Clear screen and move to home
        sys.stdout.write("\033[H\033[J")
        
        for match in re.finditer(action_regex, processed_text):
            action_name = match.group(1)
            content = match.group(2)
            
            # Print text before the match
            pre_text = processed_text[last_end:match.start()]
            sys.stdout.write(pre_text)
            current_pos += len(_strip_all_tags(pre_text))
            
            # Store action coordinates
            start_pos = current_pos + 1
            end_pos = start_pos + len(_strip_all_tags(content))
            self._action_map.append((start_pos, end_pos, action_name))
            
            # Print the action content (e.g., underlined)
            sys.stdout.write(f"\033[4m{content}\033[0m")
            current_pos = end_pos
            
            last_end = match.end()

        # Print remaining text
        sys.stdout.write(processed_text[last_end:])
        sys.stdout.flush()

    def _listen(self):
        """Listens for mouse events in a separate thread."""
        while not self._stop_event.is_set():
            key = get_key() # Re-using get_key for simplicity, needs enhancement for mouse
            # This is a placeholder for real mouse event parsing, which is very complex.
            # A real implementation would parse ANSI mouse codes like `\x1b[<0;col;row;M`
            # For now, we'll simulate it with a key press.
            if key == b'c': # Simulate a click
                # In a real scenario, we'd get x, y from the mouse event
                # Here we just trigger the first action as a demo
                if self._action_map:
                    _, _, action_name = self._action_map[0]
                    if action_name in self.actions:
                        result = self.actionsaction_name
                        self.feedback = str(result)
                        # Re-render to show feedback if needed (outside this simple loop)

    def __enter__(self):
        hide_cursor()
        # _enable_mouse_tracking() # Disabled for now as parsing is complex
        self._render()
        # self._thread = threading.Thread(target=self._listen, daemon=True)
        # self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self._stop_event.set()
        # if self._thread:
        #     self._thread.join()
        # _disable_mouse_tracking()
        show_cursor()
        print("\n") # New line after exit