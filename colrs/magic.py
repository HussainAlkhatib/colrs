# colorara/colorara/magic.py

import builtins
from .core import _process_text_for_printing, COLORS

def _get_colored_input_prompt(prompt: str, color: str, bg_color: str, inp_color: str) -> str:
    """
    Internal helper to construct the final prompt string for input,
    handling both prompt color and user input color.
    """
    # If inp_color is not given, it defaults to the prompt's text color
    effective_inp_color = inp_color if inp_color is not None else color

    # Process the prompt for any inline tags, applying base colors if no tags exist.
    processed_prompt = _process_text_for_printing(prompt, color, bg_color)

    # Get the color code for the user's input, or an empty string if no color
    input_color_code = COLORS.get(str(effective_inp_color).lower(), "") if effective_inp_color else ""
    
    # The final prompt string sets the color for the user's typing
    return processed_prompt + input_color_code

_original_print = builtins.print
_original_input = builtins.input

def _magic_print(*args, **kwargs):
    """
    A patched version of print that handles color arguments, including
    inline color tags.
    """
    # Extract our custom color arguments, removing them from kwargs
    color = kwargs.pop("color", None)
    bg_color = kwargs.pop("bg_color", None)
    to_string = kwargs.pop("to_string", False)
    
    text = " ".join(map(str, args))
    processed_text = _process_text_for_printing(text, color, bg_color)
    
    if to_string:
        return processed_text
    else:
        _original_print(processed_text, **kwargs)

def _magic_input(prompt: str = "", **kwargs) -> str:
    """
    A patched version of input that handles color arguments for the prompt
    and for the user's typed input.
    """
    # Extract our custom color arguments from kwargs
    color = kwargs.pop("color", None)
    bg_color = kwargs.pop("bg_color", None)
    inp_color = kwargs.pop("inp_color", None)
    
    # --- Smart color_rules handling ---
    # Method 1: User provides the color_rules dictionary directly.
    color_rules = kwargs.pop("color_rules", None)
    
    # Method 2: If no dict is provided, treat any remaining kwargs as rules.
    # This allows for the more intuitive syntax: input(..., yes="green", no="red")
    if color_rules is None:
        # kwargs now only contains the "extra" arguments.
        if kwargs:
            color_rules = kwargs
        else:
            color_rules = {} # Ensure it's a dict
    
    final_prompt = _get_colored_input_prompt(prompt, color, bg_color, inp_color)
    user_input = _original_input(final_prompt)

    # --- Advanced color_rules processing ---
    rule_color_to_apply = None
    if color_rules:
        # Make input case-insensitive for matching
        user_input_lower = user_input.lower()
        
        for rule_key, rule_color in color_rules.items():
            # Check if the rule_key is a list/tuple of words or a single word
            if isinstance(rule_key, (list, tuple)):
                if user_input_lower in [item.lower() for item in rule_key]:
                    rule_color_to_apply = rule_color
                    break
            # Check for single word match (case-insensitive)
            elif user_input_lower == str(rule_key).lower():
                rule_color_to_apply = rule_color
                break

    if rule_color_to_apply:
        # This provides visual feedback AFTER the user presses Enter.
        import sys
        sys.stdout.write('\033[F')
        base_prompt = _get_colored_input_prompt(prompt, color, bg_color, None)
        _magic_print(f"{base_prompt}<{rule_color_to_apply}>{user_input}</>")

    return user_input

def act():
    """
    Activates the patching of the built-in print and input functions.
    
    This allows you to use 'color' and 'bg_color' arguments directly in print()
    and input() without calling a special function.
    
    Warning: This modifies built-in functions and may conflict with other
    libraries that also modify them. Use with caution.
    """
    if builtins.print is _magic_print:
        return

    builtins.print = _magic_print
    builtins.input = _magic_input

def unact():
    """
    Deactivates the patching and restores the original built-in functions.
    """
    if builtins.print is not _magic_print:
        return
        
    builtins.print = _original_print
    builtins.input = _original_input
