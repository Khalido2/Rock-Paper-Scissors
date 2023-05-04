
import cv2
import mediapipe as mp
import numpy as np
from tensorflow import keras

class ML_API():

        def __init__(self):
            super().__init__()
            self.ANNOTATED_IMAGE_OUTPUT_FILENAME = "src/main/resources/annotation.jpg"

            self.mp_hands = mp.solutions.hands #get set up vars for mediapipe
            self.hands = self.mp_hands.Hands()
            self.mp_draw = mp.solutions.drawing_utils
            self.rps_model = keras.models.load_model('src/main/resources/rps_model') #load cnn from file
            

        def draw_hand_trackers(self, img_path):
            image = cv2.imread(img_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #convert image to rgb
            results = self.hands.process(image) #identify hand landmarks in image
            if results.multi_hand_landmarks: #if a hand was detected
                handLms = results.multi_hand_landmarks[0] #get just the first hand
                self.mp_draw.draw_landmarks(image, handLms, self.mp_hands.HAND_CONNECTIONS) #draw connections between finger points
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #currently image given is already rgb
                cv2.imwrite(self.ANNOTATED_IMAGE_OUTPUT_FILENAME, image) #save annotated image
                return self.ANNOTATED_IMAGE_OUTPUT_FILENAME #return path to annotated image
            else:
                return img_path #if no hands just return original image


        #Generates grid for hand
        def generate_grid(self, detected_landmarks):
            size = 100 #grid is 100 by 100
            grid = np.zeros((size,size))
            handLms = detected_landmarks.multi_hand_landmarks[0] #get just the first hand

            for id, lm in enumerate(handLms.landmark): #for each hand landmark
                x = int(lm.x * (size-1)) #make it val between 0 and 100
                y = int(lm.y * (size-1))

                if (x > 100 or x < 0) or (y > 100 or y < 0):
                    continue #skip this iteration if finger tracking point is out of bounds
                grid[y][x] = 1 #set index of tracking maker as 1

            return grid


        #Given image of player hand, determine their move and return the result
        def detect_player_move(self, img_path):
            image = cv2.imread(img_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #convert image to rgb
            results = self.hands.process(image) #identify hand landmarks in image

            if results.multi_hand_landmarks: #if a hand was detected
                grid = self.generate_grid(results)
                prediction = self.rps_model.predict(grid.reshape(1,100,100,1)) #predict what move it was
                return prediction.argmax() #get class model is most confident in

            else:
                return -1 #if no hand detected then return -1
