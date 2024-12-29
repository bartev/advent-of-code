Point = tuple[int, int]

numeric_keypad = {
    # "gap": (3, 0),
    "0": (3, 1),
    "A": (3, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}

arrow_keypad = {
    # "gap": (0, 0),
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


# Does not work for the final solution
def dpoint(start: str, end: str, keypad) -> Point:
    """Find the moves needed to go from start to end in terms of ^, >, v, <"""
    start_row, start_col = keypad[start]
    end_row, end_col = keypad[end]
    d_row, d_col = end_row - start_row, end_col - start_col
    x_char = "<" if d_col < 0 else ">" if d_col > 0 else ""
    y_char = "^" if d_row < 0 else "v" if d_row > 0 else ""
    if end_col == 0:  # Avoid the empty space in col 1
        # move to right row first
        move_str = y_char * abs(d_row) + x_char * abs(d_col)
    else:
        # move to right column first
        move_str = x_char * abs(d_col) + y_char * abs(d_row)
    return move_str + "A"


# Does not work for the final solution
def process_doorcode(code: str):
    """Process a single doorcode
    Get arrow codes to press the numbers on the numeric keypad
    code is like '029A'
    """
    # from_a = "A" + code
    key_paths_1 = zip("A" + code, code)
    robot_1_buttons = "".join(
        [dpoint(start, end, numeric_keypad) for start, end in key_paths_1]
    )
    key_paths_2 = zip("A" + robot_1_buttons, robot_1_buttons)
    robot_2_buttons = "".join(
        [dpoint(start, end, arrow_keypad) for start, end in key_paths_2]
    )
    key_paths_3 = zip("A" + robot_2_buttons, robot_2_buttons)
    my_buttons = "".join(
        [dpoint(start, end, arrow_keypad) for start, end in key_paths_3]
    )
    return robot_1_buttons, robot_2_buttons, my_buttons
