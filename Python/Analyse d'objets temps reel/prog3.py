import numpy as np
import os
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.SetCaptureProperty(cap,cv2.CV_CAP_PROP_FRAME_WIDTH,1280)
    cv2.SetCaptureProperty(cap,cv2.CV_CAP_PROP_FRAME_HEIGHT,)

    cv2.imshow('frame',0)    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cap.release()
    cv2.destroyAllWindows