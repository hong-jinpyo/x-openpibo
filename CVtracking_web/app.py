#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import cv2
# from hough_transform import Camera
from findlineCV import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        # frame_findline = camera.get_frame()
        frame_findline, center_Pos1, center_Pos2 = camera.get_frame()
        frame_findline = cv2.line(frame_findline, (center_Pos1, 440), (center_Pos2, 380), (255,100,0), 5)

        frame = cv2.imencode('.jpg', frame_findline)[1].tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)