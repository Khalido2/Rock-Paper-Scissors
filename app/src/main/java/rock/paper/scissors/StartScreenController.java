package rock.paper.scissors;

import animatefx.animation.*;
import javafx.animation.PauseTransition;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.util.Duration;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
public class StartScreenController {

    @FXML
    Button startBtn;


    @FXML
    protected void onStartButtonClick(){
        startBtn.setStyle(Constants.LIGHT_BTN_CLICKED_COLOUR); //change to click colour
        new Pulse(startBtn).play(); //play animation
        PauseTransition pause = new PauseTransition(Duration.seconds(0.5));
        pause.setOnFinished(event -> {
            startBtn.setStyle(Constants.LIGHT_BTN_DEFAULT_COLOUR);
            App.setScreen(App.VIDEO_SCREEN); //move to play screen
        });
        pause.play();
    }

}
