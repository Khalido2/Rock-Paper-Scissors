#THIS SCRIPT GENERATES THE FINGER GRIDS TO USE FOR MAKING THE DATASETS

import cv2
import mediapipe as mp
import numpy as np
import keyboard as key
import sys

#print visual display of grid 
def print_grid(grid):
    height, width = grid.shape
    for i in range(height):
        row = ""
        for j in range(width):
            if(grid[i][j] == 1):
                row = row + "1"
            else:
                row = row + " "
        print(row)



if len(sys.argv) < 2:
    print("Need at least 1 argument (Rock, Paper or Scissors)")
    print("Args should be in order: (Rock, Paper or Scissors) (File Index Number) (Train, Val or Test)")
    quit()

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

dataset_dir = "Datasets/"
output_dir = args[0] #get first argument as directory name to save finger grids to
index_num = 0 #this is the name of the first finger grid number to be saved

if len(args) > 1:
    index_num = int(args[1]) #might be continuing on from a previous run

if len(args) > 2:
    dataset_dir = dataset_dir + args[2] #train/test/val set

output_grids =  "-p" in opts #should print out finger grids as it generates them or not?


cam = cv2.VideoCapture(0) #get video feed from webcam
mp_hands = mp.solutions.hands #prep mediapipe
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

make_grid = False
can_generate = False

print('Press space to generate a grid and q to quit')

while True:
    success, image = cam.read() #read from cam
    cv2.waitKey(1) #show image for 1 second

    if key.is_pressed('q'):
        print("Closing")
        break

    if(not key.is_pressed('space') and not make_grid):
        can_generate = True

    if key.is_pressed('space') and can_generate:
        make_grid = True
        can_generate = False

    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB) #identify hand landmarks in image
    height, width, channel = image.shape #get dimensions of image

    if results.multi_hand_landmarks: #if a hand was detected
        handLms = results.multi_hand_landmarks[0] #get just the first hand
        size = 100 #grid is 100 by 100
        grid = np.zeros((size,size))
    
        for id, lm in enumerate(handLms.landmark): #for each hand landmark

            cx, cy = int(lm.x * width), int(lm.y * height) #get center point of hand landmark
            if id == 8:
                cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED) #circle the index finger

            if make_grid:
                x = int(lm.x * (size-1)) #make it val between 0 and 100
                y = int(lm.y * (size-1)) 
                grid[y][x] = 1

        if make_grid:
            make_grid = False
            np.savetxt(dataset_dir + "/" + output_dir + "/" + str(index_num)+".csv", grid, delimiter=",") #save finger grid
            index_num = index_num + 1
            print("Grid generated")

            if output_grids:
                print_grid(grid)


        mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS) #draw connections between finger points
    
    cv2.imshow("Output", image) #show output on screen
    cv2.waitKey(1)


cam.release()
cv2.destroyAllWindows()



