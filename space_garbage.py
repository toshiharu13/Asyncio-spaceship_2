from curses_tools import draw_frame, get_frame_size
import asyncio
import random

async def fly_garbage(canvas, column, garbage_frame, speed=0.5,  y_max=10, x_max=10):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    # NOT IN USE
    rows_number, columns_number = canvas.getmaxyx()
    border_size = 1
    garbage_size_y, garbage_size_x = get_frame_size(garbage_frame)
    rows_number = rows_number - garbage_size_y - border_size
    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = border_size

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas, garbage_frames, speed=0.5):
    border_size = 2

    while True:
        awaiting_time = random.randint(0, 25)
        for _ in range(awaiting_time):
            await asyncio.sleep(1)
        random_garbage_file_name = random.choice(garbage_frames)
        with open(random_garbage_file_name, 'r') as garbage_file:
            random_garbage_frame = garbage_file.read()

        rows_number, columns_number = canvas.getmaxyx()
        garbage_size_y, garbage_size_x = get_frame_size(random_garbage_frame)
        column = random.randint(2 + garbage_size_x, columns_number - 2 - garbage_size_x)
        rows_number = rows_number - garbage_size_y - border_size
        column = max(column, 0)
        column = min(column, columns_number - 1)

        row = border_size

        while row < rows_number:
            draw_frame(canvas, row, column, random_garbage_frame)
            canvas.refresh()
            await asyncio.sleep(0.2)
            draw_frame(canvas, row, column, random_garbage_frame, negative=True)
            row += speed
