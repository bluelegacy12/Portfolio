using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Mirror;
using UnityEngine.SceneManagement;

public class Buttons : NetworkBehaviour
{
    public void NextTurn()
    {
        Player.player.ServerNextTurn();
        Player.player.ClientNextTurn();
    }

    public void ReadyButton()
    {
        transform.gameObject.SetActive(false);
        DeckManager.deckManager.updateText.text = "Waiting for other players";
        if (Player.player.isServer)
        {
            Player.player.ReadyServer();
            DeckManager.deckManager.goalInput.SetActive(false);
        }
        else
        {
            Player.player.ReadyClient();
        }
    }
    
    public void GuessButton()
    {
        transform.gameObject.SetActive(false);
        Player.player.ApplyGuess();
    }

    public void Restart()
    {
        RestartClient();
        SceneManager.LoadScene(0);
    }

    [ClientRpc]
    void RestartClient()
    {
        DeckManager.deckManager.updateText.text = "Waiting for Host";
        DeckManager.deckManager.restartButton.SetActive(false);
    }
}
