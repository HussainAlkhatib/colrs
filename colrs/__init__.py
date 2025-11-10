# colorara/colrs/__init__.py

"""
colrs - A simple and elegant way to color your terminal text.
"""

__version__ = "0.4"

# Initialize colorama to make ANSI codes work on Windows and to auto-reset colors.
from colorama import init
init(autoreset=False)

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
from .async_tools import async_loading, AsyncLive
from .progress import progress
from . import effects


# --- Short Aliases for easier access ---
LogHandler = ColorizingStreamHandler
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
lh = LogHandler
ef = effects

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
    'async_loading',
    'AsyncLive',
    'progress',
    'effects',
    # Add aliases to __all__ so they can be imported
    'LogHandler', 'aloading', 'aLive', 'check', 'prog',
    # Add super short aliases to __all__
    'lo', 'alo', 'li', 'ali', 'me', 'chk', 'tb', 'pn', 'pr', 'sth', 'gth', 'lh', 'ef'
]
