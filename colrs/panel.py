# colorara/colrs/panel.py

from .core import _strip_all_tags, _process_text_for_printing, cprint
from .theme import get_theme

def Panel(
    content: str,
    title: str = "",
    border_color: str = None,
    width: int = 0
):
    """
    Prints content inside a colored, formatted panel.

    :param content: The main text content to display inside the panel.
    :param title: An optional title to display on the top border.
    :param border_color: The color for the panel's border.
    :param width: The total width of the panel. If 0, it's calculated automatically.
    """
    theme = get_theme()
    border_color = border_color or theme.get("border", "white")

    # Process tags BEFORE splitting, because tags can span multiple lines!
    processed_content = _process_text_for_printing(content)
    lines = processed_content.split('\n')
    
    # Calculate width if not provided
    if width == 0:
        clean_title_len = len(_strip_all_tags(title))
        max_line_len = max(len(_strip_all_tags(line)) for line in lines) if lines else 0
        width = max(clean_title_len + 4, max_line_len + 4)

    # Top border with title
    if title:
        clean_title = _strip_all_tags(title)
        title_bar = f"┤ {_process_text_for_printing(title)} ├{'─' * (width - len(clean_title) - 6)}"
        cprint(f"<{border_color}>┌─{title_bar}┐</>")
    else:
        cprint(f"<{border_color}>┌{'─' * (width - 2)}┐</>")

    # Content lines
    for line in lines:
        clean_line_len = len(_strip_all_tags(line))
        padding = ' ' * max(0, width - clean_line_len - 4)
        cprint(f"<{border_color}>│</> {line}{padding} <{border_color}>│</>")

    # Bottom border
    cprint(f"<{border_color}>└{'─' * (width - 2)}┘</>")