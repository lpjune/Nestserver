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
    from camera import Camera

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


"""video streaming generator function."""
def cam_gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


"""video streaming routes"""
@app.route('/video_feed1')
def video_feed1():
    
    return Response(cam_gen(Camera(0)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(cam_gen(Camera(1)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    


if __name__ == '__main__':
    app.run(host='192.168.0.100', threaded=True)


