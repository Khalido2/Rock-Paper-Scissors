package rock.paper.scissors;

import animatefx.animation.Pulse;
import javafx.animation.PauseTransition;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.util.Duration;

public class NoHandScreenController {

    @FXML
    Button resetBtn;

    @FXML
    protected void onResetButtonClick(){
        resetBtn.setStyle(Constants.DARK_BTN_CLICKED_COLOUR); //change to click colour
        new Pulse(resetBtn).play(); //play animation
        PauseTransition pause = new PauseTransition(Duration.seconds(0.5));
        pause.setOnFinished(event -> {
            resetBtn.setStyle(Constants.DARK_BTN_DEFAULT_COLOUR);
            App.setScreen(App.VIDEO_SCREEN);
        });
        pause.play();
    }

}
