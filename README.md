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

## ✨ Features Overview

`colrs` is more than just colors. It's a complete toolkit for modern CLI development.

| Feature | Description | Quick Example |
|---|---|---|
| **Enhanced `print`** | Use inline tags for nested, multi-color styling. | `print("<yellow>Warning: <blue>service</blue> is down.</>")` |
| **Smart `input`** | Style prompts, user input, and apply colors based on rules. | `input("Delete?", yes="red", no="green")` |
| **Panels** | Draw attention with clean, customizable bordered boxes. | `Panel("Success!", title="Status", border_color="green")` |
| **Tables** | Display data in beautifully formatted, color-aware tables. | `table(headers, data, header_color="white,bg_cyan")` |
| **Menus & Checkboxes** | Create interactive single and multi-choice prompts. | `action = menu(choices=["View", "Exit"])` |
| **Animations** | Provide feedback with spinners and context managers. | `with loading(text="Syncing..."): ...` |
| **Progress Bars** | Wrap any iterable to show a smooth progress bar. | `for i in prog(range(100)): ...` |
| **Text Effects** | Add flair with `typewriter`, `rainbow`, and `gradient` effects. | `effects.gradient("Hello", "blue", "magenta")` |
| **Live Displays** | Update multiple sections of the screen in real-time. | `with Live() as live: live.update(...)` |
| **Layouts** | Build complex, live-updating dashboards with rows and columns. | `layout.split_column(left_panel, right_panel)` |
| **Theming** | Define a central color palette for all components. | `set_theme({"primary": "blue", "border": "grey"})` |
| **Async Support** | `async/await` versions of animations and live displays. | `async with aloading(): ...` |

---

## 🌟 In-Depth Examples

### 1. The Power of Nested Tags

`colrs` intelligently handles nested tags. The inner color is applied, and when the tag closes, it correctly reverts to the parent tag's color.

```python
act()
# The word "service" will be blue, and the rest of the warning yellow.
print("<yellow>Warning: The <blue>database service</blue> is currently offline.</>")

# You can combine foreground and background colors.
print("<white,bg_red> EMERGENCY </> All systems are down!")
unact()
```

### 2. Smart `input()` with Color Rules

Style your prompts and user input separately. The `color_rules` feature (or keyword arguments) provides instant visual feedback after the user presses Enter.

```python
act()
# Use kwargs for intuitive rule-setting
choice = input(
    "Delete all files? (yes/no): ",
    color="cyan",          # Color of the prompt text
    inp_color="white",     # Color for user typing
    yes="red,bg_white",    # Color to apply if user types "yes"
    no="green"             # Color to apply if user types "no"
)
unact()
```

### 3. Advanced Components

#### Panels & Tables
Display information cleanly. All components are aware of color tags and calculate layout dimensions correctly.

```python
from colrs import Panel, table, act

act()
Panel(
    "User <green>'Hussain'</> created successfully.\nAn activation email has been sent.",
    title="<white,bg_green> Success </>",
    border_color="green"
)

headers = ["ID", "User", "Status"]
data = [
    ["101", "Hussain", "<green>Active</>"],
    ["102", "Ali", "<yellow>Idle</>"],
    ["104", "Zainab", "<red>Banned</>"]
]
table(headers, data, border_color="cyan", header_color="white,bg_cyan")
unact()
```

#### Interactive Menus & Checkboxes
Guide users with interactive prompts.

```python
from colrs import menu, check, act

act()
# Single-choice menu (navigated with arrow keys)
action = menu(
    title="<yellow>What do you want to do?</yellow>",
    choices=["Restart Service", "View Logs", "Exit"],
    selected_prefix="-> "
)

# Multi-choice checkbox (toggled with spacebar)
features = check(
    title="<cyan>Select features to install:</cyan>",
    choices=["API", "Database", "Web UI"],
    cursor=">",
    checked_char="[x]",
    unchecked_char="[ ]"
)
unact()
```

### 4. Dynamic Effects & Animations

#### Progress Bars & Loaders
Provide rich feedback for tasks. `loading` can be a blocking call (`duration=...`) or a context manager.

```python
import time
from colrs import loading, prog, act

act()
# Context manager for tasks of unknown length
with loading(text="Connecting to API...", style=7) as loader:
    time.sleep(2)
    loader.update("Downloading files...") # Update text on the fly
    time.sleep(2)

# Progress bar for any iterable
for item in prog(range(200), description="<cyan>Processing items...</>"):
    time.sleep(0.01)
unact()
```

#### TrueColor Text Effects
Create stunning text effects using `gradient` (with hex colors), `rainbow`, and `typewriter`.

```python
from colrs import effects, act

act()
effects.typewriter("This is a typewriter effect...", speed=0.04, color="green")

effects.gradient(
    "*** HELLO WORLD ***",
    start_color="magenta", # Magenta
    end_color="cyan",   # Cyan
    duration=5
)
unact()
```

### 5. The Layout Engine: Building Dashboards
This is one of `colrs`' most powerful features. Create complex, live-updating terminal dashboards by splitting the screen into resizable rows and columns.

```python
import time
from colrs import Layout, act

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
        live_layout["content"].update(f"Event <green>#{i}</> processed.")
        time.sleep(0.05)
unact()
```

## ⚡ Power-User Features

- **Theming**: Use `set_theme({...})` to define a central color palette (`primary`, `border`, `menu_selected`, etc.) that all components will use.
- **Async Support**: `aloading()` and `aLive()` provide non-blocking, `asyncio`-native versions of animations and live displays.

### Aliases for Power Users

For faster development, `colrs` provides two levels of optional, shorter aliases for most common components.

**Standard Aliases:**
| Alias | Original |
|---|---|
| `LogHandler` | `ColorizingStreamHandler` |
| `aloading` | `async_loading` |
| `aLive` | `AsyncLive` |
| `check` | `checkbox` |
| `prog` | `progress` |

**Super-Short Aliases:**
| Alias | Original | Alias | Original |
|---|---|---|---|
| `lo` | `loading` | `alo` | `async_loading` |
| `li` | `Live` | `ali` | `AsyncLive` |
| `me` | `menu` | `chk` | `checkbox` |
| `tb` | `table` | `pn` | `Panel` |
| `pr` | `progress` | `ef` | `effects` |
| `sth` | `set_theme` | `gth` | `get_theme` |
| `lh` | `LogHandler` | | |


## 🤝 Contributing

Contributions are what make the open-source community such an amazing place. Any contributions you make are **greatly appreciated**. Please feel free to fork the repo, create a feature branch, and submit a pull request.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.