# colorara/colrs/logger.py

import logging
from .magic import _magic_print

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

    def emit(self, record):
        """
        Overrides the default emit to use our color-processing print function.
        """
        try:
            msg = self.format(record)
            _magic_print(msg, end=self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

    def format(self, record):
        message = super().format(record)
        
        level_color = self.level_colors.get(record.levelno)
        
        if level_color:
            message = f"<{level_color}>{message}</>"
        
        return message