from flask import Flask, render_template, Response, flash, request, url_for, redirect, session
import numpy as np
import re
import os
import cv2
from camera import VideoCapture


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template("index2.html")


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCapture()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run()
