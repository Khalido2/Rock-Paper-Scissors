package rock.paper.scissors;

import animatefx.animation.FadeOut;
import animatefx.animation.Shake;
import javafx.animation.PauseTransition;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.util.Duration;

import java.net.URL;
import java.util.ResourceBundle;

public class VsScreenController implements IMovePlayedListener, Initializable, IScreenChangeListener {

    static final String rockImageURL = "human rock.png";
    static final String paperImageURL = "human paper.png";
    static final String scissorsImageURL = "human scissors.png";
    static final String[] imagesURLs = new String[]{rockImageURL, paperImageURL, scissorsImageURL};

    int playerMove;
    int compMove;

    @FXML
    private ImageView playerMoveImg;

    @FXML
    private ImageView compMoveImg;

    @FXML
    private ImageView flash;


    @Override
    public void onMovePlayed(int moveMade, boolean isPlayer) {
        Image newImg = new Image(getClass().getResourceAsStream(imagesURLs[moveMade]));

        if(isPlayer)
        {
            playerMoveImg.setImage(newImg);
            playerMove = moveMade;
        }else
        {
            compMoveImg.setImage(newImg);
            compMove = moveMade;
        }
    }

    //Wait for a couple seconds then move to next screen
    void waitNShiftToNextPage(){
        int result;

        PauseTransition pause = new PauseTransition(Duration.seconds(2));
        pause.setOnFinished(event -> {
            App.setScreen(App.RESULT_SCREEN);
        });
        pause.play();

        result = GameLogic.calcMatchResult(playerMove, compMove); //calculate result of match
        App.setGameResult(result);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        App.addMovePlayedListener(this);
        App.addScrnChangeListener(this);
    }

    @Override
    public void onScreenChange(int currentScreen) {
        if(currentScreen == App.VS_HAND_SCREEN){ //when game reaches this screen
            new FadeOut(flash).setSpeed(2).play();
            new Shake(playerMoveImg).play();
            new Shake(compMoveImg).play();
            waitNShiftToNextPage();
        }
    }
}
