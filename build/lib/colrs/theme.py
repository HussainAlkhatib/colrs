# colorara/colrs/theme.py

# The global theme dictionary
_current_theme = {
    "primary": "cyan",
    "secondary": "yellow",
    "accent": "magenta",
    "success": "green",
    "warning": "yellow",
    "error": "red",
    "border": "white",
    "panel_title_bg": "cyan",
    "panel_title_fg": "black",
    "menu_selected": "cyan",
    "checkbox_cursor": "cyan",
    "checkbox_selected": "green",
}

def set_theme(new_theme: dict):
    """Updates the global theme with new colors."""
    _current_theme.update(new_theme)

def get_theme() -> dict:
    """Returns the current theme dictionary."""
    return _current_theme