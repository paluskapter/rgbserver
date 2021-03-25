from multiprocessing import Process
from multiprocessing.managers import SyncManager

from flask import Flask, render_template

from control import RGBController

app = Flask(__name__)
rgb = RGBController()
proc = Process()

manager = SyncManager()
manager.start()
state = manager.list()
state.append({})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clear')
def clear():
    start_process(rgb.clear)
    return 'clear'


@app.route('/fire')
def fire():
    start_process(rgb.fire)
    return 'fire'


@app.route('/rainbow')
@app.route('/rainbow/<int:wait_ms>')
def rainbow(wait_ms=0):
    start_process(rgb.rainbow, (wait_ms,))
    return 'rainbow'


@app.route('/rainbow_color_wipe')
def rainbow_color_wipe():
    start_process(rgb.rainbow_color_wipe)
    return 'rainbow_color_wipe'


@app.route('/rainbow_fade')
def rainbow_fade():
    start_process(rgb.rainbow_fade)
    return 'rainbow_fade'


@app.route('/random_fade')
def random_fade():
    start_process(rgb.random_fade)
    return 'random_fade'


@app.route('/snake_color')
def snake_color():
    start_process(rgb.snake, ("color",))
    return 'snake_color'


@app.route('/snake_fade')
def snake_fade():
    start_process(rgb.snake, ("fade",))
    return 'snake_fade'


@app.route('/snake_rainbow')
def snake_rainbow():
    start_process(rgb.snake, ("rainbow",))
    return 'snake_rainbow'


@app.route('/static_color/<int:red>/<int:green>/<int:blue>')
def static_color(red, green, blue):
    rgb.static_color(red, green, blue)
    return 'static_color'


@app.route('/static_color_name/<name>')
def static_color_name(name):
    rgb.static_color_name(name)
    return 'static_color_name'


@app.route('/static_gradient/<int:r1>/<int:g1>/<int:b1>/<int:r2>/<int:g2>/<int:b2>')
def static_gradient(r1, g1, b1, r2, g2, b2):
    rgb.static_gradient((r1, g1, b1), (r2, g2, b2))
    return 'static_gradient'


@app.route('/strobe')
@app.route('/strobe/<int:wait_ms>')
def strobe(wait_ms=300):
    start_process(rgb.strobe, (wait_ms,))
    return 'strobe'


def start_process(func, args=()):
    global proc, state
    proc = Process(target=func, args=(state,) + args)
    proc.start()


@app.before_request
def stop_process():
    global proc
    if proc.pid is not None:
        proc.terminate()
        proc.join()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
