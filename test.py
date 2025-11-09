# c:\Users\kalth\Downloads\bib-project3\colrs\test.py

# This file demonstrates the simplified import style.
# Before running, ensure the library is installed by running `pip install .` 
# in the terminal from the project directory.

print("--- Testing the `import colrs` style ---")

try:
    # 1. Import the entire library with one simple line
    import colrs

    # 2. Now, you can access all functions through the 'colrs' namespace.
    # This keeps your code clean and organized.
    colrs.cprint("This is a test using colrs.cprint()!", color="green")
    colrs.cprint("This text has a <black,bg_white>background</>.", color="white", bg_color="blue")
    colrs.cprint("Testing <green>inline</> <yellow>tag</> <red>coloring</>.")

    # Test the new inp_color feature in safe mode
    colrs.cinput("Testing cinput (prompt=yellow, input=blue): ", color="yellow", inp_color="blue")

    # You can also activate the patch this way
    colrs.act()
    
    print("Patch is now active! This line has <magenta>tags</> and <cyan>colors</>.")
    
    # Test patched input with same color for prompt and typing
    name = input("What's your name (typing in yellow)? ", color="yellow")
    print(f"Hello, {name}! This is a patched print with <green>tags</>.", color="cyan")

    # Test patched input with different color for prompt and typing
    color = input("Favorite color (prompt=cyan, input=red)? ", color="cyan", inp_color="red")
    print(f"You like <red>{color}</>!", color="green")

    # And unpatch it
    colrs.unact()
    print("Patch is off. This is a normal print again.")

    print("\n--- Test successful! You can use `import colrs` as requested. ---")

except ImportError:
    print("\nERROR: Could not import 'colrs'.")
    print("Please make sure you have installed the package first.")
    print("Navigate to the project directory in your terminal and run: pip install .")
except Exception as e:
    print(f"An error occurred: {e}")
