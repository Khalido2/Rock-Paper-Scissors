package rock.paper.scissors;

public interface IMovePlayedListener {
    void onMovePlayed(int movePlayed, boolean isPlayer); //called whenever computer of player makes a move
}
