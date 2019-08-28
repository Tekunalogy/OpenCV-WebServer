from flask import Flask, render_template, Response
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from camera import VideoCamera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/valueofslider')
def slide(self):
    a = self.request.args.get('a')
    print(a)


@app.route('/test/', methods=['GET', 'POST'])
def test(self):
    if self.request.method == "POST":
        value = self.request.json['data']
        print(value)
    return render_template('roundslider1.html')


if __name__ == '__main__':
    app.run(host='lightbar.local', port=5807, debug=True, threaded=True)
