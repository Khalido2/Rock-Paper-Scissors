package rock.paper.scissors;

public interface IGameResultListener {

    public void onGameResult(int result); //called when the result of the game is determined
}
