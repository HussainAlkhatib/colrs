# colorara/examples.py

"""
This file contains a collection of examples demonstrating the features
of the 'colrs' library. Run this file to see them in action.
"""

import time
import random
import logging
import asyncio

# Import all the necessary components from the library
from colrs import (
    act, unact, loading, prog, table, menu, check, Layout, LogHandler,
    aloading, aLive, set_theme, Panel, ActionManager
)

def wait_for_enter():
    """Pauses the script and waits for the user to press Enter."""
    act()
    input("\n<yellow,bg_black> Press Enter to continue to the next example... </>")
    unact()

def example_core_concept():
    """Demonstrates the basic activation and use of print/input."""
    print("\n--- 1. Core Concept: act() and unact() ---")
    print("This is a normal, default print.")
    act()
    print("This print is now <green>super-powered</>!", color="cyan")
    name = input("What's your name? ", color="yellow", inp_color="magenta")
    print(f"Hello, <bold>{name}</>!")
    unact()
    print("And we're back to normal.")

def example_enhanced_print():
    """Demonstrates advanced print formatting."""
    print("\n--- 2. Enhanced print() ---")
    act()
    print("This is red.", color="red")
    print("This is blue on a yellow background.", color="blue", bg_color="yellow")
    print("This is a <green>green text</> using inline tags.")
    print("<yellow>This is yellow with <blue>blue text</blue> inside.</yellow>")
    print("<white,bg_red> White text on a red background. </>")
    unact()

def example_smart_input():
    """Demonstrates color_rules in input()."""
    print("\n--- 3. Smart input() ---")
    act()
    username = input("Username: ", color="yellow", inp_color="cyan")
    choice = input(
        "Delete all files? (yes/no): ",
        color="cyan",
        color_rules={"yes": "red,bg_white", "no": "green"}
    )
    unact()

def example_panels():
    """Demonstrates the Panel component."""
    print("\n--- 4. Panels for Clean Output ---")
    act()
    success_message = "User 'Hussain' created successfully.\nAn activation email has been sent."
    Panel(
        success_message,
        title="<white,bg_green> Success </>",
        border_color="green"
    )
    unact()

def example_animations():
    """Demonstrates loading animations and progress bars."""
    print("\n--- 5. Loading Animations & Progress Bars ---")
    act()
    loading(duration=3, text="Syncing data...", style=7)
    with loading(text="Connecting to API...", style=2) as loader:
        time.sleep(2)
        loader.update("Downloading files...")
        time.sleep(2)
    for item in prog(range(200), description="<cyan>Processing items...</>"):
        time.sleep(0.01)
    unact()

def example_tables():
    """Demonstrates data tables."""
    print("\n--- 6. Data Tables ---")
    act()
    headers = ["ID", "User", "Status", "Last Login"]
    data = [
        ["101", "Hussain", "<green>Active</>", "2023-10-27 10:00"],
        ["102", "Ali", "<yellow>Idle</>", "2023-10-27 09:15"],
        ["104", "Zainab", "<red>Banned</>", "2023-10-26 15:30"]
    ]
    table(headers, data, border_color="cyan", header_color="white,bg_cyan")
    unact()

def example_menus():
    """Demonstrates interactive menus."""
    print("\n--- 7. Interactive Menus ---")
    act()
    action = menu(
        title="<yellow>What do you want to do?</yellow>",
        choices=["Restart Service", "View Logs", "Exit"]
    )
    print(f"You chose: <green>{action}</green>")
    features = check(
        title="<cyan>Select features to install:</cyan>",
        choices=["API", "Database", "Web UI", "Docs"]
    )
    print(f"Installing: <green>{', '.join(features)}</green>")
    unact()

def example_layout():
    """Demonstrates live layouts."""
    print("\n--- 8. Live Displays & Layouts ---")
    act()
    layout = Layout()
    layout.split_column(Layout(name="left", ratio=4), Layout(name="right", ratio=6))
    layout["right"].split_row(Layout(name="header"), Layout(name="stats", ratio=3))
    with layout.live(refresh_rate=1):
        layout["header"].update("<bg_magenta,white> Real-time System Dashboard </>")
        for i in range(5):
            data = [["Task A", f"<green>OK</>"], ["Task B", f"<yellow>WARN</>"]]
            layout["left"].update(table(headers=["Service", "Status"], data=data, to_string=True))
            cpu = random.randint(20, 90)
            layout["stats"].update(f"CPU: <cyan>{cpu}%</> | Cycle: {i+1}")
            time.sleep(1)
    unact()

def example_logging():
    """Demonstrates colored logging."""
    print("\n--- 9. Colored Logging ---")
    act()
    logger = logging.getLogger("colrs_example")
    if not logger.handlers: # Avoid adding handlers multiple times
        logger.setLevel(logging.DEBUG)
        logger.addHandler(LogHandler())
    logger.debug("This is a debug message.")
    logger.info("System startup successful.")
    logger.warning("Disk space is running low.")
    logger.error("Failed to connect to the database.")
    logger.critical("Core service has crashed!")
    unact()

async def example_async_support():
    """Demonstrates async components."""
    print("\n--- 10. Async Support ---")
    act()
    async with aloading(text="Doing async work...", style=6):
        await asyncio.sleep(3)
    async with aLive() as live:
        for i in range(5):
            live.update(f"Async Counter: <green>{i}</green>")
            await asyncio.sleep(1)
    unact()

def example_theming():
    """Demonstrates the theming system."""
    print("\n--- 11. Theming System ---")
    act()
    fire_theme = {
        "primary": "orange", "border": "red", "menu_selected": "yellow", "panel_title_bg": "red"
    }
    set_theme(fire_theme)
    Panel("This panel will now have a red border.", title="Fire Theme")
    choice = menu(title="Options", choices=["Option 1", "Option 2"])
    # Reset to default theme for subsequent examples
    set_theme({"primary": "cyan", "border": "white", "menu_selected": "cyan", "panel_title_bg": "cyan"})
    unact()

def example_action_tags():
    """Demonstrates the clickable ActionTagManager."""
    print("\n--- 12. Clickable Actions (Mouse Support) ---")
    act()

    def show_status():
        return "System status: <green>OK</>. Click <action=shutdown>here</action> to shut down."

    def shutdown_system():
        return "<red,bg_white> SHUTDOWN INITIATED! </>"

    actions = { "status": show_status, "shutdown": shutdown_system }

    print("Click on the underlined words with your mouse.")
    print("This demo will automatically exit after 15 seconds.")

    with ActionManager(actions, initial_text="Click <action=status>here</action> to check system status."):
        time.sleep(15)
    unact()

if __name__ == "__main__":
    example_core_concept(); wait_for_enter()
    example_enhanced_print(); wait_for_enter()
    example_smart_input(); wait_for_enter()
    example_panels(); wait_for_enter()
    example_animations(); wait_for_enter()
    example_tables(); wait_for_enter()
    example_menus(); wait_for_enter()
    example_layout(); wait_for_enter()
    example_logging(); wait_for_enter()
    asyncio.run(example_async_support()); wait_for_enter()
    example_theming()
    example_action_tags() # This is the last example, no need for wait_for_enter()
    act(); print("\n<green,bg_black> All examples finished. </>"); unact()