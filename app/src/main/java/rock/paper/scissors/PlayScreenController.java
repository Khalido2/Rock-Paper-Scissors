package rock.paper.scissors;

import animatefx.animation.FadeIn;
import animatefx.animation.Flash;
import javafx.fxml.FXML;
import javafx.application.Platform;
import javafx.fxml.Initializable;
import javafx.scene.image.*;
import javafx.scene.text.Text;
import org.bytedeco.javacv.*;
import org.bytedeco.opencv.global.opencv_imgcodecs;
import org.bytedeco.opencv.global.opencv_imgproc;
import org.bytedeco.opencv.opencv_core.IplImage;
import org.bytedeco.opencv.opencv_core.Mat;

import java.net.URL;
import java.nio.ByteBuffer;
import java.util.ResourceBundle;

import jep.*;

//TODO get rid of hardcoded java path
//TODO handle when finger tracking points are out of bounds

public class PlayScreenController implements IShutDownListener, Initializable, IScreenChangeListener {
    static final String snapshotFilePath = "src/main/resources/snapshot.jpg";

    @FXML
    private ImageView videoView;
    @FXML
    private Text playText;

    private Interpreter pyInterpreter; //used to trigger python functions

    boolean cameraActive = true;
    boolean appShutDown = false;

    Mat javaCVMat = new Mat();
    WritablePixelFormat<ByteBuffer> formatByte = PixelFormat.getByteBgraPreInstance();

    OpenCVFrameConverter<Mat> javaCVConv = new OpenCVFrameConverter.ToMat();

    OpenCVFrameGrabber frameGrabber = new OpenCVFrameGrabber(0);
    OpenCVFrameConverter.ToIplImage iplConverter = new OpenCVFrameConverter.ToIplImage();

    ByteBuffer buffer;

    //Update webcam display with annotated webcam footage
    protected void updateView(Frame frame) {
        int w = frame.imageWidth;
        int h = frame.imageHeight;

        IplImage img = iplConverter.convert(frame); //reads in webcam frame
        opencv_imgcodecs.cvSaveImage(snapshotFilePath, img); //convert to image and save
        String imgPath = getAnnotatedImage(snapshotFilePath); //pass image path to media pipe in python script

        IplImage img2 = opencv_imgcodecs.cvLoadImage(imgPath); //load annotated image
        Mat matBGR = javaCVConv.convert(iplConverter.convert(img2));
        opencv_imgproc.cvtColor(matBGR, javaCVMat, opencv_imgproc.COLOR_BGR2BGRA); //convert to required form

        if (buffer == null) {
            buffer = javaCVMat.createBuffer();
        }

        PixelBuffer<ByteBuffer> pb = new PixelBuffer<ByteBuffer>(w, h, buffer, formatByte);
        final WritableImage wi = new WritableImage(pb);
        Platform.runLater(() -> videoView.setImage(wi)); //change image asynchronously

        videoView.setVisible(true); //ensure screen is visible, stop loading screen
    }

    //Calls mediapipe and gets annotated image
    //Returns the path to that image
    public String getAnnotatedImage(String imgPath){
        try{
            pyInterpreter.set("img_path", imgPath);
            Object res = pyInterpreter.getValue("ml.draw_hand_trackers(img_path)");
            return res.toString();
        } catch (JepException e){
            e.printStackTrace();
            return "";
        }
    }

    void setVideoView(Frame mat) {
        updateView(mat);
    }

    //Given a webcam frame, use the ml model to determine the move made
    void detectPlayerMove(Frame frame){
        IplImage img = iplConverter.convert(frame); //reads in webcam frame
        opencv_imgcodecs.cvSaveImage(snapshotFilePath, img); //convert to image and save

        try{
            pyInterpreter.set("img_path", snapshotFilePath);
            Object res = pyInterpreter.getValue("ml.detect_player_move(img_path)");
            System.out.println(res.toString());
        } catch (JepException e){
            e.printStackTrace();
        }
    }

    void setPlayText(String text){
        new FadeIn(playText).setSpeed(2).play();
        playText.setText(text);
    }

    //Does a countdown from 3 before disabling the camera and taking the player's move
    void startCountDown(){
        new Thread(() -> { //create a new thread to do the counting
            try
            {
                playText.setVisible(true);
                playText.setText("HANDS UP!");
                Thread.sleep(1000);
                setPlayText("ROCK");
                Thread.sleep(800);
                setPlayText("PAPER");
                Thread.sleep(800);
                setPlayText("SCISSORS");
                Thread.sleep(800);
                setPlayText("SHOOT!");
                Thread.sleep(500);
                cameraActive = false;
                playText.setVisible(false);
            }
            catch(InterruptedException ex)
            {
                Thread.currentThread().interrupt();
            }
        }).start();
    }

    //Repeatedly grabs frames of webcam and triggers countdown
    void handleCamera(){
        pyInterpreter = new SharedInterpreter(); //set up python interpreter
        try {
            pyInterpreter.exec("from src.main.python.ml_api import ML_API");
            pyInterpreter.exec("ml = ML_API()");
        } catch (JepException e) {
            e.printStackTrace();
        }

        startCountDown(); //trigger countdown

        while (cameraActive) {
            try {
                Frame frame = frameGrabber.grab(); //get new frame
                setVideoView(frame); //display camera frame
            } catch (FrameGrabber.Exception e) {
                e.printStackTrace();
            }
        }

        try {
            if(!appShutDown){
                Frame frame = frameGrabber.grab(); //grab last frame and attempt to classify player move
                detectPlayerMove(frame); //get player move
                frameGrabber.release(); //release camera
            }

            pyInterpreter.close(); //close jep interpreter

        } catch (FrameGrabber.Exception e) {
            e.printStackTrace();
        }
    }

    void triggerCameraGrabber() {
        videoView.setVisible(false); //hide image display loading screen or something
        //TODO add loading screen here

        try {
            frameGrabber.start(); //open camera
        } catch (FrameGrabber.Exception e) {
            e.printStackTrace();
        }
        new Thread(() -> handleCamera()).start(); //create new thread to repeatedly grab frames
    }

    @Override
    public void onShutDown() {
        cameraActive = false;
        appShutDown = true;
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        App.addShutDownListener(this);
        App.addScrnChangeListener(this);
    }

    @Override
    public void onScreenChange(int currentScreen) {

        if(currentScreen == App.VIDEO_SCREEN)
            triggerCameraGrabber(); //start capturing webcam footage if cam screen opened
    }
}