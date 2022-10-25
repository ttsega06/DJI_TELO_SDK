import cap as cap
import cv2

cp = cv2.VideoCapture(1)

def thresholding(img):
    hsv = cv2.cvtColore(img, cv2.COLOR_BGR2HSV)


while True:
    _, img = cap.read()
    img = cv2.resize(img, (480, 360))
    # img = cv2.flip(img, 0)

    thresholding(img)
    cv2.imshow("Output", img)
    cv2.waitKey()