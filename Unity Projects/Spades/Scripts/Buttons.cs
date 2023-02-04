using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Mirror;

public class Buttons : NetworkBehaviour
{
    public void NextTurn()
    {
        Player.player.ServerNextTurn();
        Player.player.ClientNextTurn();
    }

    public void ReadyButton()
    {
        DeckManager.deckManager.updateText.text = "Waiting for other players";
        if (Player.player.isServer)
        {
            Player.player.ReadyServer();
        }
        else
        {
            Player.player.ReadyClient();
        }
        transform.gameObject.SetActive(false);
    }
    
    public void GuessButton()
    {
        transform.gameObject.SetActive(false);
        Player.player.ApplyGuess();
    }
}
