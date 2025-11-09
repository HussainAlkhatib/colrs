# colorara/colrs/logger.py

import logging

class ColorizingStreamHandler(logging.StreamHandler):
    """
    A logging handler that colorizes output based on log level.
    It automatically wraps log messages in color tags that are then
    processed by the patched `print` function.
    """
    def __init__(self, stream=None, level_colors=None):
        super().__init__(stream)
        
        default_colors = {
            logging.DEBUG: 'cyan',
            logging.INFO: 'green',
            logging.WARNING: 'yellow',
            logging.ERROR: 'red',
            logging.CRITICAL: 'white,bg_red',
        }
        
        if level_colors:
            default_colors.update(level_colors)
        
        self.level_colors = default_colors

    def format(self, record):
        # Get the formatted message from the base class formatter
        message = super().format(record)
        
        # Get the color for the current log level
        level_color = self.level_colors.get(record.levelno)
        
        # Wrap the entire message in the level's color tag
        if level_color:
            # We add the color tag, and our patched print() will handle it
            # The closing tag </ > is important to reset color for subsequent prints
            message = f"<{level_color}>{message}</>"
        
        return message