package rock.paper.scissors;

public class GameLogic {

    public static int GetComputerMove(){return (int) ((Math.random() * (3 - 1)) + 1); }//get rand num between 1-3

    //Determines who won or if it was a tie
    //0 is Rock, 1 is Paper and 2 is Scissors
    public static int calcMatchResult(int playerMove, int compMove){
        if(playerMove == compMove)
            return 2; // a tie

        if ((playerMove == 0 && compMove == 2) || (playerMove == 1 && compMove == 0) || (playerMove == 2 && compMove == 1))
            return 0; //player win
        else
            return 1; //comp win
    }

}
