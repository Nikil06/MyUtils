from MY_INPUT_v2 import start_keyboard_thread, stop_keyboard_thread
import MY_INPUT_v2.key_map as key_map

exit_program = False

def handle_input(_key):
    global cookie_count, count_changed, exit_program

    key, state = _key

    if key == key_map.SMALL_Q:
        stop_keyboard_thread(k_thread)
        exit_program = True
    elif key == key_map.SMALL_C:
        cookie_count += 1
        count_changed = True

if __name__ == "__main__":
    k_thread = start_keyboard_thread(handle_input)

    cookie_count = 0
    count_changed = False

    print("Cookie count :", cookie_count, end="\r")
    while not exit_program:
        if count_changed:
            print("Cookie count :", round(cookie_count, 2), end="\r")
            count_changed = False
