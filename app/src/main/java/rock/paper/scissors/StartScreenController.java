package rock.paper.scissors;

import animatefx.animation.*;
import javafx.animation.PauseTransition;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.util.Duration;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
public class StartScreenController {

    String clickedColour = "-fx-background-color:#5FE1D9";
    String regularColour = "-fx-background-color:#F7FAD1";

    @FXML
    Button startBtn;


    @FXML
    protected void onStartButtonClick(){
        startBtn.setStyle(clickedColour); //change to click colour
        new Pulse(startBtn).play(); //play animation
        PauseTransition pause = new PauseTransition(Duration.seconds(0.5));
        pause.setOnFinished(event -> {
            startBtn.setStyle(regularColour);
            App.setScreen(1); //move to play screen
        });
        pause.play();
    }

}