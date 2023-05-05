package rock.paper.scissors;

import animatefx.animation.Pulse;
import javafx.animation.PauseTransition;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.text.Text;
import javafx.util.Duration;

import java.net.URL;
import java.util.ResourceBundle;

public class ResultScreenController implements IGameResultListener, IMovePlayedListener, Initializable {

    int playerMove;

    String tieTxt = "\"If a tie is like kissing your sister, losing is like kissing you grandmother with her teeth out.\" - George Brett";
    String scissorWinTxt = "\"I've never seen sharper scissors\" - Obama 2021";
    String scissorLoseTxt = "\"Sorry kid, you didn't make the cut\" - Coach Carter";

    String paperWinTxt = "\"That paper plane really took flight\" - Newton 1665";
    String paperLoseTxt = "\"You suck at origami!\" - The Lorax"; //or I thought we were on a roll, but we got wiped out

    String rockWinTxt = "\"Tall stands the rock that shatters the blades of time\" - Sun Tzu";
    String rockLoseTxt = "\"I said be a rock, not a pebble!\" - The Rock";

    @FXML
    Text resTxt;

    @FXML
    Text quoteTxt;

    @FXML
    Button resetBtn;

    @FXML
    protected void onResetButtonClick(){
        resetBtn.setStyle(Constants.LIGHT_BTN_CLICKED_COLOUR); //change to click colour
        new Pulse(resetBtn).play(); //play animation
        PauseTransition pause = new PauseTransition(Duration.seconds(0.5));
        pause.setOnFinished(event -> {
            resetBtn.setStyle(Constants.LIGHT_BTN_DEFAULT_COLOUR);
            App.setScreen(App.VIDEO_SCREEN);
        });
        pause.play();
    }

    String getQuoteRock(boolean playerWon){
        return (playerWon ? rockWinTxt : rockLoseTxt);
    }

    String getQuotePaper(boolean playerWon){
        return (playerWon ? paperWinTxt : paperLoseTxt);
    }

    String getQuoteScissors(boolean playerWon){
        return (playerWon ? scissorWinTxt : scissorLoseTxt);
    }

    @Override
    public void onGameResult(int result) { //on game result calculated, set game quote and text

        if(result == 2){
            resTxt.setText("IT'S A TIE!");
            quoteTxt.setText(tieTxt);
        }else{

            if(result == 0)
                resTxt.setText("YOU WON!");
            else
                resTxt.setText("YOU LOST!");

            String quote;

            if(playerMove == 0)
                quote = getQuoteRock(result == 0);
            else if (playerMove == 1)
                quote = getQuotePaper(result == 0);
            else
                quote = getQuoteScissors(result == 0);

            quoteTxt.setText(quote);
        }
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        App.addMovePlayedListener(this);
        App.addGameResultListener(this);
    }

    @Override
    public void onMovePlayed(int movePlayed, boolean isPlayer) {
        if(isPlayer)
            playerMove = movePlayed;
    }
}
