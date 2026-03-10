# colrs - The Ultimate Python Library for Rich CLI Interfaces

`colrs` is a powerful, intuitive, and highly elegant Python library expressly architected for creating exceptionally beautiful and interactive command-line interfaces. It completely transforms your static terminal output from a simple text display into a fully-fledged, rich, dynamic application canvas.

Forget the days of juggling messy, cryptic ANSI escape codes. Forget wrapping every single print function in complex nested calls. `colrs` offers a high-level, component-based methodology centered entirely around a unique global activation model and semantic XML-like string tags. 

Whether you are building a simple CLI utility that needs some color, an interactive installation wizard requiring menus and checkboxes, or a massive live-updating split-screen dashboard monitoring complex server states, `colrs` remains robust, elegant, and entirely non-intrusive.

---

## The Core Philosophy: `act()` and `unact()`

The fundamental architecture of `colrs` centers around its global activation paradigm. To maintain the cleanest possible codebase, instead of requiring you to import specific `cprint` functions or wrap your strings in modifier objects, `colrs` temporarily hooks into your environment.

When you call `act()`, the library intelligently and silently monkey-patches Python's built-in `print()` and `input()` functions. Once activated, any standard `print("...")` statement instantly gains super-powers, capable of parsing and rendering inline HTML-like tags (e.g., `<green>Success</green>`). 

When your stylized output is complete, or if you wish to enforce standard output temporarily, simply call `unact()`. The environment is instantly restored to Python's original, default behavior with zero side effects.

```python
from colrs import act, unact

# Standard behavior
print("This is a normal print statement. Nothing magical happens here.")

# Activate the styler globally
act()
print("This print statement is now <cyan,bold>super-powered</cyan>!")

name = input("Identify yourself: ", color="yellow", inp_color="magenta")
print(f"System access granted to <bold>{name}</bold>.")

# Disable the styler globally
unact()
print("And we have cleanly returned to standard Python output.")
```

## Global Installation

Install the library securely and swiftly via PyPI. Note that `colrs` relies inherently on `colorama` for cross-platform (especially Windows) color terminal support.

```bash
pip install colrs
```

---

## Exhaustive Feature Documentation

This section provides an extremely deep dive into every single module, class, and component provided by `colrs`. The library is vast, covering everything from simple string styling to complex, asynchronous live layouts. Read through the examples to fully grasp the capabilities of your terminal.

---

### 1. The Core Engine: Semantic Tags and Nested Styling

Once `act()` is executed, the `print()` function becomes a rendering engine. You define styles by wrapping text in intuitive XML-like tags. 

**Coloring Syntax:** 
Use the tag format `<color>text</color>` or `<color>text</>`. The `</>` shorthand intelligently closes the most recently opened styling tag.

**Supported Foreground Colors:**
`black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, `lightblack_ex`, `lightred_ex`, `lightgreen_ex`, `lightyellow_ex`, `lightblue_ex`, `lightmagenta_ex`, `lightcyan_ex`, `lightwhite_ex`.

**Supported Background Colors:**
Prefix any standard color with `bg_`.
`bg_black`, `bg_red`, `bg_green`, `bg_yellow`, `bg_blue`, `bg_magenta`, `bg_cyan`, `bg_white`, `bg_lightblack_ex`, `bg_lightred_ex`, `bg_lightgreen_ex`, `bg_lightyellow_ex`, `bg_lightblue_ex`, `bg_lightmagenta_ex`, `bg_lightcyan_ex`, `bg_lightwhite_ex`.

**Styles:**
`dim`, `normal`, `bright` (or `bold`).

**Composing Styles:**
You can combine a foreground, a background, and a style within a single tag by separating them with commas.

```python
from colrs import act

act()

# Basic coloring
print("The primary database is <green>online</green>.")

# Using shorthand closer
print("The secondary database is <red>offline</>.")

# Combining attributes (Foreground, Background, Style)
print("<white,bg_red,bold> CRITICAL ERROR </> System meltdown imminent.")
```

**Intelligent Tag Nesting:**
`colrs` handles complex tag nesting flawlessly. When an inner tag closes, the engine seamlessly reverts the styling back to the exact state of the parent tag, preventing style leakage.

```python
from colrs import act

act()

# The word "Warning:" and everything after the inner tag is yellow.
# The inner text "database authentication service" temporarily shifts to blue.
print("<yellow>Warning: The <blue>database authentication service</blue> has failed to respond.</yellow>")
```

---

### 2. Smart User Interactivity: Advanced `input()`

Standard `input()` simply grabs strings. `colrs` elevates `input()` to allow distinct styling between your system's prompt, the text the user actually types, and instant visual validation based on what they typed using `color_rules`.

```python
from colrs import act

act()

# The prompt asks the user a question in cyan.
# As the user types their answer, the text they type appears in bright magenta.
# The 'yes'/'no' attributes act as dynamic color rules.
# If they specifically type "yes", it instantly recolors their typed text to red on a white background.
# If they type "no", it turns green.
choice = input(
    "Are you absolutely certain you wish to format the drive? (yes/no): ",
    color="cyan",          
    inp_color="lightmagenta_ex",     
    yes="red,bg_white",    
    no="green"             
)

print(f"Action logged: {choice}")
```

---

### 3. Structured Data: Auto-Resizing Panels

When you need to draw specific attention to a block of text---like a success message, a configuration summary, or an error traceback---plain text often gets lost in the terminal scroll. The `Panel` component draws a dynamic, unicode-bordered box perfectly fitted around your text.

Panels are fully self-aware. They calculate the true length of your text (ignoring the length of the internal color tags) to draw precise borders.

```python
from colrs import act, Panel

act()

# A straightforward panel. It will expand horizontally to fit the longest line.
Panel(
    "Configuration loaded successfully from /etc/config.json.\nNo syntax errors detected.",
    title="<white,bg_green> Configuration OK </>",
    border_color="green"
)

# Panels gracefully handle heavily nested tags inside them without breaking their borders.
Panel(
    "The connection to <blue>192.168.1.100</> timed out after <yellow>30.0s</>.\nPlease check your firewall settings.",
    title="<white,bg_red> Connection Failure </>",
    border_color="red"
)
```

---

### 4. Structured Data: Intelligent Auto-width Tables

Command-line output often involves displaying sets of data (users, processes, files). The `table` component takes headers and a list of lists, automatically calculating the maximum width of the data per column to render a perfectly aligned table.

Tables natively support `colrs` semantic styling tags inside individual cells without breaking alignment.

```python
from colrs import act, table

act()

headers = ["Process ID", "Service Name", "Status", "Memory Usage (MB)"]

# Notice the extensive use of inline tags for statuses
data = [
    ["1040", "nginx", "<green>Running</>", "24.5"],
    ["2011", "postgres-main", "<green>Running</>", "1024.0"],
    ["4099", "redis-cache", "<yellow>Restarting</>", "512.2"],
    ["8022", "python-worker-1", "<red>Dead</>", "0.0"]
]

# Render the table with custom branding
table(
    headers, 
    data, 
    border_color="cyan", 
    header_color="white,bg_cyan,bold"
)
```

---

### 5. Interactive Navigation: Single-Choice Menus

Typing strings repeatedly can lead to user error. The `menu` component captures the terminal, hides the cursor, and presents an interactive list. Users navigate cleanly using the `Up` and `Down` arrow keys, confirming their selection with `Enter`.

```python
from colrs import act, menu

act()

# Presents an interactive UI. The process halts until the user makes a selection.
selected_action = menu(
    title="<yellow>Select Server Operation:</yellow>",
    choices=["Reboot Target Server", "Restart Network Interfaces", "View System Logs", "Exit Console"],
    selected_prefix=">>> ",
    selected_color="cyan"
)

print(f"Executing protocol: <green>{selected_action}</green>")
```

---

### 6. Interactive Navigation: Multi-Choice Checkboxes

When the user needs to select multiple items from a list, use the `checkbox` component. Users navigate with arrows, toggle selections using the `Spacebar`, clear selections instantly using the `Delete` key, and confirm their final curated list with `Enter`.

You can also deeply customize the visual appearance of the checkmarks, including passing a custom `check_emoji`.

```python
from colrs import act, checkbox

act()

# An advanced checkbox rendering custom check characters.
installed_modules = checkbox(
    title="<cyan>Select modules to install in the virtual environment:</cyan>",
    choices=["Requests", "FastAPI", "SQLAlchemy", "Pydantic", "Pytest"],
    cursor=">",
    checked_char="✓",
    unchecked_char=" ",
    selected_color="green",
    # Pass check_emoji to use an entirely custom indicator for selected items
    check_emoji="[*]" 
)

if not installed_modules:
    print("<yellow>No modules selected. Aborting installation.</>")
else:
    print(f"Preparing to install: <green>{', '.join(installed_modules)}</green>")
```

---

### 7. Temporal Indicators: Spinners and Loaders

Long-running synchronous processes (like downloading files or executing heavy computations) leave the user staring at a frozen screen. The `loading` component provides instant visual feedback.

It can be used as a simple blocking mechanism for artificial delays, or more powerfully, as a `with` Context Manager that manages its own threads to spin fluidly while your main application logic computes.

```python
import time
from colrs import act, loading

act()

# Context Manager Mode: Highly Recommended
# The spinner runs in a background thread, keeping the UI alive while time.sleep runs.
with loading(text="Authenticating user...", style=7) as loader:
    time.sleep(2)
    # You can dynamically update the text at any point without breaking the spinner
    loader.update("Fetching high-resolution profile imagery...") 
    time.sleep(3)
    loader.update("Finalizing login state...")
    time.sleep(1)

# Blocking Mode: Useful for strict, predetermined delays
print("System cooling down...")
loading(duration=3, text="Purging cache...", style=4)
print("<green>System stable.</green>")
```

---

### 8. Temporal Indicators: Iterable Progress Bars

When processing arrays of data (e.g., lines in a file, records in a database), wrap your iterable in the `progress` component. `colrs` handles calculating ratios, drawing smooth dynamic progress bars, and rendering completion percentages seamlessly.

```python
import time
from colrs import act, progress

act()

dataset = range(500)

# Simply wrap 'dataset' in 'progress()'
# The terminal draws a dynamic bar that smoothly fills across the screen.
for record in progress(dataset, description="<cyan>Processing Machine Learning Epochs...</>"):
    # Simulate heavy data processing
    time.sleep(0.01) 
    
print("<green>All epochs processed successfully.</>")
```

---

### 9. Dynamic Mechanics: Live Output Replacement

If you need to repeatedly update text to the exact same lines on the terminal (such as a dashboard reading out sensor data or a clock), standard `print()` will spam the output endlessly downward. 

The `Live` component reserves a specific block of terminal space and exclusively updates it, overriding entirely over its previous text on every loop.

```python
import time
import random
from colrs import act, Live

act()

with Live(refresh_rate=0.5) as live_display:
    for iteration in range(15):
        cpu_temp = random.randint(40, 95)
        color = "green" if cpu_temp < 70 else "yellow" if cpu_temp < 85 else "red"
        
        # The update() method rewrites the reserved block on the terminal.
        live_display.update(
            f"Terminal Dashboard Iteration: {iteration}\n"
            f"CPU Core Temperature: <{color},bold>{cpu_temp}°C</>\n"
            f"Status: Monitoring actively."
        )
        time.sleep(0.5)
```

---

### 10. The Crown Jewel: The Complex Layout Engine

The `Layout` component represents the absolute peak of the `colrs` library. It transitions your application from a sequential script into a full-blown Command Line Application. 

You construct a recursive tree of `Layout` panes. You can split panes vertically (`split_column`) or horizontally (`split_row`), assign them names, and define their proportional sizes (`ratio`).

Once initialized inside a `.live()` context manager, you can update each named quadrant independently at any time.

```python
import time
import random
from colrs import act, Layout

act()

# Initialize the root layout
root_ui = Layout()

# Slice the terminal into three vertical sections (Header, Body, Footer)
root_ui.split_column(
    Layout(name="header", ratio=1),
    Layout(name="body", ratio=6),
    Layout(name="footer", ratio=1)
)

# Further slice the middle 'body' section into two horizontal sections (Sidebar, Main Content)
root_ui["body"].split_row(
    Layout(name="sidebar", ratio=3),
    Layout(name="content", ratio=7)
)

print("Booting specialized interface environment...")

# Render the layout structure to the screen and enter live streaming mode
with root_ui.live(refresh_rate=0.1) as dynamic_grid:
    
    # Render static blocks that rarely change
    dynamic_grid["header"].update("<white,bg_blue,bold> SERVER METRICS DASHBOARD v2.0 </>")
    dynamic_grid["footer"].update("<black,bg_white> Press Ctrl+C to safely terminate monitoring session. </>\nSystem Uptime: 24 Days")
    
    # Continually update specific targeted quadrants dynamically
    for tick in range(100):
        # Generate fake load metrics
        server_load = random.randint(0, 100)
        load_color = "green" if server_load < 50 else "yellow" if server_load < 80 else "red"
        
        # Update sidebar
        dynamic_grid["sidebar"].update(
            f"Active Workers: 14/16\n"
            f"Queue Delay: 12ms\n"
            f"Tick Rate: <cyan>{tick}/100</cyan>"
        )
        
        # Update main content independently
        dynamic_grid["content"].update(
            f"Current Traffic Load:\n"
            f"[{'#' * (server_load // 5):<20}] <{load_color}>{server_load}%</>\n"
            f"\n"
            f"Incoming Packet Signatures Normal."
        )
        
        time.sleep(0.1)
```

---

### 11. Asynchronous Compatibility: Native `asyncio` Flow

Modern Python backend applications heavily utilize `async`/`await` patterns for non-blocking I/O operations. `colrs` natively supports this paradigm. You must never mix synchronous locking components (`loading`, `Live`) with async loops. Instead, use their native asynchronous counterparts (`aloading`, `AsyncLive`).

```python
import asyncio
from colrs import act, aloading, AsyncLive

async def perform_database_migration():
    act()
    
    # 1. Async Loading Spinner
    # The spinner thread yields execution cleanly back to the asyncio event loop while the sleep occurs.
    async with aloading(text="Initiating asynchronous database migration...", style=6) as async_spinner:
        await asyncio.sleep(2)
        async_spinner.update("Calculating index hashes...")
        await asyncio.sleep(2)
        async_spinner.update("Flushing buffers...")
        await asyncio.sleep(1)

    # 2. Async Live Updater
    async with AsyncLive(refresh_rate=0.2) as live_feed:
        for validation_step in range(1, 6):
            live_feed.update(f"Migration phase completed.\nPerforming integrity check <cyan>#{validation_step}</cyan> of 5...")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(perform_database_migration())
```

---

### 12. Extracurricular Aesthetics: Text Effects

For banners, intro sequences, or critical success messages, traditional flat colors may not suffix. The `effects` module contains generators for complex visual transitions.

```python
import time
from colrs import act, effects

act()

# Typewriter: Types characters out one by one.
effects.typewriter(
    "Establishing secure connection payload...",
    speed=0.03,  # Delay between individual keystrokes
    color="lightgreen_ex"
)
time.sleep(1)

# Rainbow: Rapidly cycles through bright ANSI colors the entire string.
effects.rainbow("SECTOR 7 MAINFRAME HACKED SUCCESSFULLY", duration=3)
time.sleep(1)

# TrueColor Gradient: Generates a perfectly smooth math-based interpolation between two exact RGB hex values.
effects.gradient(
    "INITIALIZING THE MATRIX ENGINE PROTOCOLS",
    start_color="#00FFFF", # pure cyan
    end_color="#FF00FF",   # pure magenta
    duration=4
)
```

---

### 13. System Integration: Colored Python Logging

If your application relies on the standard Python `logging` module, you do not need to rewrite your logs to use `print`. `colrs` supplies a customized standard library `StreamHandler` that intercepts log emissions and colors them cleanly based entirely on their logging severity `LEVEL`.

```python
import logging
from colrs import act, ColorizingStreamHandler

act()

# Initialize standard Python logger
sys_logger = logging.getLogger("SystemCore")
sys_logger.setLevel(logging.DEBUG)

# Inject the colrs magical handler
sys_logger.addHandler(ColorizingStreamHandler())

# The handler intercepts these standard calls and applies robust styling
sys_logger.debug("Core process launched at memory address 0x00FF.")         # Renders gray/dim
sys_logger.info("Database connection successfully established.")            # Renders standard clear text
sys_logger.warning("Packet loss detected on Node 4. Retrying connection.")   # Renders bright yellow
sys_logger.error("Target user profile could not be located in directory.")   # Renders bright red
sys_logger.critical("KERNEL PANIC. SHUTTING DOWN IMMEDIATELY.")             # Renders flashing red/white
```

---

### 14. Global Theming Configuration

When establishing a brand or unified aesthetics across hundreds of script files, manually overriding parameters like `border_color` or `selected_color` in every single `Panel()`, `table()`, or `menu()` call is tedious. 

`set_theme()` overrides the core global defaults for the entire session.

```python
from colrs import act, set_theme, Panel, menu

act()

# Supply a dictionary mapping internal keys to standard supported colors.
neon_tokyo_theme = {
    "primary": "magenta",
    "border": "cyan",
    "menu_selected": "lightmagenta_ex",
    "panel_title_bg": "magenta"
}

set_theme(neon_tokyo_theme)

# These components instantly inherit the 'cyan' borders and 'magenta' titles/preferences.
Panel("The network has been compromised.", title="Alert")
menu(title="Intercept Data?", choices=["Yes", "No"])

# Calling it with an empty dictionary resets all parameters back to factory defaults.
set_theme({})
```

---

### 15. Standard Library Universal Compatibility

`colrs` was built from the ground up to never conflict with the Python Standard Library. Because it operates largely by proxying string representations and safely managing localized ANSI escapes, **you can use it immediately alongside `json`, `datetime`, `random`, `math`, `subprocess`, and any other core functionality.**

```python
import json
import random
import time
from datetime import datetime
from colrs import act, Panel

act()

# Operating cleanly alongside random and datetime
registration_status = {
    "user_token": f"UID-{random.randint(10000, 99999)}",
    "creation_time": datetime.now().isoformat(),
    "permissions": ["read", "write", "execute"],
    "is_admin": False
}

# The built-in json module serializes dictionaries into strings natively
# We can cleanly embed that standard string inside a colrs Panel without issue
formatted_json_string = json.dumps(registration_status, indent=4)

Panel(
    f"<yellow>{formatted_json_string}</yellow>",
    title="<white,bg_blue> Authorized User Data Payload </>",
    border_color="blue"
)

# You can still use time.sleep, subprocess.run, threads, etc. totally uninhibited.
print("Generating session... <cyan>Proceeding.</>")
time.sleep(1)
```

---

## Power-User Workflows: Import Aliases

Writing out `ColorizingStreamHandler` or `async_loading` repeatedly can bloat your code. `colrs` explicitly exposes a suite of short-hand aliases designed strictly for rapid prototyping and scripting speed.

### Standard Level Aliases
You can use these aliases for cleaner code without sacrificing too much readability.

| Alias | Original Object |
|---|---|
| `LogHandler` | `ColorizingStreamHandler` |
| `aloading` | `async_loading` |
| `aLive` | `AsyncLive` |
| `check` | `checkbox` |
| `prog` | `progress` |

### Super-Short Level Aliases
For absolute maximum speed when writing small bash-like python scripts:

| Alias | Original Object |
|---|---|
| `lo` | `loading` |
| `alo` | `async_loading` |
| `li` | `Live` |
| `ali` | `AsyncLive` |
| `me` | `menu` |
| `chk` | `checkbox` |
| `tb` | `table` |
| `pn` | `Panel` |
| `pr` | `progress` |
| `ef` | `effects` |
| `sth` | `set_theme` |
| `gth` | `get_theme` |
| `lh` | `LogHandler` |

**Rapid Prototyping Import Statement:**
```python
# Copy and initialize your toolset instantly:
from colrs import act, unact, lo, alo, li, ali, me, chk, tb, pn, pr, sth, gth, lh, ef
```

---

## Technical Specifications

- **Language:** Python 3.10+ highly recommended.
- **Strict Dependencies:** `colorama` (Required absolutely for guaranteeing unified Windows/Linux/macOS ANSI sequence translation).
- **Core Architecture:** Non-intrusive stream intercept buffering, context management locking.

## Open Source Contribution

Contributions define the open-source ethos. Any modifications, feature suggestions, or issue reports are greatly appreciated. Fork the repository, create a dedicated feature branch, commit your structural enhancements, and submit a pull request for review.

## License Declarations

The `colrs` project is formally distributed under the guidelines and restrictions of the absolute MIT License. Refer to the internal `LICENSE` document located in the root directory for explicit legal information, usage parameters, and protection details.
