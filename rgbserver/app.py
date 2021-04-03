from multiprocessing import Process
from multiprocessing.managers import SyncManager
from pathlib import Path
from typing import Callable, List, Tuple

import boto3
import requests
from flask import Flask, render_template

from config import Config
from control import RGBController

app = Flask(__name__)
config = Config(Path(__file__).parent.parent / "config.json")
rgb = RGBController(config)

proc = Process()
manager = SyncManager()
manager.start()
color_state = manager.list()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clear')
def clear():
    start_process(color_state, rgb.clear)
    return 'clear'


@app.route('/fire')
def fire():
    start_process(color_state, rgb.fire)
    return 'fire'


@app.route('/rainbow')
@app.route('/rainbow/<int:wait_ms>')
def rainbow(wait_ms: int = 0):
    start_process(color_state, rgb.rainbow, (wait_ms,))
    return 'rainbow'


@app.route('/rainbow_color_wipe')
def rainbow_color_wipe():
    start_process(color_state, rgb.rainbow_color_wipe)
    return 'rainbow_color_wipe'


@app.route('/rainbow_fade')
@app.route('/rainbow_fade/<int:brightness>')
def rainbow_fade(brightness: int = 255):
    start_process(color_state, rgb.rainbow_fade, (brightness,))
    return 'rainbow_fade'


@app.route('/random_fade')
def random_fade():
    start_process(color_state, rgb.random_fade)
    return 'random_fade'


@app.route('/snake_color')
def snake_color():
    start_process(color_state, rgb.snake, ("color",))
    return 'snake_color'


@app.route('/snake_fade')
def snake_fade():
    start_process(color_state, rgb.snake, ("fade",))
    return 'snake_fade'


@app.route('/snake_rainbow')
def snake_rainbow():
    start_process(color_state, rgb.snake, ("rainbow",))
    return 'snake_rainbow'


@app.route('/static_color/<int:red>/<int:green>/<int:blue>')
def static_color(red: int, green: int, blue: int):
    start_process(color_state, rgb.static_color, (red, green, blue))
    return 'static_color'


@app.route('/static_color_name/<name>')
def static_color_name(name: str):
    start_process(color_state, rgb.static_color_name, (name,))
    return 'static_color_name'


@app.route('/static_gradient/<int:r1>/<int:g1>/<int:b1>/<int:r2>/<int:g2>/<int:b2>')
def static_gradient(r1: int, g1: int, b1: int, r2: int, g2: int, b2: int):
    start_process(color_state, rgb.static_gradient, ((r1, g1, b1), (r2, g2, b2)))
    return 'static_gradient'


@app.route('/strobe')
@app.route('/strobe/<int:wait_ms>')
def strobe(wait_ms: int = 300):
    start_process(color_state, rgb.strobe, (wait_ms,))
    return 'strobe'


def start_process(state: List[Tuple[int, int, int]], func: Callable, args: Tuple = ()):
    global proc
    proc = Process(target=func, args=(state,) + args)
    proc.start()


@app.before_request
def stop_process():
    global proc
    if proc.pid is not None:
        proc.terminate()
        proc.join()


def sqs_reader(conf: Config):
    client = boto3.client('sqs', region_name=conf.aws_region, aws_access_key_id=conf.aws_key,
                          aws_secret_access_key=conf.aws_secret)
    while True:
        response = client.receive_message(QueueUrl=conf.sqs_url, AttributeNames=[], MessageAttributeNames=[],
                                          MaxNumberOfMessages=1, VisibilityTimeout=30, WaitTimeSeconds=20)
        if 'Messages' in response:
            message = response['Messages'][0]
            requests.get("http://localhost:" + str(conf.port) + "/" + message['Body'])
            client.delete_message(QueueUrl=conf.sqs_url, ReceiptHandle=message['ReceiptHandle'])


if config.sqs_url:
    reader = Process(target=sqs_reader, args=(config,))
    reader.start()

app.run(host='0.0.0.0', port=config.port)
