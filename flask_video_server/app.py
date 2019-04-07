# INSTRUCTIONS:
# run app.py, go to http://localhost:5000/

#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from base_camera import BaseCamera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    """video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """video streaming route, put in src attribute of an img tag"""
    return Response(gen(BaseCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    """video streaming route, put in src attribute of an img tag"""
    return Response(gen(BaseCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.0.5', threaded=True)
