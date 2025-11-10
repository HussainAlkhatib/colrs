from colrs import (
    act, unact, loading, prog, table, menu, check, Layout, LogHandler,
    aloading, aLive, set_theme, Panel, ActionManager, draw
)

def example_drawing_shapes():
    """Demonstrates drawing geometric shapes."""
    print("\n--- 13. Drawing Geometric Shapes ---")
    act()

    print("<yellow>Let's draw a rectangle!</yellow>")
    try:
        width = int(input("Enter width (characters): ", color="cyan"))
        height = int(input("Enter height (characters): ", color="cyan"))
        draw("rectangle", width, height, char='*', color="green", bg_color="blue")
    except ValueError:
        print("<red>Invalid input. Please enter numbers.</red>")
    
    print("\n<yellow>Drawing a smaller square...</yellow>")
    draw("rectangle", 5, 5, char='@', color="magenta") # A square is a rectangle with equal sides
    unact()

if __name__ == "__main__":
    example_drawing_shapes()
    act(); 
    print("\n<green,bg_green> All examples finished. </>"); 
    unact()