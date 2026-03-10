# colrs_showcase.py

import time
import asyncio
import logging
from colrs import act, unact, loading, table, set_theme, menu, Panel, Live, ColorizingStreamHandler, checkbox, async_loading, AsyncLive, progress, effects, Layout

def showcase():
    act()
    
    print()
    print("<cyan,bg_black>=== Welcome to colrs Ultimate Showcase ===</>")
    print("<yellow>This script demonstrates all the major features of the colrs library in one go!</yellow>")
    print()
    time.sleep(1)

    # 1. Basic & Nested Prints
    print("<green>--- 1. Basic & Nested Prints ---</>")
    print("Normal text, <red>red text</red>, <blue,bg_yellow>blue on yellow</>.")
    print("<cyan>Nested: <magenta>middle</magenta> back to cyan.</>")
    print()
    time.sleep(1)

    # 2. Smart Input
    print("<green>--- 2. Smart Input ---</>")
    name = input("Enter your username (try 'admin' for red output): ",
                 color="yellow", inp_color="white", admin="red", default="green")
    print(f"Hello, <bold>{name}</>!")
    print()
    time.sleep(1)

    # 3. Panel
    print("<green>--- 3. Panels ---</>")
    Panel("<white>This is a flexible panel content.\nIt automatically resizes to fit text!</white>", title="<magenta>Panel Title</>", border_color="blue")
    print()
    time.sleep(1)

    # 4. Table
    print("<green>--- 4. Tables ---</>")
    headers = ["ID", "Name", "Status", "Role"]
    data = [
        ["1", "Alice", "<green>Active</>", "Admin"],
        ["2", "Bob", "<yellow>Idle</>", "User"],
        ["3", "Charlie", "<red>Banned</>", "Guest"]
    ]
    table(headers, data, border_color="cyan", header_color="blue")
    print()
    time.sleep(1)

    # 5. Checkbox
    print("<green>--- 5. Interactive Checkbox ---</>")
    res = checkbox("<cyan>Select your preferred frameworks (Space to toggle, Enter to confirm):</>", ["React", "Vue", "Angular", "Svelte"], selected_color="magenta", check_emoji="🌟")
    print(f"You selected: <yellow>{', '.join(res) if res else 'None'}</>")
    print()
    time.sleep(1)

    # 6. Menu
    print("<green>--- 6. Interactive Menu ---</>")
    choice = menu("<cyan>Choose an action to proceed:</>", ["Continue", "Skip", "Abort"], selected_color="green")
    print(f"You chose: <yellow>{choice}</>")
    print()
    time.sleep(1)

    # 7. Loading
    print("<green>--- 7. Loading Animation ---</>")
    with loading(text="Processing heavy data...", style=2) as loader:
        time.sleep(2)
        loader.update("Finalizing chunks...")
        time.sleep(1)
    print()

    # 8. Progress Bar
    print("<green>--- 8. Progress Bar ---</>")
    for _ in progress(range(50), description="<cyan>Downloading assets</>"):
        time.sleep(0.02)
    print()

    # 9. Effects
    print("<green>--- 9. Text Effects ---</>")
    effects.typewriter("This is the typewriter effect rendering text smoothly...", speed=0.03, color="yellow")
    effects.rainbow("This is the rainbow effect shining brightly!", duration=2)
    effects.gradient("This is the TrueColor gradient effect blending colors!", start_color="#FF0000", end_color="#0000FF", duration=2)
    print()

    # 10. Theming
    print("<green>--- 10. Centralized Theming ---</>")
    set_theme({"border": "magenta", "panel_title_bg": "black", "menu_selected": "red"})
    Panel("Theme changed globally! Borders are now magenta.", title="Theme Test")
    set_theme({"border": "white"}) # Reset back to normal
    print()
    time.sleep(1)

    # 11. Logging
    print("<green>--- 11. Colored Logging ---</>")
    logger = logging.getLogger("colrs_demo")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        logger.addHandler(ColorizingStreamHandler())
    
    logger.debug("System debug analysis running.")
    logger.info("Connection established successfully.")
    logger.warning("Resource usage is surprisingly high.")
    logger.error("Failed to connect to the secondary node.")
    logger.critical("Catastrophic failure in the main core!")
    print()
    time.sleep(1)

    # 12. Layout & Live Display
    print("<green>--- 12. Complex Layout & Live Rendering ---</>")
    print("<yellow>Generating a live updating layout for 3 seconds...</>")
    time.sleep(1)
    
    layout = Layout()
    layout.split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=2)
    )
    with layout.live(refresh_rate=0.1) as live_layout:
        for i in range(30):
            progress_bar = "█" * (i//3) + "─" * (10 - i//3)
            live_layout["left"].update(f"Frame Processing:\n<cyan>{i}/30</>")
            live_layout["right"].update(f"Status Progress:\n<green>[{progress_bar}]</>\nTime left: <red>{(30 - i) / 10:.1f}s</>")
            time.sleep(0.1)

    print()
    print("<green,bg_black>=== Showcase Complete! Thank you for using colrs. ===</>")
    unact()

if __name__ == "__main__":
    showcase()
