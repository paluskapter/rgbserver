import board
import neopixel


class Config:
    GPIO = board.D18
    LENGTH = 300
    BRIGHTNESS = 1
    AUTO_WRITE = False
    ORDER = neopixel.GRB
