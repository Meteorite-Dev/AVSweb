from flask import request, render_template, url_for, redirect, flash
from flask import Blueprint
from flask import render_template
from flask.wrappers import Response

from imutils.video import VideoStream
import threading
import argparse
import datetime
import imutils
import time
import cv2

webcv = Blueprint('Webcv', __name__, template_folder='../templates/webcv')

outputFrame = None
lock = threading.Lock()


@webcv.record_once
def cvinit(state):
    cvapp = state.app
    global vs
    print(cvapp.config['VIDEO_SOURCE'])
    vs = VideoStream(src=cvapp.config['VIDEO_SOURCE'], frame=30).start()


@webcv.route('/cv')
def cvt():
    return render_template('cv.html')


def motion():
    global vs, outputFrame, lock

    if vs is None:
        print("vs is none")
    while True:
        
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        with lock:
            outputFrame = frame.copy()


def generate():
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            if outputFrame is None:
                # print("output is none")
                continue

            # encode Frame to JPEG
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            if not flag:
                print("no flag")
                continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')


@webcv.route("/video")
def vid():
    return render_template("video.html")


@webcv.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")
