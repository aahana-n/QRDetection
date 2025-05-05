import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

scanned_codes = set()

def is_duplicate(data):
    with open("mydata.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if data in line:
                scanned_codes.add(data)
                return True
    return False

def write_to_text(data):
    if not is_duplicate(data):
        with open("mydata.txt", "a") as file:
            file.write(f"{data}\n")
            scanned_codes.add(data)
            print(f"{data} Data saved successfully")
            

while True: 
    success, img = cap.read()
    for qrcode in decode(img):
        myData = qrcode.data.decode('utf-8')

        write_to_text(myData)

        pts = np.array([qrcode.polygon], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img, [pts], True, (0,255,0),5)

        x, y, w, h = qrcode.rect
        cv2.putText(img, myData, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(0,255,0),2)
    cv2.imshow("QR detection", img)
    cv2.waitKey(1)

cap.release()



