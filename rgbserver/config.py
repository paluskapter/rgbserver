import board
import neopixel


class Config:
    PORT = 80
    SQS_URL = ""
    AWS_REGION = ""
    AWS_KEY = ""
    AWS_SECRET = ""
    GPIO = board.D18
    LENGTH = 300
    BRIGHTNESS = 1
    AUTO_WRITE = False
    ORDER = neopixel.GRB
