from colrs import act, unact, effects

act()

print("<cyan>--- Testing Text Effects ---</>")

print("\n<yellow>--- Typewriter Effect (Simple) ---</yellow>")
effects.typewriter(
    "This is the new, powerful, and simple text effects engine!",
    speed=0.05,
    color="green"
)

print("\n<yellow>--- Typewriter with inline tags ---</yellow>")
effects.typewriter(
    "You can also use <magenta>inline</> <blue>tags</> with the typewriter effect.",
    speed=0.05
)

print("\n<yellow>--- Rainbow Effect ---</yellow>")
effects.rainbow(
    "*** RAINBOW POWER ***",
    speed=0.1,
    duration=5
)

print("\n<yellow>--- Gradient Effect ---</yellow>")
effects.gradient(
    "LOADING...",
    start_color="blue",
    end_color="magenta",
    duration=5
)

unact()

print("\nDone.")