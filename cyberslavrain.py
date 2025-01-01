#!/usr/bin/env python3

import random
import curses
import time

YELLOW_COLOR = 4
ORANGE_COLOR = 167
BLACK_COLOR = 1

def get_window_dimensions(window):
    height, width = window.getmaxyx()
    return height - 2, width - 1

def initialize_rain_drops(screen_width, screen_height):
    drop_heights = [
        random.randrange(screen_height // 3 - 4, screen_height // 2 - 4)
        for _ in range(screen_width)
    ]
    
    drop_starting_positions = [i % (screen_height + 1) for i in range(screen_width)]

    for _ in range(random.randrange(1, 5)):
        random.shuffle(drop_starting_positions)
    
    return drop_heights, drop_starting_positions

def setup_colors():
    curses.start_color()
    curses.use_default_colors()
    
    for i in range(0, curses.COLORS): curses.init_pair(i + 1, i, -1)

def draw_rain_drop(window, row, col, drop_starting_positions, drop_heights, char, screen_height):
    start_pos = drop_starting_positions[col]
    length = drop_heights[col]
    row_mod_height = row % screen_height

    color = curses.color_pair(BLACK_COLOR)
    style = curses.A_DIM

    if row_mod_height == start_pos:
        window.addstr(0, col, char, curses.color_pair(ORANGE_COLOR) + curses.A_BOLD)
    elif row > start_pos:
        char_to_print = char

        if row_mod_height in {(start_pos + i) % screen_height for i in range(1, 3)}:
            color = curses.color_pair(YELLOW_COLOR)
            style = curses.A_BOLD
        elif row_mod_height == (start_pos + 3) % screen_height and random.randrange(2):
            color = curses.color_pair(YELLOW_COLOR)
            style = curses.A_BOLD
        elif row_mod_height in {start_pos + length - i for i in range(0, 3)}:
            color = curses.color_pair(YELLOW_COLOR)
            style = curses.A_DIM
        else:
            char_to_print = " "

        window.addstr(0, col, char_to_print, color + style)

        if char_to_print == " ":
            target_value = row_mod_height - (start_pos % screen_height)

            if target_value < 0: target_value += screen_height

            if 3 <= target_value < length:
                window.addstr(0, col, char, curses.color_pair(YELLOW_COLOR))

    else:
        window.addstr(0, col, " ", color + style)

def main(window):
    try:
        screen_height, screen_width = get_window_dimensions(window)
        drop_heights, drop_starting_positions = initialize_rain_drops(screen_width, screen_height)
        setup_colors()
        curses.curs_set(0)

        row = 0
        while True:
            for col in range(screen_width):
                char = random.choice("ЦЮДФОЖЮБЩШѦѪѢ")
                draw_rain_drop(window, row, col, drop_starting_positions, drop_heights, char, screen_height)

            window.refresh()
            window.insertln()

            time.sleep(0.1)

            row += 1

    except KeyboardInterrupt:
        pass

    finally:
        curses.endwin()
        curses.curs_set(1)

if __name__ == '__main__':
    curses.wrapper(main)
