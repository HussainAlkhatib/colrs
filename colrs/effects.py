# colorara/colrs/effects.py

import sys
import time
from .magic import _magic_print
from .core import _process_text_for_printing, colorize, COLORS


NAMED_COLORS_RGB = {
    "black": (0, 0, 0), "red": (255, 0, 0), "green": (0, 255, 0),
    "yellow": (255, 255, 0), "blue": (0, 0, 255), "magenta": (255, 0, 255),
    "cyan": (0, 255, 255), "white": (255, 255, 255), "grey": (128, 128, 128)
}

def _color_to_rgb(color_str: str) -> tuple[int, int, int]:
    """Converts a color name or hex string to an RGB tuple."""
    color_str = color_str.lower()
    if color_str in NAMED_COLORS_RGB:
        return NAMED_COLORS_RGB[color_str]
    if color_str.startswith('#') and len(color_str) == 7:
        try:
            return tuple(int(color_str[i:i+2], 16) for i in (1, 3, 5))
        except ValueError:
            pass # Fallback to a default color
    return (255, 255, 255) # Default to white if color is unknown

def _rgb_to_truecolor_ansi(r: int, g: int, b: int) -> str:
    """Converts an RGB tuple to a TrueColor ANSI escape code for foreground."""
    return f"\033[38;2;{r};{g};{b}m"


def typewriter(text: str, speed: float = 0.05, color: str = None, bg_color: str = None):
    """
    Prints text with a typewriter effect.

    :param text: The text to print.
    :param speed: The delay between each character in seconds.
    :param color: The foreground color of the text.
    :param bg_color: The background color of the text.
    """
    # Process the entire string first to get the final colored string with ANSI codes
    processed_text = _process_text_for_printing(text, color, bg_color)

    # Iterate through the processed string. If a character is part of an ANSI code,
    # print the whole code at once. Otherwise, print the character and sleep.
    i = 0
    while i < len(processed_text):
        char = processed_text[i]
        # Check if this is the start of an ANSI escape code
        if char == '\033':
            # Find the end of the code (usually 'm')
            end_code_index = processed_text.find('m', i)
            if end_code_index != -1:
                # Print the entire ANSI code at once without sleeping
                code = processed_text[i:end_code_index+1]
                sys.stdout.write(code)
                i = end_code_index + 1 # Move index past the code
                continue # Skip the i += 1 at the end of the loop
            else:
                # Fallback for broken code
                sys.stdout.write(char)
        else:
            # If it's a normal character, print it and sleep
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        i += 1

    print() # Print a newline at the end

def gradient(text: str, start_color: str, end_color: str, speed: float = 0.05, duration: float = 5):
    """
    Prints text with a moving gradient effect for a specific duration.

    :param text: The text to animate.
    :param start_color: The starting color name (e.g., 'blue') or hex ('#0000FF').
    :param end_color: The ending color name or hex.
    :param speed: The delay between each frame in seconds.
    :param duration: The total time the effect should run in seconds.
    """
    start_rgb = _color_to_rgb(start_color)
    end_rgb = _color_to_rgb(end_color)
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # Calculate the progress of the animation (from 0 to 1 and back to 0)
        # This creates a smooth "ping-pong" effect
        elapsed = (time.time() - start_time)
        # Simple ping-pong logic: go from 0 to 1 in the first half, 1 to 0 in the second
        # We can use a sine wave for a smoother effect.
        import math
        progress = (math.sin(elapsed * (math.pi / (duration / 2))) + 1) / 2

        # Interpolate the color based on progress
        current_rgb = [
            int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * progress)
            for i in range(3)
        ]
        
        # Create the ANSI code for the current color
        color_code = _rgb_to_truecolor_ansi(*current_rgb)
        
        # Construct the frame
        frame_text = f"{color_code}{text}{COLORS['reset']}"
        
        sys.stdout.write('\r' + frame_text)
        sys.stdout.flush()
        
        time.sleep(speed)
        
    # Clear the line at the end
    sys.stdout.write('\r' + ' ' * len(text) + '\r')
    print() # Print a newline

def rainbow(text: str, speed: float = 0.1, duration: float = 5):
    """
    Prints text with a moving rainbow effect for a specific duration.

    :param text: The text to animate.
    :param speed: The delay between each frame in seconds.
    :param duration: The total time the effect should run in seconds.
    """
    rainbow_colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    num_colors = len(rainbow_colors)
    
    start_time = time.time()
    offset = 0
    
    while time.time() - start_time < duration:
        colored_parts = []
        for i, char in enumerate(text):
            # Don't color spaces to make it look cleaner
            if char == ' ':
                colored_parts.append(' ')
                continue
            
            # Calculate color based on character position and time offset
            color_index = (i + offset) % num_colors
            color = rainbow_colors[color_index]
            colored_parts.append(colorize(char, color))
        
        frame_text = "".join(colored_parts)
        sys.stdout.write('\r' + frame_text)
        sys.stdout.flush()
        offset += 1
        time.sleep(speed)
    
    print() # Print a newline at the end