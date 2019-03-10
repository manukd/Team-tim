import picamera
import picamera.array

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as output:
        camera.resolution = (1280,600)
        #camera.capture_continuous(output, 'rgb')
for frame in camera.capture_continuous(output, format="rgb", use_video_port=True):
    image = frame.array
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
      