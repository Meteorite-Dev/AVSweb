from re import L
from flask import request, render_template
from flask import Blueprint
from flask import render_template
from flask.wrappers import Response

import cv2
from cv2 import VideoCapture

import multiprocessing
import time
from os import walk

webcv = Blueprint('Webcv', __name__,
                  template_folder='../templates/webcv', url_prefix='/cv')

outputFrame = None
lock = multiprocessing.Lock()
vs = None


# blueprint init
@webcv.record_once
def cvinit(state):
    cvapp = state.app
    global vs, video_name, video_dir, vd_mode
    video_name = cvapp.config['VIDEO_SOURCE']
    video_dir = cvapp.config['VIDEO_SOURCE_DIR']
    vd_mode = cvapp.config['VIDEO_DIR_MODE']

# dash board


@webcv.route('/dash')
def dash():
    return render_template('cv.html')

# video walk


def video_dir_walk():
    vfiles = []
    for root, dirs, files in walk(video_dir, topdown=False):
        for fi in files:
            vfiles.append(str(root+"/"+fi))

    print(vfiles)
    return vfiles


# main video process reae file form config.py
# VIDEO_SOURCE flags
def gen_can_frames(vname):
    if vd_mode:
        vs = VideoCapture(vname)
    else:
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
    return render_template("video.html")


@webcv.route("/video_feed")
def video_feed():
    # reaponse image src (/cv/video_feed?num=?)
    cam_num = request.args.get('num', type=int)
    print("responce :", cam_num)
    vdn = video_dir_walk()
    print(vdn[cam_num-1])
    return Response(gen_can_frames(vdn[cam_num-1]), mimetype="multipart/x-mixed-replace; boundary=frame")
