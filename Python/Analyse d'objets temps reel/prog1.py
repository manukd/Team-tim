from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera(0)
camera.resolution = (800,608)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(800,608))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
    image = frame.array
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
