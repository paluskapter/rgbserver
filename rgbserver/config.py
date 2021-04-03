import json

import board


class Config:
    def __init__(self, path):
        with path.open(mode='r') as file:
            config = json.load(file)
        self.port = config["port"]
        self.gpio = getattr(board, "D" + str(config["gpio"]))
        self.length = config["length"]
        self.order = config["order"]
        self.sqs_url = config["sqs_url"]
        self.aws_region = config["aws_region"]
        self.aws_key = config["aws_key"]
        self.aws_secret = config["aws_secret"]
