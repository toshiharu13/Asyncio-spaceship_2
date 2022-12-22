from curses_tools import draw_frame, get_frame_size
import asyncio

async def fly_garbage(canvas, column, garbage_frame, speed=0.5,  y_max=10, x_max=10):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
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