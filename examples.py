# colorara/examples.py

def run_examples():
    """
    Demonstrates the simplified use of the library with act() and unact().
    """
    # If you are running this script before installing the package,
    # you need to make sure 'colorara' is in the Python path.
    # One way is to install it first using `pip install .`
    try:
        from colrs import act, unact, loading
    except ImportError:
        print("Could not import colrs. Please install it first with 'pip install .'")
        return

    print("\n--- Running Simplified Examples ---")
    print("Library is not active. This is a normal print.")

    # Activate the patching
    act()

    # Now use the standard print and input
    print("Patching is ON. This print is magenta.", color="magenta")
    print("And this one has a red background.", color="white", bg_color="red")
    print("You can use <green>inline</> <yellow>tags</> too!")
    
    try:
        food = input("What is your favorite food? ", color="yellow")
        print(f"You like {food}? That's cool!", color="green")
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled.", color="yellow")

    # It's good practice to deactivate when you're done
    unact()
    print("Patching is OFF. This print is back to normal.")

def run_loading_examples():
    """Demonstrates the new loading animations."""
    try:
        from colrs import loading
    except ImportError:
        return # Already handled in the first function

    print("\n--- Running Loading Animation Examples ---")
    loading(style=1, duration=3, text="Processing data...", color="cyan")
    loading(style=2, duration=3, text="Connecting to server...", color="magenta")
    loading(style=7, duration=4, text="Compiling assets...", color="yellow", end_text="Build complete!")

if __name__ == "__main__":
    run_examples()
    run_loading_examples()
    print("\n--- All examples finished ---")
