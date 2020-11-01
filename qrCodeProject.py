import urllib

import cv2
import numpy as np
from pyzbar.pyzbar import decode
import urllib.request

# img = cv2.imread('qrcode.png')

URL = "http://192.168.1.34:8080/shot.jpg"

with open('myData.text') as f:
    myDataList = f.read().splitlines()

while True:
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print(myData)
        if myData in myDataList:
            myOutput  = 'Authorized.'
            myColor = (0,255,0)

        else:
            myOutput = 'Un-Authorized.'
            myColor = (0, 0, 255)

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
        pts2 = barcode.rect
        cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
    cv2.imshow('IPWebcam', img)

    if cv2.waitKey(1) & 0xFF == 27:
        break
