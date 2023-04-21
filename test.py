import cv2

cam = cv2.VideoCapture(0) #get video feed from webcam

while True:
    success, image = cam.read() #read from cam
    cv2.imshow('input', image)
    c = cv2.waitKey(1) #show image for 1 second
    if c == 27:
        break

cam.release()
cv2.destroyAllWindows()
