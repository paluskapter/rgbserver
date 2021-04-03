import sys
from multiprocessing import Process
from multiprocessing.managers import SyncManager
from typing import Any, Callable, List, Optional, Tuple

import boto3
import requests
from flask import Flask, render_template

from config import Config
from control import RGBController


class Webserver(Flask):
    def __init__(self, location: str) -> None:
        super().__init__(__name__)
        self.rgb_config = Config(location)
        self.rgb = RGBController(self.rgb_config)
        self.proc = Process()
        self.manager = SyncManager()
        self.manager.start()
        self.state: List[Tuple[int, int, int]] = self.manager.list()

        self.before_request(self.stop_process)
        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/clear', view_func=self.clear)
        self.add_url_rule('/fire', view_func=self.fire)
        self.add_url_rule('/rainbow', view_func=self.rainbow)
        self.add_url_rule('/rainbow_color_wipe', view_func=self.rainbow_color_wipe)
        self.add_url_rule('/rainbow_fade', view_func=self.rainbow_fade)
        self.add_url_rule('/random_fade', view_func=self.random_fade)
        self.add_url_rule('/snake_color', view_func=self.snake_color)
        self.add_url_rule('/snake_fade', view_func=self.snake_fade)
        self.add_url_rule('/snake_rainbow', view_func=self.snake_rainbow)
        self.add_url_rule('/static_color/<int:red>/<int:green>/<int:blue>', view_func=self.static_color)
        self.add_url_rule('/static_color_name/<name>', view_func=self.static_color_name)
        self.add_url_rule('/static_gradient/<int:r1>/<int:g1>/<int:b1>/<int:r2>/<int:g2>/<int:b2>',
                          view_func=self.static_gradient)
        self.add_url_rule('/strobe', view_func=self.strobe)

    def run(self, host: str = None, port: int = None, debug: bool = None, load_dotenv: bool = True,
            **options: Optional[Any]) -> None:
        if self.rgb_config.sqs_url:
            reader = Process(target=self.sqs_reader, args=())
            reader.start()

        super().run('0.0.0.0', self.rgb_config.port, debug, load_dotenv, **options)

    @staticmethod
    def index() -> str:
        return render_template('index.html')

    def clear(self) -> str:
        self.start_process(self.rgb.clear)
        return 'clear'

    def fire(self) -> str:
        self.start_process(self.rgb.fire)
        return 'fire'

    def rainbow(self) -> str:
        self.start_process(self.rgb.rainbow)
        return 'rainbow'

    def rainbow_color_wipe(self) -> str:
        self.start_process(self.rgb.rainbow_color_wipe)
        return 'rainbow_color_wipe'

    def rainbow_fade(self) -> str:
        self.start_process(self.rgb.rainbow_fade)
        return 'rainbow_fade'

    def random_fade(self) -> str:
        self.start_process(self.rgb.random_fade)
        return 'random_fade'

    def snake_color(self) -> str:
        self.start_process(self.rgb.snake, ("color",))
        return 'snake_color'

    def snake_fade(self) -> str:
        self.start_process(self.rgb.snake, ("fade",))
        return 'snake_fade'

    def snake_rainbow(self) -> str:
        self.start_process(self.rgb.snake, ("rainbow",))
        return 'snake_rainbow'

    def static_color(self, red: int, green: int, blue: int) -> str:
        self.start_process(self.rgb.static_color, (red, green, blue))
        return 'static_color'

    def static_color_name(self, name: str) -> str:
        self.start_process(self.rgb.static_color_name, (name,))
        return 'static_color_name'

    def static_gradient(self, r1: int, g1: int, b1: int, r2: int, g2: int, b2: int) -> str:
        self.start_process(self.rgb.static_gradient, ((r1, g1, b1), (r2, g2, b2)))
        return 'static_gradient'

    def strobe(self) -> str:
        self.start_process(self.rgb.strobe)
        return 'strobe'

    def start_process(self, func: Callable, args: Tuple = ()) -> None:
        self.proc = Process(target=func, args=(self.state,) + args)
        self.proc.start()

    def stop_process(self) -> None:
        if self.proc.pid is not None:
            self.proc.terminate()
            self.proc.join()

    def sqs_reader(self) -> None:
        client = boto3.client('sqs', region_name=self.rgb_config.aws_region,
                              aws_access_key_id=self.rgb_config.aws_key,
                              aws_secret_access_key=self.rgb_config.aws_secret)
        while True:
            response = client.receive_message(QueueUrl=self.rgb_config.sqs_url, AttributeNames=[],
                                              MessageAttributeNames=[],
                                              MaxNumberOfMessages=1, VisibilityTimeout=30, WaitTimeSeconds=20)
            if 'Messages' in response:
                message = response['Messages'][0]
                requests.get("http://localhost:" + str(self.rgb_config.port) + "/" + message['Body'])
                client.delete_message(QueueUrl=self.rgb_config.sqs_url, ReceiptHandle=message['ReceiptHandle'])


def main() -> None:
    if len(sys.argv) != 2:
        exit("The only parameter needed is the json config file's absolute path!")
    Webserver(sys.argv[1]).run()


if __name__ == "__main__":
    main()
