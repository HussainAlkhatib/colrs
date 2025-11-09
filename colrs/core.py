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
    # This regex finds the *innermost* tag, which is a tag that contains no other tags.
    # This is the key to correctly processing nested tags from the inside out.
    innermost_tag_regex = r"<([a-zA-Z0-9_,]+)>([^<>]*?)(?:</>|</\1>)"
    
    # Keep processing the innermost tags until no tags are left.
    while re.search(innermost_tag_regex, text):
        text = re.sub(innermost_tag_regex, _color_tag_replacer, text)

    # After all tags are resolved, apply the base color to the entire string.
    return colorize(text, color, bg_color)

def _color_tag_replacer(match) -> str:
    """Internal helper for re.sub to replace a matched tag with colored text."""
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

def _strip_all_tags(text: str) -> str:
    """Strips all tags (color and action) for length calculation."""
    # First, handle the complex tags like <green>text</>
    text = re.sub(r"<([a-zA-Z0-9_,=]+)>((?:.|\n)*?)(?:</>|</\1>)", r"\2", text)
    # Then, handle any remaining simple tags
    text = re.sub(r"<[^>]+>", "", text)
    return text

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
