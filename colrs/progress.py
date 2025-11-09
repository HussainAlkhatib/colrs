# colorara/colrs/progress.py

import time
import sys

from .core import _process_text_for_printing

def progress(
    sequence,
    description: str = "Working...",
    bar_length: int = 40,
    done_char: str = '█',
    remain_char: str = '─'
):
    """
    Wraps an iterable to display a progress bar.

    :param sequence: The iterable to process.
    :param description: Text to display before the progress bar.
    :param bar_length: The character width of the progress bar.
    :param done_char: The character for the completed part of the bar.
    :param remain_char: The character for the remaining part of the bar.
    """
    try:
        total = len(sequence)
    except TypeError:
        print("<red>Error: 'progress' requires an iterable with a defined length (e.g., a list or range).</red>")
        return

    start_time = time.time()

    for i, item in enumerate(sequence):
        yield item
        
        percent = (i + 1) / total
        filled_len = int(bar_length * percent)
        
        bar = done_char * filled_len + remain_char * (bar_length - filled_len)
        
        # Choose bar color based on progress
        bar_color = "green" if percent > 0.8 else "yellow" if percent > 0.4 else "cyan"
        
        # Construct the full string with all tags
        full_line = f'{description} <{bar_color}>[{bar}]</> {percent:.0%} '
        
        # Process the entire line for colors
        processed_line = _process_text_for_printing(full_line)
        
        sys.stdout.write(f'\r{processed_line}')
        sys.stdout.flush()
    
    sys.stdout.write('\n')