# colorara/colorara/core.py

import builtins
import re

# ANSI escape codes
COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
}

BG_COLORS = {
    "black": "\033[40m",
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m",
}

def colorize(text: str, color: str = None, bg_color: str = None) -> str:
    """
    Wraps text with ANSI color codes.
    """
    if not isinstance(text, str):
        text = str(text)
        
    color_code = COLORS.get(str(color).lower()) if color else ""
    bg_color_code = BG_COLORS.get(str(bg_color).lower()) if bg_color else ""

    if color_code or bg_color_code:
        return f"{bg_color_code}{color_code}{text}{COLORS['reset']}"
    
    return text

def _process_text_for_printing(text: str, color: str = None, bg_color: str = None) -> str:
    """
    Processes a string for printing, handling both inline color tags and
    overall coloring. If tags are found, they take precedence.
    """
    # Regex to find color tags like <green> or <white,bg_blue>
    tag_regex = r"<([a-zA-Z0-9_,]+)>(.*?)</>"

    if "<" not in text and "</>" not in text:
        return colorize(text, color, bg_color)

    def replacer(match):
        tags = match.group(1).lower().split(',')
        inner_text = match.group(2)
        
        tag_color = None
        tag_bg_color = None
        
        for tag in tags:
            if tag.startswith('bg_'):
                tag_bg_color = tag[3:]
            else:
                tag_color = tag
                
        return colorize(inner_text, tag_color, tag_bg_color)

    # Apply default color to the whole string first, then parse tags
    # This is complex. Let's just color the untagged parts.
    # A simpler approach for now: tags override the main color.
    return re.sub(tag_regex, replacer, text)


def cprint(*args, color: str = None, bg_color: str = None, **kwargs):
    """
    A safe wrapper around the built-in print function that adds color,
    supporting both overall coloring and inline color tags.
    
    e.g. cprint("Status: <green>OK</>")
    """
    text = " ".join(map(str, args))
    processed_text = _process_text_for_printing(text, color, bg_color)
    builtins.print(processed_text, **kwargs)

def _get_colored_input_prompt(prompt: str, color: str, bg_color: str, inp_color: str) -> str:
    """
    Internal helper to construct the final prompt string for input,
    handling both prompt color and user input color.
    """
    # If inp_color is not given, it defaults to the prompt's text color
    effective_inp_color = inp_color if inp_color is not None else color

    # Color the prompt part (which includes a reset)
    colored_prompt = colorize(prompt, color, bg_color)

    # Get the color code for the user's input, or an empty string if no color
    input_color_code = COLORS.get(str(effective_inp_color).lower(), "") if effective_inp_color else ""
    
    # The final prompt string sets the color for the user's typing
    return colored_prompt + input_color_code

def cinput(prompt: str = "", color: str = None, bg_color: str = None, inp_color: str = None) -> str:
    """
    A safe wrapper around the built-in input function that adds color to the
    prompt and optionally to the user's typed input.

    :param prompt: The prompt string to display.
    :param color: The color of the prompt string.
    :param bg_color: The background color of the prompt string.
    :param inp_color: The color of the user's typed text. If None, defaults to `color`.
    """
    final_prompt = _get_colored_input_prompt(prompt, color, bg_color, inp_color)
    return builtins.input(final_prompt)
