from flask import request, render_template
from flask import Blueprint
from flask import render_template
from flask.wrappers import Response

from imutils.video import VideoStream
import imutils
import cv2
from cv2 import VideoCapture

import multiprocessing
import concurrent.futures
import time

webcv = Blueprint('Webcv', __name__,
                  template_folder='../templates/webcv', url_prefix='/cv')

outputFrame = None
# lock = threading.Lock()
lock = multiprocessing.Lock()
vs = None

# blueprint init
@webcv.record_once
def cvinit(state):
    cvapp = state.app
    global vs, video_name
    video_name = cvapp.config['VIDEO_SOURCE']

# dash board


@webcv.route('/dash')
def dash():
    return render_template('cv.html')

# main video process reae file form config.py
# VIDEO_SOURCE flags
def gen_can_frames(num):

    vs = VideoCapture(video_name)

    while True:
        (flag, frames) = vs.read()
        frames = cv2.resize(frames, (400, 200))

        with lock:
            outputFrame = frames.copy()
            if outputFrame is None:
                continue

            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            if not flag:
                continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')

        time.sleep(0.05)


# main page of video
@webcv.route("/video")
def vid():
    global pageargs
    pageargs = request.args.get('num', default=1, type=int)
    print("pageargs : ", pageargs)
    return render_template("video.html")

# create multiprocess
# using gen_can_frams -> create multi video process
def motion():
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        cam_proc = {executor.submit(
            gen_can_frames, num): num for num in range(1, pageargs+1)}
        try:
            res = cam_proc.result()
        except Exception as exc:
            print("error")


@webcv.route("/video_feed")
def video_feed():
    # reaponse image src (/cv/video_feed?num=?)
    cam_num = request.args.get('num', type=int)
    print("responce :", cam_num)
    return Response(gen_can_frames(cam_num), mimetype="multipart/x-mixed-replace; boundary=frame")


@webcv.route("/video_stop")
def video_stop():
    return 0
