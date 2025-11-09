# colorara/colorara/__init__.py

"""
colrs - A simple and elegant way to color your terminal text.
"""

__version__ = "0.3"

# Initialize colorama to make ANSI codes work on Windows and to auto-reset colors.
from colorama import init
init(autoreset=True)

# The public API is now just act() and unact() for maximum simplicity.
from .magic import act, unact
from .animations import loading
from .tables import table
from .theme import set_theme, get_theme
from .panel import Panel
from .menus import menu
from .live import Live
from .logger import ColorizingStreamHandler
from .components import checkbox
from .layout import Layout
from .actions import ActionTagManager
from .async_tools import async_loading, AsyncLive
from .progress import progress

# --- Short Aliases for easier access ---
LogHandler = ColorizingStreamHandler
ActionManager = ActionTagManager
aloading = async_loading
aLive = AsyncLive
check = checkbox
prog = progress

# --- Super Short Aliases for power users ---
lo = loading
alo = async_loading
li = Live
ali = AsyncLive
me = menu
chk = checkbox
tb = table
pn = Panel
pr = progress
sth = set_theme
gth = get_theme
ly = Layout
lh = LogHandler
am = ActionManager

__all__ = [
    'act',
    'unact',
    'loading',
    'table',
    'set_theme',
    'get_theme',
    'menu',
    'Panel',
    'Live',
    'ColorizingStreamHandler',
    'checkbox',
    'Layout',
    'ActionTagManager',
    'async_loading',
    'AsyncLive',
    'progress',
    # Add aliases to __all__ so they can be imported
    'LogHandler', 'ActionManager', 'aloading', 'aLive', 'check', 'prog',
    # Add super short aliases to __all__
    'lo', 'alo', 'li', 'ali', 'me', 'chk', 'tb', 'pn', 'pr', 'sth', 'gth', 'ly', 'lh', 'am'
]
