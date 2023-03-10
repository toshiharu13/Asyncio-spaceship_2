import asyncio
import curses
import os
import random
import time

from space_ship_fly import animate_spaceship
from space_garbage import fly_garbage

TIC_TIMEOUT = 0.1
ROCKET_FRAMES = 'frames/rocket'

GARBAGE_FRAMES = {
    'duck': 'frames/duck/duck_frame.txt',
    'hubble': 'frames/hubble/hubble_frame.txt',
    'lamp': 'frames/lamp/lamp_frame.txt',
    'trash_large': 'frames/trash_large/trash_large_frame.txt',
    'trash_small': 'frames/trash_small/trash_small_frame.txt ',
    'trash_xl': 'frames/trash_xl/trash_xl_frame.txt',
}


def get_frame_from_file(file_name, frame_folder):
    frame_file = os.path.join(frame_folder, file_name)
    with open(frame_file, 'r') as file:
        return file.read()


def generate_stars(width, height, value=50):
    for star in range(value):
        column = random.randint(1, width - 2)
        raw = random.randint(1, height - 2)
        symbol = random.choice(['+', '*', '.', ':'])
        yield column, raw, symbol


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    height, width = canvas.getmaxyx()

    frame_filenames = os.listdir(ROCKET_FRAMES)
    frames = (get_frame_from_file(frame_filename, ROCKET_FRAMES) for frame_filename in frame_filenames)

    coroutines = [
        blink(canvas, raw, column, symbol, random.randint(0, 3)) for column, raw, symbol in generate_stars(width, height)
    ]
    # TODO add shutting func

    coroutines.append(
        animate_spaceship(canvas, frames, height / 2, width / 2, height, width))

    random_garbage = random.choice(list(GARBAGE_FRAMES.values()))
    with open(random_garbage, 'r') as garbage_file:
        frame = garbage_file.read()
    coroutines.append(fly_garbage(canvas, 10, frame))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()

        time.sleep(TIC_TIMEOUT)


def add_offset(count):
    if count >= 3:
        return 0
    return count + 1


async def blink(canvas, row, column, symbol='*', offset=0):
    while True:
        if offset == 0:
            canvas.addstr(row, column, symbol, curses.A_DIM)
            for tic in range(20):
                await asyncio.sleep(0)
            offset = add_offset(offset)
        if offset == 1:
            canvas.addstr(row, column, symbol)
            for tic in range(3):
                await asyncio.sleep(0)
            offset = add_offset(offset)
        if offset == 2:
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            for tic in range(5):
                await asyncio.sleep(0)
            offset = add_offset(offset)
        if offset == 3:
            canvas.addstr(row, column, symbol)
            for tic in range(3):
                await asyncio.sleep(0)
            offset = add_offset(offset)


if __name__ == '__main__':
    curses.wrapper(draw)
    curses.update_lines_cols()
