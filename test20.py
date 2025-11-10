# test20.py
from colrs import act, unact, ActionManager
import time

act()

# 1. عرف الدوال التي تريد تنفيذها
def show_status():
    return "System status: <green>OK</>. Click <action=shutdown>here</action> to shut down."

def shutdown_system():
    return "<red,bg_white> SHUTDOWN INITIATED! </>"

# 2. قم بربط أسماء الأفعال بالدوال
actions = {
    "status": show_status,
    "shutdown": shutdown_system
}

# 3. استخدم مدير الأفعال
# The ActionManager takes full control of the screen. 
# We provide all necessary text to it directly.
with ActionManager(actions, initial_text="--- Action Tag Manager Demo ---\nClick on the underlined words with your mouse.\n\nClick <action=status>here</action> to check system status.") as manager:
    try:
        # Keep the main thread alive to listen for clicks
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, EOFError):
        pass

unact()
