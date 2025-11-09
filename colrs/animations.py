# colorara/colrs/animations.py

import time
import importlib
import sys
import threading
from contextlib import contextmanager
from typing import Optional, Generator, Any

class _Loader:
    """Internal class to manage the animation thread."""
    def __init__(self, style, text, color):
        self._text = text
        self._style_module = importlib.import_module(f'.style_{style}', package='colrs')
        self._color = color
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._stop_event = threading.Event()

    def _animate(self):
        """The main animation loop, run in a separate thread."""
        try:
            # The run function of styles now becomes a generator
            animation_generator = self._style_module.run(text=self._text, color=self._color)
            while not self._stop_event.is_set():
                frame = next(animation_generator)
                # We need to dynamically get the current text
                current_text = getattr(self._style_module.run, 'text', self._text)
                print(frame.replace("{text}", current_text), end='\r', flush=True)
                time.sleep(0.1) # Generic sleep, can be overridden by style
        except StopIteration:
            pass # Generator finished

    def update(self, text: str):
        """Updates the text displayed next to the animation."""
        # We need to re-create the generator with the new text
        self._style_module.run.text = text # A bit of a hack, but works for simple updates

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

def _run_fixed_duration_loading(style, duration, text, color, bf_text, af_text, end_color):
    """Internal function to handle fixed-duration loading."""
    if bf_text:
        print(bf_text)
    
    loader = _Loader(style=style, text=text, color=color)
    loader.start()
    try:
        time.sleep(duration)
    finally:
        loader.stop()
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        if af_text:
            print(f"<{end_color}>{af_text}</>")

@contextmanager
def _loading_context_manager(style, text, color, af_text, end_color) -> Generator[Any, Any, None]:
    """Internal context manager for indefinite-duration loading."""
    loader = _Loader(style=style, text=text, color=color)
    loader.start()
    try:
        yield loader
    finally:
        loader.stop()
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        if af_text:
            print(f"<{end_color}>{af_text}</>")

def loading(style: int = 1, duration: Optional[float] = None, text: str = "Loading...", color: str = "yellow", bf_text: Optional[str] = None, af_text: str = "Done!", end_color: str = "green"):
    """
    Displays a loading animation. Acts as a blocking function if `duration` is
    provided, or as a context manager (`with` statement) if not.
    """
    if duration is not None:
        # Blocking mode for a fixed duration
        try:
            _run_fixed_duration_loading(style, duration, text, color, bf_text, af_text, end_color)
        except ImportError:
            print(f"<red>Error: Loader style '{style}' not found.</red>")
        except Exception as e:
            sys.stdout.write('\r' + ' ' * 80 + '\r')
            print(f"<red>An error occurred during animation: {e}</red>")
    else:
        # Context manager mode for indefinite duration
        # We return the context manager itself to be used in the `with` statement.
        return _loading_context_manager(style, text, color, af_text, end_color)


def loading_legacy(style=1, duration=3, text="Loading...", color="yellow", bf_text=None, af_text="Done!", end_color="green"):
    """
    Displays a loading animation for tasks of unknown duration.
    Use as a context manager (`with` statement).

    :param style: The style of the loader to display.
    :param text: The initial text to display.
    :param color: The primary color of the animation.
    :param af_text: Text to display upon completion.
    :param end_color: The color of the completion text.
    """