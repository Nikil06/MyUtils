import sys
from getpass import getpass

if sys.platform == "win32":
    import msvcrt  # Import modules related to Windows
else:
    import tty     # Import modules related to Mac and Linux
    import termios


def get_char():
    if sys.platform == "win32":
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


def get_password(prompt="Password: ", mask_char="*") -> str:
    ########################################################################
    # Check if given prompt and mask character are valid
    if not isinstance(prompt, str):
        raise TypeError(f"prompt must be a string not {type(prompt).__name__}")
    if not isinstance(mask_char, str):
        raise TypeError(f"mask_char must be a string of length 0 or 1 not {type(mask_char).__name__}")
    if len(mask_char) > 1:
        raise ValueError(f"mask_char must be a string of length of 0 or 1.")

    # If mask is empty then we can fall back to the standard getpass
    if mask_char == '' or sys.stdin is not sys.__stdin__:
        # ALSO Check if the standard input (sys.stdin) is different from the original standard input (sys.__stdin__).
        # In this situation, input may be redirected from a source other than the keyboard.
        # To ensure secure password input, fall back on the getpass library, which is designed for secure password input.

        return getpass(prompt)
    ########################################################################
    # Actual logic for input starts here

    password_chars = []

    sys.stdout.write(prompt)  # Similar to print(prompt)
    sys.stdout.flush()  # Flushes the stdout so that the prompt is printed immediately and not stored to print later

    while True:
        key_pressed = ord(get_char())

        if key_pressed == 13:  # i.e. Enter key is pressed
            sys.stdout.write("\n")
            return "".join(password_chars)
        elif key_pressed in (8, 127):  # i.e. Backspace or Delete key is pressed
            # Erase previous character
            if len(password_chars) > 0:
                sys.stdout.write("\b \b")  # \b doesn't erase the character, it just moves the cursor back.
                sys.stdout.flush()
                password_chars = password_chars[:-1]
        elif 0 <= key_pressed <= 31:
            # Do nothing for Non-Printable keys (e.g. esc, alt, etc.)
            pass
        elif key_pressed == 224:  # Means special key triggered (i.e. arrow keys, home, etc.)
            special_key = ord(get_char())
            if special_key == 83:  # Delete Key Pressed
                # Erase previous character
                if len(password_chars) > 0:
                    sys.stdout.write("\b \b")  # \b doesn't erase the character, it just moves the cursor back.
                    sys.stdout.flush()
                    password_chars = password_chars[:-1]
        else:
            char = chr(key_pressed)
            sys.stdout.write(mask_char)
            sys.stdout.flush()
            password_chars.append(char)
