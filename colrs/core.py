# colorara/colorara/core.py

import builtins
import re

# ANSI escape codes
COLORS = {
    "black": "\033[30m",
    "grey": "\033[90m", # Added grey
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
        
    # If the text already contains ANSI codes, we need to be smart.
    # We replace the reset code with a "reset then re-apply current color" code.
    # This ensures that nested colors correctly return to their parent color.
    if (color or bg_color) and COLORS['reset'] in text:
        reapply_code = f"{BG_COLORS.get(str(bg_color).lower(), '')}{COLORS.get(str(color).lower(), '')}"
        return text.replace(COLORS['reset'], f'{COLORS["reset"]}{reapply_code}')

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
    # This regex finds the *first* top-level tag. The non-greedy `.*?` is crucial.
    tag_regex = r"<([a-zA-Z0-9_,]+)>((?:.|\n)*?)(?:</>|</\1>)"
    
    match = re.search(tag_regex, text)
    
    # If no tags are found in the text, just colorize the whole thing and return.
    if not match:
        return colorize(text, color, bg_color)

    # If tags are found, we build the string piece by piece.
    parts = []
    
    # 1. Process the part of the string *before* the first tag.
    # This part inherits the base color.
    pre_match_text = text[:match.start()]
    parts.append(colorize(pre_match_text, color, bg_color))
    
    # 2. Process the content *inside* the tag.
    # This is the recursive step. The content of the tag is processed,
    # and the tag's color becomes the new base color for that content.
    tag_content = match.group(2)
    tags = match.group(1).lower().split(',')
    tag_color = next((t for t in tags if not t.startswith('bg_')), None)
    tag_bg_color = next((t[3:] for t in tags if t.startswith('bg_')), None)
    
    # The crucial change: The inner content is processed, and then the result
    # is colored by the *outer* color. This ensures the parent color "wraps"
    # the child color correctly.
    inner_processed = _process_text_for_printing(tag_content, tag_color, tag_bg_color)
    parts.append(colorize(inner_processed, color, bg_color))

    # 3. Process the part of the string *after* the tag.
    # This part also inherits the original base color.
    parts.append(_process_text_for_printing(text[match.end():], color, bg_color))
    
    return "".join(parts)
def _strip_all_tags(text: str) -> str:
    """Strips all tags (color and action) for length calculation."""
    # A simple regex to remove all tags for length calculation.
    return re.sub(r"<[^>]+>", "", text)

def _find_actions(text: str) -> list[tuple[str, str]]:
    """Finds all action tags and their content in a string."""
    action_regex = r"<action=([a-zA-Z0-9_]+)>((?:.|\n)*?)(?:</>|</action=\1>)"
    return re.findall(action_regex, text)


def cprint(*args, color: str = None, bg_color: str = None, **kwargs):
    """
    A safe wrapper around the built-in print function that adds color,
    supporting both overall coloring and inline color tags.
    
    e.g. cprint("Status: <green>OK</>")
    """
    text = " ".join(map(str, args))
    processed_text = _process_text_for_printing(text, color, bg_color)
    builtins.print(processed_text, **kwargs)
