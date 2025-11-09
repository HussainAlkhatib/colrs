# colorara/colrs/tables.py

from .magic import _magic_print
import re

def _strip_tags(text: str) -> str:
    """Removes color tags from a string to calculate its real length."""
    return re.sub(r"<[^>]+>", '', str(text))

def table(headers: list, data: list[list], border_color: str = "white", header_color: str = None, to_string: bool = False):
    """
    Prints a formatted, color-aware table to the console.

    The function automatically calculates column widths and supports inline
    color tags within the data cells.

    :param headers: A list of strings for the table headers.
    :param data: A list of lists, where each inner list represents a row.
    :param border_color: The color for the table's border.
    :param header_color: The color for the header text (e.g., "white,bg_blue").
    :param to_string: If True, returns the table as a string instead of printing it.
    """
    if not headers:
        return "" if to_string else None

    # Calculate column widths based on the longest item in each column (header or data)
    num_columns = len(headers)
    col_widths = [len(_strip_tags(h)) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            if i < num_columns:
                col_widths[i] = max(col_widths[i], len(_strip_tags(cell)))

    output_lines = []

    # --- Drawing functions ---
    def _draw_separator(char_left, char_mid, char_right):
        parts = [char_left]
        for width in col_widths:
            parts.append('─' * (width + 2))
        separator = char_mid.join(parts) + char_right
        output_lines.append(f"<{border_color}>{separator}</>")

    def _draw_row(row_data, is_header=False):
        parts = [f"<{border_color}>│</>"]
        for i, cell in enumerate(row_data):
            clean_cell_len = len(_strip_tags(cell))
            padding = ' ' * (col_widths[i] - clean_cell_len)

            if is_header and header_color:
                # The closing tag for header should be specific to avoid breaking nested tags
                cell_content = f" <{header_color}>{cell}{padding}</> "
            else:
                cell_content = f" {cell}{padding} "
            parts.append(cell_content)

        row_str = f"<{border_color}>│</>{f'<{border_color}>│</>'.join(parts)}"
        output_lines.append(row_str)

    # --- Build the table ---
    _draw_separator('┌', '┬', '┐')
    _draw_row(headers, is_header=True)
    _draw_separator('├', '┼', '┤')
    for row in data:
        _draw_row(row)
    _draw_separator('└', '┴', '┘')

    final_output = "\n".join(output_lines)
    if to_string:
        return final_output
    else:
        _magic_print(final_output)