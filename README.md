# colrs - The Ultimate Python Library for Rich CLI Interfaces 🎨

[![PyPI version](https://badge.fury.io/py/colrs.svg)](https://badge.fury.io/py/colrs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`colrs` is a powerful, intuitive, and elegant Python library for creating beautiful and interactive command-line interfaces. It transforms your terminal from a simple text display into a rich, dynamic application canvas.

Forget juggling ANSI codes. `colrs` offers a high-level, component-based approach with a unique activation model, making rich CLI styling effortless and fun.

![colrs in action](https://raw.githubusercontent.com/HussainAlkhatib/colrs/main/media/show.gif) 
*(This GIF showcases the power of `colrs`. It's highly recommended to include one!)*

## 🚀 Core Philosophy: `act()` and `unact()`

The magic of `colrs` lies in its activation model. Instead of wrapping every print statement, you activate styling for a section of your code.

- **`act()`**: Monkey-patches `print()` and `input()`. All subsequent calls are super-powered, understanding HTML-like tags (`<green>Hello</>`), color arguments, and more.
- **`unact()`**: Restores the original `print` and `input` functions, returning to default behavior.

```python
from colrs import act, unact

print("This is a normal print.")

act()
print("This print is now <green>super-powered</>")
name = input("What's your name? ", color="yellow", inp_color="magenta")
print(f"Hello, <bold>{name}</>")
unact()

print("And we're back to normal.")
```

## 📦 Installation

```bash
pip install colrs
```

## ✨ Features



`colrs` is more than just colors. It's a complete toolkit for modern CLI development. Below are detailed explanations and examples for each feature.



### 1. Enhanced `print()` with Nested Tags

Once `act()` is called, `print()` is super-powered. You can use simple, HTML-like tags to style any part of a string. `colrs` intelligently handles nested tags: the inner color is applied, and when the tag closes, it correctly reverts to the parent tag's color.



```python

from colrs import act, unact



act()

# The word "service" will be blue, and the rest of the warning yellow.

print("<yellow>Warning: The <blue>database service</blue> is currently offline.</yellow>")



# You can combine foreground and background colors.

print("<white,bg_red> EMERGENCY </> All systems are down!")

unact()

```



### 2. Smart `input()` with Color Rules

Style your prompts and user input separately. The `color_rules` feature provides instant visual feedback *after* the user presses Enter, based on their input. You can pass rules as a dictionary or as intuitive keyword arguments.



```python

from colrs import act, unact



act()

# Use kwargs for intuitive rule-setting

choice = input(

    "Delete all files? (yes/no): ",

    color="cyan",          # Color of the prompt text

    inp_color="white",     # Color for user typing

    yes="red,bg_white",    # Color to apply if user types "yes"

    no="green"             # Color to apply if user types "no"

)

print(f"You chose: {choice}")

unact()

```



### 3. Panels

Draw attention to important information using clean, bordered panels. Panels are color-aware and will correctly calculate their dimensions around styled text.



```python

from colrs import act, unact, Panel



act()

Panel(

    "User <green>'Hussain'</green> created successfully.\nAn activation email has been sent.",

    title="<white,bg_green> Success </>",

    border_color="green"

)

unact()

```



### 4. Tables

Display data in a clean, organized table format. `colrs` automatically handles column widths and supports inline color tags within cells.



```python

from colrs import act, unact, table



act()

headers = ["ID", "User", "Status", "Last Login"]

data = [

    ["101", "Hussain", "<green>Active</>", "2023-10-27 10:00"],

    ["102", "Ali", "<yellow>Idle</>", "2023-10-27 09:15"],

    ["104", "Zainab", "<red>Banned</>", "2023-10-26 15:30"]

]

table(headers, data, border_color="cyan", header_color="white,bg_cyan")

unact()

```



### 5. Interactive Menus

Create interactive single-choice prompts that users can navigate with arrow keys and select with Enter.



```python

from colrs import act, unact, menu



act()

action = menu(

    title="<yellow>What do you want to do?</yellow>",

    choices=["Restart Service", "View Logs", "Exit"],

    selected_prefix="-> ",

    selected_color="cyan"

)

print(f"You chose to: <green>{action}</green>")

unact()

```



### 6. Interactive Checkboxes

Create interactive multi-choice prompts. Users can navigate with arrow keys, toggle selections with the spacebar, and confirm with Enter.



```python

from colrs import act, unact, check



act()

features = check(

    title="<cyan>Select features to install:</cyan>",

    choices=["API", "Database", "Web UI", "Docs"],

    cursor=">",

    checked_char="[x]",

    unchecked_char="[ ]",

    selected_color="green"

)

print(f"Installing: <green>{', '.join(features)}</green>")

unact()

```



### 7. Loading Animations

Provide visual feedback for long-running tasks. `loading` can be used in two ways: as a blocking function for a fixed time, or as a context manager for tasks of unknown duration.



```python

import time

from colrs import act, unact, loading



act()

# As a context manager (for tasks of unknown length)

with loading(text="Connecting to API...", style=7) as loader:

    time.sleep(2)

    loader.update("Downloading files...") # Update text on the fly

    time.sleep(2)



# As a blocking function

loading(duration=3, text="Syncing data...", style=4)

unact()

```



### 8. Progress Bars

Wrap any iterable (like a list or range) to display a smooth, color-changing progress bar.



```python

import time

from colrs import act, unact, prog



act()

for item in prog(range(200), description="<cyan>Processing items...</>"):

    time.sleep(0.02)

unact()

```



### 9. Text Effects

Add a dynamic flair to your text with `typewriter`, `rainbow`, and `gradient` effects. The `gradient` effect supports TrueColor via hex codes.



```python

import time

from colrs import act, unact, effects



act()

print("<yellow>--- Typewriter Effect ---</yellow>")

effects.typewriter(

    "This is a typewriter effect...",

    speed=0.04,

    color="green"

)

time.sleep(1)



print("\n<yellow>--- Rainbow Effect ---</yellow>")

effects.rainbow("*** RAINBOW POWER ***", duration=4)

time.sleep(1)



print("\n<yellow>--- Gradient Effect (TrueColor) ---</yellow>")

effects.gradient(

    "*** HELLO WORLD ***",

    start_color="#FF00FF", # Magenta

    end_color="#00FFFF",   # Cyan

    duration=5

)

unact()

```



### 10. Live Displays

The `Live` component creates a "live" area in your terminal that can be updated continuously. It's perfect for dashboards, clocks, or any dynamically changing information.



```python

import time

from datetime import datetime

from colrs import act, unact, Live



act()

with Live(refresh_rate=1) as live:

    for i in range(10):

        now = datetime.now().strftime("%H:%M:%S")

        live.update(f"Time: <green>{now}</green>\nUpdate <cyan>#{i+1}</cyan>")

        time.sleep(1)

unact()

```



### 11. Layout Engine

The Layout engine is one of `colrs`' most powerful features. Build complex, live-updating terminal dashboards by splitting the screen into resizable rows and columns.



```python

import time

from colrs import act, unact, Layout



act()

# Define the layout structure

layout = Layout()

layout.split_column(

    Layout(name="header", ratio=1),

    Layout(name="main", ratio=5),

    Layout(name="footer", ratio=1)

)

layout["main"].split_row(

    Layout(name="left_sidebar", ratio=2),

    Layout(name="content", ratio=8)

)



# Run the live display

with layout.live(refresh_rate=0.1) as live_layout:

    live_layout["header"].update("<white,bg_blue> My Dashboard </>")

    live_layout["footer"].update("<yellow>Status: OK</>")

    

    for i in range(101):

        # Update different parts of the layout independently

        live_layout["left_sidebar"].update(f"Progress:\n<cyan>{i}%</>")

        live_layout["content"].update(f"Event <green>#{i}</green> processed.")

        time.sleep(0.05)

unact()

```



### 12. Theming

Customize the look and feel of all components to match your brand by defining a central color palette.



```python

from colrs import act, unact, set_theme, Panel, menu



act()

# Define a custom theme

fire_theme = {

    "primary": "orange",

    "border": "red",

    "menu_selected": "yellow",

    "panel_title_bg": "red"

}

set_theme(fire_theme)



Panel("This panel now has a red border.", title="Fire Theme")

menu(title="Options", choices=["Option 1", "Option 2"])



# Reset to default by passing an empty dict

set_theme({})

unact()

```



### 13. Colored Logging

Integrate `colrs` with Python's standard `logging` module for beautiful, readable logs, color-coded by level.



```python

import logging

from colrs import act, unact, LogHandler



act()

logger = logging.getLogger("my_app")

logger.setLevel(logging.DEBUG)

# Avoid adding handlers multiple times if run in a loop

if not logger.handlers:

    logger.addHandler(LogHandler())



logger.debug("This is a debug message.")

logger.info("System startup successful.")

logger.warning("Disk space is running low.")

logger.error("Failed to connect to the database.")

logger.critical("Core service has crashed!")

unact()

```



### 14. Async Support

`colrs` provides asynchronous, non-blocking versions of its dynamic components, perfect for modern `asyncio`-based applications.



```python

import asyncio

from colrs import act, unact, aloading, aLive



async def main():

    act()

    print("--- Async Loader ---")

    async with aloading(text="Doing async work...", style=6):

        await asyncio.sleep(3)



    print("\n--- Async Live ---")

    async with aLive() as live:

        for i in range(5):

            live.update(f"Async Counter: <green>{i}</green>")

            await asyncio.sleep(1)

    unact()



asyncio.run(main())

```



---



## ⚡ Power-User Features



### Aliases for Faster Development

For rapid development, `colrs` provides two levels of optional, shorter aliases for most common components.



**Standard Aliases:**

| Alias | Original |

|---|---|

| `LogHandler` | `ColorizingStreamHandler` |

| `aloading` | `async_loading` |

| `aLive` | `AsyncLive` |

| `check` | `checkbox` |

| `prog` | `progress` |



**Super-Short Aliases:**

| Alias | Original |

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



You can import them directly for a more concise coding style.



```python

# Copy this line to import the core functions and all super-short aliases

from colrs import act, unact, lo, alo, li, ali, me, chk, tb, pn, pr, sth, gth, lh, ef

```



## 🤝 Contributing



Contributions are what make the open-source community such an amazing place. Any contributions you make are **greatly appreciated**. Please feel free to fork the repo, create a feature branch, and submit a pull request.



## 📜 License



Distributed under the MIT License. See `LICENSE` for more information.
