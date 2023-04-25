import customtkinter as ctk
import tkinter as tk
from PIL import Image
import threading
import time
import cv2
import mediapipe as mp

class Game(ctk.CTk):
        
        def on_closing(self):
            self.stop_event.set() #set stop event
            self.quit() #destroy all ctk widgets
        
        #Create start frame with start button in centre
        def init_start_frame(self, parent):
            frame = ctk.CTkFrame(parent)
            bt_start = ctk.CTkButton(frame, text="START", font=ctk.CTkFont(size=80, weight="bold"), command=self.start_play_phase)
            bt_start.place(relx=.5, rely=.5,anchor= tk.CENTER)
            return frame
        
        #Create video frame which has webcam vid feed
        def init_video_frame(self, parent):
            self.cam = cv2.VideoCapture(0) #get video feed from webcam
            self.mp_hands = mp.solutions.hands #get set up vars for mediapipe
            self.hands = self.mp_hands.Hands()
            self.mp_draw = mp.solutions.drawing_utils

            video_frame = ctk.CTkFrame(parent) #make frame to hold video feed
            self.video_feed = None #declare video feed variable for later

            self.stop_event = threading.Event()
            self.video_thread = threading.Thread(target=self.video_loop, args=())
            self.wm_protocol("WM_DELETE_WINDOW", self.on_closing) #set callback for when window is closed

            return video_frame

        def start_video_feed(self):
             self.video_thread.start()

        #Stream video feed to frame
        def video_loop(self):
             
             while not self.stop_event.is_set():  
                  success, image = self.cam.read() #read from cam
                  
                  if self.stop_event.is_set():
                       break    
                  
                  # OpenCV represents images in BGR order; however PIL
                  # represents images in RGB order, so we need to swap
                  # the channels, then convert to PIL and ImageTk format
                  tk_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                  tk_image = self.draw_hand_trackers(tk_image) #use media pipe to display tracking elements
                  tk_image = Image.fromarray(tk_image)
                  tk_image = ctk.CTkImage(light_image=tk_image, size=tk_image.size)

                  try:
                    if(self.video_feed is None): 
                        self.video_feed = ctk.CTkLabel(self.video_frame, image=tk_image, text="") #init feed if doesn't exist
                        self.video_feed.place(relx=.5, rely=.5,anchor= tk.CENTER)
                    else:
                        self.video_feed.configure(image=tk_image) #else just update the image
                        self.video_feed.image = tk_image

                    if(self.countdown is None):
                       # self.video_canvas = ctk.CTkCanvas(self.video_frame, bg=self.video_frame._bg_color[0]).create_text(x=)
                       # self.video_canvas.place(relx=.5, rely=.5,anchor= tk.CENTER)
                        self.countdown = ctk.CTkLabel(self.video_frame, text=self.countdown_text, fg_color="transparent", font=ctk.CTkFont(size=100, weight="bold"))
                        self.countdown.place(relx=.5, rely=.5,anchor= tk.CENTER) #display countdown
                    else:
                        self.countdown.configure(require_redraw=True, text=self.countdown_text)
                        self.countdown.text = self.countdown_text
                  except RuntimeError:
                      print("[INFO] caught a RuntimeError") #current solution to unresolved (main thread not in main loop error)
                      break
                  
 

        #Draw hand tracking points on image
        def draw_hand_trackers(self, image):
            results = self.hands.process(image) #identify hand landmarks in image
            if results.multi_hand_landmarks: #if a hand was detected
                handLms = results.multi_hand_landmarks[0] #get just the first hand
    
                #for id, lm in enumerate(handLms.landmark): #for each hand landmark
                    
                    #cx, cy = int(lm.x * width), int(lm.y * height) #get center point of hand landmark
                    #if id == 8:
                    #    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED) #circle the index finger

                self.mp_draw.draw_landmarks(image, handLms, self.mp_hands.HAND_CONNECTIONS) #draw connections between finger points

            return image #return edited image
        

        def set_countdown_text(self, text):
            self.countdown_text = text
        
        def start_play_phase(self):
            self.countdown = None
            self.countdown_text = ""
            self.video_canvas = None

            self.hide_frame(self.start_frame)
            self.display_frame(self.video_frame)
            self.start_video_feed()

            threading.Timer(1, self.set_countdown_text, ["3"]).start()
            threading.Timer(2, self.set_countdown_text, ["2"]).start()
            threading.Timer(3, self.set_countdown_text, ["1"]).start()
            threading.Timer(4, self.set_countdown_text, [""]).start()

            #detect move player made

            #wait a second, then start the count down then one second for detection then move onto next phase

        def display_frame(self, frame):
            frame.pack(fill=tk.BOTH, expand=True)

        def hide_frame(self, frame):
            frame.pack_forget()

        def __init__(self):
            super().__init__()
            DARK_MODE = "dark"
            ctk.set_appearance_mode(DARK_MODE) #use dark theme
            ctk.set_default_color_theme("blue")

            self.geometry("900x550")
            self.title("ROCK PAPER SCISSORS!")

            main_container = ctk.CTkFrame(self) #make main container
            main_container.pack(fill=tk.BOTH, expand=True)

            self.start_frame = self.init_start_frame(main_container)
            self.video_frame = self.init_video_frame(main_container)

            self.display_frame(self.start_frame)
          #  time.sleep(100)
           # self.stop_event.set()
          #  self.display_frame(start_frame)


g = Game()
g.mainloop()
g.cam.release()
cv2.destroyAllWindows()