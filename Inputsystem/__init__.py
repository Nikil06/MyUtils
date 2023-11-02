import key_map
from key_input import get_key, check_for_key_press
import threading

def keyboard_input(stop_thread, handle_input_func):
    """
    Captures keyboard input and passes the received key to the provided handler function.

    Args:
        stop_thread (threading.Event): An event to stop the keyboard input thread.
        handle_input_func (callable): Function to process the received key.

    Returns:
        None
    """
    while not stop_thread.is_set():
        key = get_key()
        handle_input_func(key)  # Pass the key to the input loop function

def start_keyboard_thread(handle_input_func):
    """
    Initiates a separate thread to capture keyboard input and handle it using the provided function.

    Args:
        handle_input_func (callable): Function to process the received key.

    Returns:
        threading.Event: An event controlling the thread; use this to stop the keyboard input.
    """
    if not callable(handle_input_func):
        raise TypeError("'handle_input_func' must be callable (i.e. function)")

    stop_thread = threading.Event()

    input_thread = threading.Thread(target=keyboard_input, args=(stop_thread, handle_input_func))
    input_thread.daemon = True
    input_thread.start()

    return stop_thread  # Return the thread control variable

def stop_keyboard_thread(stop_thread):
    """
    Stops the keyboard input thread by setting the provided event.

    Args:
        stop_thread (threading.Event): An event controlling the keyboard input thread.

    Returns:
        None
    """
    stop_thread.set()  # Set the event to stop the keyboard thread
