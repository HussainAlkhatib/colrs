# colorara/colorara/magic.py

import builtins
from .core import cprint, _get_colored_input_prompt, _process_text_for_printing

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
    
    text = " ".join(map(str, args))
    processed_text = _process_text_for_printing(text, color, bg_color)
    
    _original_print(processed_text, **kwargs)

def _magic_input(prompt: str = "", **kwargs) -> str:
    """
    A patched version of input that handles color arguments for the prompt
    and for the user's typed input.
    """
    # Extract our custom color arguments from kwargs
    color = kwargs.get("color")
    bg_color = kwargs.get("bg_color")
    inp_color = kwargs.get("inp_color")
    
    final_prompt = _get_colored_input_prompt(prompt, color, bg_color, inp_color)
    return _original_input(final_prompt)

def magic():
    """
    Activates 'Magic Mode' by patching the built-in print and input functions.
    
    This allows you to use 'color' and 'bg_color' arguments directly in print()
    and input() without calling a special function.
    
    Warning: This modifies built-in functions and may conflict with other
    libraries that also modify them. Use with caution.
    """
    if builtins.print == _magic_print:
        cprint("Magic is already active.", color="yellow")
        return

    builtins.print = _magic_print
    builtins.input = _magic_input
    cprint("Magic activated. `print` and `input` are now color-aware.", color="yellow")

def revert():
    """
    Deactivates 'Magic' and restores the original built-in functions.
    """
    if builtins.print != _magic_print:
        cprint("Magic is not active.", color="yellow")
        return
        
    builtins.print = _original_print
    builtins.input = _original_input
    cprint("Magic deactivated. `print` and `input` restored.", color="yellow")
