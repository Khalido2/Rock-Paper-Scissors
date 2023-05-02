# Rock-Paper-Scissors
 
A rock paper scissors game where you play against the computer

Packages required for project: check build.gradle file

Still in development. The main elements of the project (i.e. mediapipe that detects and tracks player's hands and the tensorflow model (CNN) that classifies the generated grids of tracking points into moves) are all written in
python in the ml_api.py script. The whole project has been wrapped in Java in order to provide a more flexible and prettier GUI using JavaFX rather than the python options.

Currently only the start screen and play screen are implemented