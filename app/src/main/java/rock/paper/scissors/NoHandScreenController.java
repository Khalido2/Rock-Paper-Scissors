package rock.paper.scissors;

import javafx.fxml.FXML;

public class NoHandScreenController {

    @FXML
    protected void onResetButtonClick(){
        App.setScreen(App.VIDEO_SCREEN);
    }

}
