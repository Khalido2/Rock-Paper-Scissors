#open cv
#metaplot
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np

def arrThreshold(arr, threshold, maxVal):
    height = len(arr)
    width = len(arr[0])
    for i in range(height):
        for j in range(width):
            if(arr[i][j] > threshold):
                arr[i][j] = maxVal
            else:
                arr[i][j] = 0
    return arr

#returns numpy array
def imageDiff(img1, img2):
    height, width = img1.shape[:2]
   # diff = np.zeros((height, width))
    diff=[ [0]*(width-1) for i in range(height-1)]
    for i in range(height-1):
        for j in range(width-1):
            diff[i][j] = img2[i][j]-img1[i][j]

    return diff

#How do I make a GUI in python?

#Give a warning then take an image before the hand is up then wait a moment give another warning then take an image 
#when hand is up
#then subtract first image from second, then use binary thresholding to make a mask leaving only the hand

cam = cv2.VideoCapture(0) #get video feed from webcam

time.sleep(1)
ret, frame1 = cam.read() #ret is true when frame is read succesfully
print("Taken")

if not ret:
    print("Failed to read")

time.sleep(1)
print("Now for fingers")
time.sleep(0.5)
print("3")
time.sleep(0.5)
print("2")
time.sleep(0.5)
print("1")
time.sleep(0.5)

ret, frame2 = cam.read()
print("Taken")

if not ret:
    print("Failed to read")

gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) #convert RGB images into grayscale as luminosity is most important
gray2= cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

imgDiff = imageDiff(gray1, gray2) #get difference between to images, using first image as a mask to remove the background
resArr = np.array(imgDiff) #convert into numpy array for thresholding function
ret,thresh = cv2.threshold(resArr,127,255,cv2.THRESH_BINARY) #binary threshold to make foreground 1 and background 0
plt.imshow(imgDiff, cmap='gray')
plt.savefig("photo.png")

plt.imshow(thresh, cmap='gray')
plt.savefig("photo2.png")
