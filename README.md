# Rock-Paper-Scissors
 
 A rock paper scissors game where you play against the computer

In prototyping phase to determine how to recognise what play the user has made
imageProcessing.py attempts to use image subtraction and binary thresholding to mask out the user's hand but this is a little flawed as it requires you to have a consistent background for the subtraction to work 

finger_grid_generator.py uses mediapipe to track 21 pointer of the detected hand then creates a binary matrix representing the move made (rock, paper or scissors), this script is used to generate the datasets for training and testing in the Datasets folder

gui.py creates the gui for the game (in development)

game_logic handles the game logic for playing the game, handling wins and detecting the player's move (in development)

Packages required for project: opencv2, mediapipe, tensorflow, customtkinter, numpy 