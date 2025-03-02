# Rock-Paper-Scissors
 
A rock paper scissors game where you play against the computer

Using medapipe the program creates a grid of hand tracking points. This grid is then put into a Convolutional Neural Network (using Tensorflow) which classifies that grid into Rock, Paper of Scissors. The GUI is built using JavaFX. The mediapipe and Tensorflow segments are written in python and wrapped in a Java gradle project.

Currently the Neural Network only has a 90% accuracy on the test set and has a tendency to misclassify Rock. It was trained on 200 examples of each class and tested on 20 examples of each. See the confusion matrix for more details. 
![confusion-matrix](https://github.com/Khalido2/Rock-Paper-Scissors/assets/60740437/711fd7d8-53ce-4fcf-98b5-b1a5a96dc908)

Some recorded gameplay:
![Gameplay](https://github.com/Khalido2/Rock-Paper-Scissors/assets/60740437/b0ca9e0f-a652-4176-a150-75ac8b9986aa)

Packages required for project: check build.gradle file

To run project: 
* Install gradle
* Download the repo
* Open a terminal at the path of the repo
* Run the command "gradle build"
* Then run the command "gradle run"

Features to be added:
* Sound fx and music
* Optimise CNN to have greater accuracy
