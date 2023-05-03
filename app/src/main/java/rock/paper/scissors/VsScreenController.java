package rock.paper.scissors;

import animatefx.animation.FadeOut;
import animatefx.animation.Shake;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

import java.net.URL;
import java.util.ResourceBundle;

public class VsScreenController implements IMovePlayedListener, Initializable, IScreenChangeListener {

    static final String rockImageURL = "human rock.png";
    static final String paperImageURL = "human paper.png";
    static final String scissorsImageURL = "human scissors.png";
    static final String[] imagesURLs = new String[]{rockImageURL, paperImageURL, scissorsImageURL};

    @FXML
    private ImageView playerMove;

    @FXML
    private ImageView compMove;

    @FXML
    private ImageView flash;


    @Override
    public void onMovePlayed(int moveMade, boolean isPlayer) {
        Image newImg = new Image(getClass().getResourceAsStream(imagesURLs[moveMade]));

        if(isPlayer)
            playerMove.setImage(newImg);
        else
            compMove.setImage(newImg);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        App.addMovePlayedListener(this);
        App.addScrnChangeListener(this);
    }

    @Override
    public void onScreenChange(int currentScreen) {
        if(currentScreen == App.VS_HAND_SCREEN){
            new FadeOut(flash).setSpeed(2).play();
            new Shake(playerMove).play();
            new Shake(compMove).play();
        }
    }
}
