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
    # Regex to find color tags like <green>text</green> or <white,bg_blue>text</>
    # It matches the opening tag, the content, and a closing tag which is either </> or a matching tag.
    tag_regex = r"<([a-zA-Z0-9_,]+)>((?:.|\n)*?)(?:</>|</\1>)"
    # Regex for action tags specifically
    action_tag_regex = r"<action=([a-zA-Z0-9_]+)>"

    # A simpler check to see if tags might be present.
    # This avoids running regex on every single string.
    if "<" not in text:
        return colorize(text, color, bg_color)

    # This replacer handles standard color tags
    def color_replacer(match):
        tags = match.group(1).lower().split(',')
        inner_text = match.group(2)
        
        tag_color = None
        tag_bg_color = None
        
        for tag in tags:
            # Ignore action tags in this replacer
            if tag.startswith('action='):
                return match.group(0) # Return the original tag unchanged

            if tag.startswith('bg_'):
                tag_bg_color = tag[3:]
            else:
                tag_color = tag
                
        return colorize(inner_text, tag_color, tag_bg_color)

    # Apply default color to the whole string first, then parse tags
    # This is complex. Let's just color the untagged parts.
    # A simpler approach for now: tags override the main color.    
    return re.sub(tag_regex, color_replacer, text)

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
