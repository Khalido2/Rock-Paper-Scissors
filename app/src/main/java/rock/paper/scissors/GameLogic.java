package rock.paper.scissors;

public class GameLogic {

    public static int GetComputerMove(){
        return (int) ((Math.random() * (3 - 1)) + 1); //get rand num between 1-3
    }
}
