# colorara/colrs/layout.py

import os
import sys
import time
import threading
import asyncio
from contextlib import contextmanager

from .live import Live
from .core import _process_text_for_printing

class Layout:
    """
    A class that defines a layout structure for creating complex live displays.
    """
    def __init__(self, name: str = "root", ratio: int = 1, is_row: bool = False):
        self.name = name
        self.ratio = ratio
        self.is_row = is_row
        self.children = []
        self.parent = None
        self._content = ""

    def split_row(self, *layouts):
        """Splits the layout into rows."""
        self._split(True, *layouts)

    def split_column(self, *layouts):
        """Splits the layout into columns."""
        self._split(False, *layouts)

    def _split(self, is_row: bool, *layouts):
        self.is_row = is_row
        self.children = list(layouts)
        for child in self.children:
            child.parent = self

    def __getitem__(self, name: str):
        """Find a layout by name in the tree."""
        if self.name == name:
            return self
        for child in self.children:
            found = child[name]
            if found:
                return found
        return None

    def update(self, content: str):
        """Update the content of a leaf layout."""
        if self.children:
            raise TypeError("Cannot update a layout that has children. Update a leaf layout.")
        self._content = content

    def _render(self, x: int, y: int, width: int, height: int) -> str:
        """Recursively renders the layout into a string for final display."""
        total_ratio = sum(child.ratio for child in self.children) or 1
        
        output_map = {}

        if not self.children:
            # This is a leaf node, render its content
            processed_content = _process_text_for_printing(self._content)
            lines = processed_content.split('\n')
            for i, line in enumerate(lines):
                if i < height:
                    # Truncate line and add to map
                    output_map[(x, y + i)] = line[:width]
        else:
            # This is a container node, render its children
            offset = 0
            for child in self.children:
                if self.is_row:
                    child_height = (height * child.ratio) // total_ratio
                    child_map = child._render(x, y + offset, width, child_height)
                    output_map.update(child_map)
                    offset += child_height
                else: # is column
                    child_width = (width * child.ratio) // total_ratio
                    child_map = child._render(x + offset, y, child_width, height)
                    output_map.update(child_map)
                    offset += child_width
        
        return output_map

    @contextmanager
    def live(self, refresh_rate: float = 0.1):
        """A context manager to run the live display for the layout."""
        live_manager = _LiveLayoutManager(self, refresh_rate)
        try:
            live_manager.start()
            yield self # Yield the layout itself for updates
        finally:
            live_manager.stop()

    @contextmanager
    def async_live(self, refresh_rate: float = 0.1):
        """An async context manager to run the live display for the layout."""
        # This is a simplified placeholder. A full implementation would need an _AsyncLiveLayoutManager
        # For now, we'll just note that it's possible.
        print("<yellow>Async layout support is under development.</yellow>")
        # In a real implementation:
        # manager = _AsyncLiveLayoutManager(self, refresh_rate)
        yield self

class _LiveLayoutManager:
    """Manages the rendering thread for a Layout."""
    def __init__(self, layout: Layout, refresh_rate: float):
        self.layout = layout
        self.refresh_rate = refresh_rate
        self._stop_event = threading.Event()
        self._thread = None
        self._lines_rendered = 0

    def start(self):
        from .menus import hide_cursor
        hide_cursor()
        self._thread = threading.Thread(target=self._render_loop, daemon=True)
        self._thread.start()

    def stop(self):
        from .menus import show_cursor
        if self._thread:
            self._stop_event.set()
            self._thread.join()
        
        # Do a final render
        self._render_frame()
        sys.stdout.write('\n')
        show_cursor()

    def _render_loop(self):
        while not self._stop_event.is_set():
            self._render_frame()
            time.sleep(self.refresh_rate)

    def _render_frame(self):
        from .menus import move_up
        if self._lines_rendered > 0:
            move_up(self._lines_rendered)

        width, height = os.get_terminal_size()
        
        # Get a map of (x, y) -> line content
        content_map = self.layout._render(0, 0, width, height)
        
        # Clear the old content area
        sys.stdout.write("\033[J")

        # Build the final screen buffer
        screen_buffer = []
        max_y = 0
        if content_map:
            max_y = max(y for _, y in content_map.keys())

        for y in range(max_y + 1):
            line = ""
            # Find all segments for the current line and sort by x
            line_segments = sorted([(x_pos, content) for (x_pos, y_pos), content in content_map.items() if y_pos == y], key=lambda item: item[0])
            
            current_x = 0
            for x, content in line_segments:
                padding = " " * (x - current_x)
                line += padding + content
                current_x = x + len(content) # A simplification, doesn't account for ANSI codes in len
            screen_buffer.append(line)

        final_output = "\n".join(screen_buffer)
        sys.stdout.write(final_output)
        sys.stdout.flush()
        self._lines_rendered = final_output.count('\n') + 1