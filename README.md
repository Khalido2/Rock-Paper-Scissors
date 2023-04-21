# Rock-Paper-Scissors
 
 A rock paper scissors game where you play against the computer

In prototyping phase to determine how to recognise what play the user has made
imageProcessing.py attempts to use image subtraction and binary thresholding to mask out the user's hand but this is a little flawed as it requires you to have a consistent background for the subtraction to work 

handtracker.py attempts to use hand + finger tracking to identify what move user is doing
-currently this script just detects fingers using mediapipe library and prints it to screen