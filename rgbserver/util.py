from colorsys import hls_to_rgb
from random import random
from typing import Generator, List, Tuple

rainbow_list: List[Tuple[int, int, int]] = [
    (255, 0, 0),
    (255, 127, 0),
    (255, 255, 0),
    (127, 255, 0),
    (0, 255, 0),
    (0, 255, 127),
    (0, 255, 255),
    (0, 127, 255),
    (0, 0, 255),
    (127, 0, 255),
    (255, 0, 255),
    (255, 0, 127),
]


def gradient_color(pos: int, c1: Tuple[int, int, int], c2: Tuple[int, int, int], length: int) -> Tuple[int, int, int]:
    """Calculates the color for a given pixel in a gradient effect."""
    return (
        int(pos * (c2[0] - c1[0]) / length + float(c1[0])),
        int(pos * (c2[1] - c1[1]) / length + float(c1[1])),
        int(pos * (c2[2] - c1[2]) / length + float(c1[2])))


def rainbow_wheel(pos: int) -> Tuple[int, int, int]:
    """Generate rainbow colors across 0-255 positions."""
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return r, g, b


def rainbow_color_generator(brightness: int = 255) -> Generator[Tuple[int, int, int], None, None]:
    """Returns an iterator with all the rainbow colors."""
    r = brightness
    g = 0
    b = 0

    yield r, g, b

    while True:
        for i in range(brightness):
            g += 1
            yield r, g, b
        for i in range(brightness):
            r -= 1
            yield r, g, b
        for i in range(brightness):
            b += 1
            yield r, g, b
        for i in range(brightness):
            g -= 1
            yield r, g, b
        for i in range(brightness):
            r += 1
            yield r, g, b
        for i in range(brightness):
            b -= 1
            yield r, g, b


def random_color() -> List[int]:
    """Random color generator."""
    return [int(255 * x) for x in hls_to_rgb(random(), 0.5, 1)]
