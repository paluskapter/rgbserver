import itertools
from itertools import chain
from random import randint
from time import sleep
from typing import List, Tuple

import neopixel
from webcolors import name_to_rgb

from config import Config
from util import *


class RGBController:
    def __init__(self, conf: Config):
        self.length = conf.length
        self.pixels = neopixel.NeoPixel(conf.gpio, conf.length, brightness=1, auto_write=False, pixel_order=conf.order)

    def __del__(self):
        self.pixels.deinit()

    def clear(self, state):
        """Clears the strip one by one."""
        self.static_color_list(state[0]['colors'])
        self.color_wipe(state, (0, 0, 0))

    def fire(self, state):
        """Fire effect."""
        while True:
            for i in chain(range(40), range(self.length - 25, self.length)):
                self.pixels[i] = (randint(180, 255), 0, 0)

            for i in range(40, self.length - 25):
                self.pixels[i] = (
                    randint(180, 255),
                    randint(10, 50) if random() > 0.7 else 0,
                    0)
            self.pixels.show()
            self.save_state(state)
            sleep(randint(100, 200) / 1000.0)

    def rainbow(self, state, wait_ms: int = 0):
        """Whole rainbow moves across the strip."""
        while True:
            for j in range(255):
                for i in range(self.length):
                    pixel_index = (i * 256 // self.length) + j
                    self.pixels[i] = rainbow_wheel(pixel_index & 255)
                self.pixels.show()
                self.save_state(state)
                sleep(wait_ms / 1000.0)

    def rainbow_color_wipe(self, state):
        """Wipe 12 colors across display a pixel at a time."""
        for color in itertools.cycle(RAINBOW):
            self.color_wipe(state, color, 10)

    def rainbow_fade(self, state, brightness: int = 255):
        """Fades between all the colors in the rainbow."""
        color_generator = rainbow_color_generator(brightness)
        wait = int((-1 / 5.0 * brightness) + 50) if brightness <= 200 else 10

        for r, g, b in color_generator:
            self.static_color(state, r, g, b, wait)
            self.save_state(state)

    def random_fade(self, state):
        """Randomly fades between colors."""
        old_r, old_g, old_b = random_color()
        self.static_color(state, old_r, old_g, old_b)

        while True:
            new_r, new_g, new_b = random_color()

            dist_r = old_r - new_r
            dist_g = old_g - new_g
            dist_b = old_b - new_b

            steps = max(abs(dist_r), abs(dist_g), abs(dist_b))

            step_r = (steps / float(abs(dist_r))) if dist_r != 0 else 999
            step_g = (steps / float(abs(dist_g))) if dist_g != 0 else 999
            step_b = (steps / float(abs(dist_b))) if dist_b != 0 else 999

            for i in range(1, steps + 1):
                if i % step_r < 1:
                    old_r = (old_r - 1) if dist_r > 0 else old_r + 1
                if i % step_g < 1:
                    old_g = (old_g - 1) if dist_g > 0 else old_g + 1
                if i % step_b < 1:
                    old_b = (old_b - 1) if dist_b > 0 else old_b + 1
                self.static_color(state, old_r, old_g, old_b, 10)
                self.save_state(state)

    def snake(self, state, method="color"):
        """
        Snake implementation for all 3 methods:
        color: Snake with changing color.
        fade: Snake with continuously changing color.
        rainbow: Snake with the whole rainbow.
        """
        start = 0
        length = 48
        direction = False
        count = itertools.count()
        normal_color = None
        fade_color_gen = rainbow_color_generator(255)
        while True:
            r, g, b = next(fade_color_gen)
            fade_color = (r, g, b)

            if start == self.length - length or start == 0:
                direction = not direction
                normal_color = RAINBOW[next(count) % 12]

            for i in chain(range(start), range(start + length, self.length)):
                self.pixels[i] = (0, 0, 0)

            for i in range(start, start + length):
                color = normal_color if method == "color" else fade_color if method == "fade" else RAINBOW[
                    int((i - start) / 4)]
                self.pixels[i] = color

            if direction:
                start += 1
            else:
                start -= 1

            self.pixels.show()
            self.save_state(state)
            sleep(0.01)

    def static_color(self, state, r: int, g: int, b: int, wait_ms: int = 0):
        """Switches color of the whole strip."""
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            self.pixels.fill((r, g, b))
            self.pixels.show()
            self.save_state(state)
            sleep(wait_ms / 1000.0)
        else:
            self.show_error()

    def static_color_name(self, state, name, wait_ms=0):
        """Switches color of the whole strip by name."""
        try:
            (red, green, blue) = name_to_rgb(name)
            self.static_color(state, red, green, blue, wait_ms)
        except ValueError:
            self.show_error()

    def static_gradient(self, state, c1, c2):
        """Gradient between 2 colors."""
        if all([0 <= i <= 255 and 0 <= j <= 255 for i in c1 for j in c2]):
            for i in range(self.length):
                self.pixels[i] = gradient_color(i, c1, c2, self.length)
            self.pixels.show()
            self.save_state(state)
        else:
            self.show_error()

    def strobe(self, state, wait_ms=300):
        """Strobe effect."""
        while True:
            r, g, b = random_color()
            self.static_color(state, r, g, b, wait_ms)
            self.save_state(state)

    def color_wipe(self, state, color: Tuple[int, int, int], wait_ms: int = 0):
        """Wipe color across display a pixel at a time."""
        for i in range(self.length):
            self.pixels[i] = color
            self.pixels.show()
            self.save_state(state)
            sleep(wait_ms / 1000.0)

    def save_pixels(self):
        """Saves current pixel colors."""
        return [self.pixels[i] for i in range(self.length)]

    def save_state(self, state):
        """Saves the state of the strip between processes."""
        d = state[0]
        d['colors'] = self.save_pixels()
        state[0] = d

    def static_color_list(self, color: List[Tuple[int, int, int]], wait_ms: int = 0):
        """Instantly switches color from a list of colors."""
        for i in range(self.length):
            self.pixels[i] = color[i]
        self.pixels.show()
        sleep(wait_ms / 1000.0)

    def show_error(self):
        """Flashes red twice."""
        colors = self.save_pixels()
        for i in range(2):
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
            sleep(0.1)
            self.pixels.fill((255, 0, 0))
            self.pixels.show()
            sleep(0.1)

        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        sleep(0.1)
        self.static_color_list(colors)
