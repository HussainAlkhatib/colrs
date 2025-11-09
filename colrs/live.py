# colorara/colrs/live.py

import sys
import threading
import time
from io import StringIO

from .core import _process_text_for_printing
from .menus import hide_cursor, show_cursor, move_up

class Live:
    """
    A context manager for creating a live-updating display area in the terminal.
    
    Use it with a `with` statement. The object yielded can be updated with new
    content, which will be automatically re-rendered in place.
    """
    def __init__(self, initial_content="", refresh_rate: float = 0.1):
        self._content_generator = lambda: initial_content
        self._lines_rendered = 0
        self._stop_event = threading.Event()
        self._thread = None
        self._lock = threading.Lock()
        self._refresh_rate = refresh_rate

    def _render_loop(self):
        """The main rendering loop, run in a separate thread."""
        while not self._stop_event.is_set():
            self._render_content()
            time.sleep(self._refresh_rate)

    def _render_content(self):
        """Renders the current content to the terminal."""
        with self._lock:
            # Move cursor up to the beginning of the last render
            if self._lines_rendered > 0:
                move_up(self._lines_rendered)

            # Use a StringIO buffer to capture the output and count lines
            buffer = StringIO()
            
            # Check if the generator is a callable function or just content
            if callable(self._content_generator):
                content_to_render = self._content_generator()
            else:
                content_to_render = self._content_generator
            # The _process_text_for_printing function is the core of colrs
            processed_content = _process_text_for_printing(content_to_render)
            buffer.write(processed_content)
            
            # Get the content and clear the old lines
            output = buffer.getvalue()
            # Clear screen from cursor down
            sys.stdout.write("\033[J")
            
            # Write the new content
            sys.stdout.write(output)
            sys.stdout.flush()

            # Update the number of lines for the next render
            self._lines_rendered = output.count('\n') + 1

    def update(self, content_generator):
        """
        Updates the content to be displayed.
        :param content_generator: A string or a callable (function) that returns the string to display.
        """
        with self._lock:
            self._content_generator = content_generator

    def __enter__(self):
        hide_cursor()
        self._thread = threading.Thread(target=self._render_loop, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        self._thread.join()
        
        # Do one final render to print the last state
        self._render_content()
        
        # Ensure the cursor is shown and on a new line
        sys.stdout.write('\n')
        show_cursor()