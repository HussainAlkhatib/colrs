# colorara/colrs/actions.py

import sys
import re
import threading
from contextlib import contextmanager

from .menus import get_key, hide_cursor, show_cursor
from .core import _process_text_for_printing, _strip_all_tags
from .theme import get_theme

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
        self.theme = get_theme()
        self.actions = actions
        self.text = initial_text
        self._action_map = {} # Using a dict: {(x, y): action_name}
        self._stop_event = threading.Event() # To safely stop the listener thread
        self._thread = None
        self.feedback = ""

    def update(self, new_text: str):
        """Updates the text to be displayed."""
        self.text = new_text
        self._render()

    def _render(self):
        """Renders the text and maps out action tag coordinates."""
        from .menus import move_up
        
        self._action_map.clear()
        sys.stdout.write("\033[H\033[J") # Clear screen and move to home
        
        # We need to manually walk through the text to calculate coordinates
        # because print() doesn't return cursor position.
        x, y = 0, 0
        action_regex = r"<action=([a-zA-Z0-9_]+)>((?:.|\n)*?)(?:</>|</action=\1>)"
        last_end = 0
        
        # First, replace action tags with a special, colored version
        accent_color = self.theme.get("accent", "magenta")
        def action_replacer(match):
            # Replace <action=foo>bar</> with <accent,underline>bar</>
            return f"<{accent_color},underline>{match.group(2)}</>"
            
        display_text = re.sub(action_regex, action_replacer, self.text)
        processed_text = _process_text_for_printing(display_text)

        # Now, find the coordinates of the original action tags
        for match in re.finditer(action_regex, self.text):
            action_name = match.group(1)
            content = match.group(2)
            
            # Calculate the position of the action tag
            pre_text_len = len(_strip_all_tags(self.text[last_end:match.start()]))
            x += pre_text_len
            
            content_len = len(_strip_all_tags(content))
            for i in range(content_len):
                self._action_map[(x + i, y)] = action_name
            
            x += content_len
            last_end = match.end()

        # Finally, print the fully processed text
        sys.stdout.write(processed_text)
        sys.stdout.flush()

    def _listen(self):
        """Listens for mouse events in a separate thread."""
        while not self._stop_event.is_set():
            # Read a sequence of bytes from stdin
            # Mouse click: \x1b[<0;col;row;M
            char = sys.stdin.read(1)
            if char == '\x1b':
                seq = sys.stdin.read(1)
                if seq == '[':
                    mouse_seq = sys.stdin.read(6)
                    try:
                        # Check for mouse click event
                        if mouse_seq.endswith('M'):
                            parts = mouse_seq.strip('<M').split(';')
                            # event_type = int(parts[0])
                            col = int(parts[1]) - 1 # Terminal columns are 1-based
                            row = int(parts[2]) - 1 # Terminal rows are 1-based
                            
                            # Check if the click was on an action
                            if (col, row) in self._action_map:
                                action_name = self._action_map[(col, row)]
                                if action_name in self.actions:
                                    # Execute the action
                                    result = self.actionsaction_name
                                    self.update(str(result)) # Re-render with the result
                    except (ValueError, IndexError):
                        # Not a valid mouse sequence we can parse
                        pass

    def __enter__(self):
        hide_cursor()
        _enable_mouse_tracking()
        self._render()
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=0.2)
        _disable_mouse_tracking()
        show_cursor()
        print("\n") # New line after exit