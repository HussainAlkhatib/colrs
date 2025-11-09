# colorara/colrs/async_tools.py

import asyncio
import sys
import importlib
from contextlib import asynccontextmanager
from io import StringIO

from .core import _process_text_for_printing
from .menus import hide_cursor, show_cursor, move_up

# --- Async Loading ---

class _AsyncLoader:
    """Internal class to manage the async animation task."""
    def __init__(self, style, text, color):
        self._text = text
        self._style_module = importlib.import_module(f'.style_{style}', package='colrs')
        self._color = color
        self._task = None
        self._stop_event = asyncio.Event()

    async def _animate(self):
        animation_generator = self._style_module.run(text=self._text, color=self._color)
        while not self._stop_event.is_set():
            try:
                frame = next(animation_generator)
                current_text = getattr(self._style_module.run, 'text', self._text)
                print(frame.replace("{text}", current_text), end='\r', flush=True)
                await asyncio.sleep(0.1)
            except StopIteration:
                break

    def update(self, text: str):
        self._style_module.run.text = text

    def start(self):
        self._task = asyncio.create_task(self._animate())

    async def stop(self):
        self._stop_event.set()
        if self._task:
            await self._task

@asynccontextmanager
async def async_loading(style=1, text="Loading...", color="yellow", af_text="Done!", end_color="green"):
    """An async context manager for loading animations."""
    loader = _AsyncLoader(style=style, text=text, color=color)
    loader.start()
    try:
        yield loader
    finally:
        await loader.stop()
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        if af_text:
            print(f"<{end_color}>{af_text}</>")


# --- Async Live ---

class AsyncLive:
    """An async context manager for live-updating displays."""
    def __init__(self, initial_content="", refresh_rate: float = 0.1):
        self._content_generator = initial_content
        self._lines_rendered = 0
        self._stop_event = asyncio.Event()
        self._task = None
        self._lock = asyncio.Lock()
        self._refresh_rate = refresh_rate

    async def _render_loop(self):
        while not self._stop_event.is_set():
            await self._render_content()
            await asyncio.sleep(self._refresh_rate)

    async def _render_content(self):
        async with self._lock:
            if self._lines_rendered > 0:
                move_up(self._lines_rendered)

            buffer = StringIO()
            content_to_render = self._content_generator() if callable(self._content_generator) else self._content_generator
            processed_content = _process_text_for_printing(content_to_render)
            buffer.write(processed_content)
            
            output = buffer.getvalue()
            sys.stdout.write("\033[J")
            sys.stdout.write(output)
            sys.stdout.flush()
            self._lines_rendered = output.count('\n') + 1

    def update(self, content_generator):
        # This update is synchronous, the loop will pick it up asynchronously
        self._content_generator = content_generator

    async def __aenter__(self):
        hide_cursor()
        self._task = asyncio.create_task(self._render_loop())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        if self._task:
            await self._task
        
        await self._render_content()
        
        sys.stdout.write('\n')
        show_cursor()