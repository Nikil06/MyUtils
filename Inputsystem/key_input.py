import sys
from .key_map import (DIRECT_KEYS, EXTENDED_KEYS, PARENT_000, PARENT_224, UNKNOWN_KEY)

WINDOWS = bool(sys.platform == "win32")

if WINDOWS:
    import msvcrt
else:
    import tty
    import termios
    import select


def get_char():
    if WINDOWS:
        # Direct function available for Windows
        return msvcrt.getch()
    else:
        # Obtain the file descriptor associated with the standard input (usually the keyboard).
        file_descriptor = sys.stdin.fileno()

        # Save the current terminal settings to later restore them.
        old_setting = termios.tcgetattr(file_descriptor)

        try:
            # Set the terminal to raw mode, which allows reading individual characters without buffering.
            tty.setraw(file_descriptor)

            # Read a single character from the terminal input.
            char = sys.stdin.read(1)
        finally:
            # Restore the original terminal settings.
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_setting)

        # Return the captured character.
        return char


def check_for_key_press():
    if WINDOWS:
        return msvcrt.kbhit()
    else:
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def get_key():
    char = get_char()
    if char == PARENT_224["code"]:
        extended_char = get_char()
        return EXTENDED_KEYS[PARENT_224].get(extended_char, UNKNOWN_KEY)
    elif char == PARENT_000["code"]:
        extended_char = get_char()
        return EXTENDED_KEYS[PARENT_000].get(extended_char, UNKNOWN_KEY)
    else:
        return DIRECT_KEYS.get(char, UNKNOWN_KEY)
