using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Mirror;
using static DeckManager;
using UnityEngine.UI;
using static Player;

public class CardBehavior : NetworkBehaviour
{
    public static CardBehavior cardBehavior;
    public int value;
    public string suit;
    public Sprite image;

    void Start()
    {
        cardBehavior = this;
    }

    public void PlayThisCard()
    {
        if (!Player.player.isServer)
        {
            Player.player.CheckClientPlay(transform.gameObject.GetComponent<CardBehavior>().value, transform.gameObject.GetComponent<CardBehavior>().suit);
        }
        else
        {
            Player.player.PlayServerCard(transform.gameObject);
        }
    }
    
}
