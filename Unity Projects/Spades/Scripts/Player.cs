using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Mirror;
using UnityEngine.UI;
using static DeckManager;

public class Player : NetworkBehaviour
{
    public static Player player;
    public GameObject discard1;
    public GameObject discard2;
    public GameObject discard3;
    public GameObject discard4;
    public GameObject[] discards;
    public GameObject playerHand;
    public List<Card> discardList = new List<Card>();
    public int discardValue;
    public string discardSuit;
    public string leadingSuit;
    public int winningCard;
    public GameObject nm;
    [SyncVar]
    public bool p3Play = false;
    [SyncVar]
    public bool spawnClientHand = false;
    public int guessNumber;
    public GameObject guessButton;
    public GameObject slider;

    void Start()
    {
        player = this;
        playerHand = GameObject.Find("Player Hand");
        discard1 = GameObject.Find("Discard1");
        discard2 = GameObject.Find("Discard2");
        discard3 = GameObject.Find("Discard3");
        discard4 = GameObject.Find("Discard4");
        guessButton = GameObject.Find("Submit Guess"); 
        slider = GameObject.Find("Guess Counter");
    }

    void Update()
    {
        if (!isServer && spawnClientHand)
        {
            SpawnHand();
        }
        if (leadingSuit != null && DeckManager.deckManager.leadingSuit != null)
        {
            if (leadingSuit != DeckManager.deckManager.leadingSuit || winningCard != DeckManager.deckManager.winningCard)
            {
                leadingSuit = DeckManager.deckManager.leadingSuit;
                winningCard = DeckManager.deckManager.winningCard;
                if (DeckManager.deckManager.turnCount == 1)
                {
                    foreach (Sprite s in DeckManager.deckManager.cardFace)
                    {
                        if (s.name == winningCard.ToString() + leadingSuit)
                        {
                            DeckManager.deckManager.suitDisplay.GetComponent<Image>().sprite = s;
                            break;
                        }
                    }
                    DeckManager.deckManager.suitDisplay.SetActive(true);
                }
            }
        }
    }
    
    public void DealHandP1()
    {
        if (isServer)
        {
            foreach (Card c in DeckManager.deckManager.player1Hand)
            {
                DeckManager.deckManager.CreateCard(c);
                DeckManager.deckManager.newCard.transform.SetParent(playerHand.transform);
                DeckManager.deckManager.newCard.transform.localScale = new Vector3(1, 1, 1);
            }
        }
    }

    [ClientRpc]
    public void DealHandP3()
    {
        // the server updated the card list for p3 - now turn those loose card prefabs into p3's hand and move them to the hand display
        if (!isServer)
        {
            GameObject[] looseCardObjects = GameObject.FindGameObjectsWithTag("Card");
            List<Card> player3Hand = DeckManager.deckManager.player3Hand;
            for (int i = 0; i < player3Hand.Count; i++)
            {
                CardBehavior card = looseCardObjects[i].GetComponent<CardBehavior>();
                card.transform.SetParent(playerHand.transform);
                card.transform.localScale = new Vector3(1, 1, 1);
                card.value = player3Hand[i].value;
                card.suit = player3Hand[i].suit;
                card.image = player3Hand[i].image;
                card.GetComponent<Image>().sprite = card.image;
            }
        }
    }

    [ClientRpc]
    public void UpdateDiscards(int value, string suit, int index)
    {
        discards = GameObject.FindGameObjectsWithTag("Discard");
        GameObject emptyCard = new GameObject();
        foreach (GameObject c in discards)
        {
            if (c.GetComponent<CardBehavior>().value == 0)
            {
                emptyCard = c;
            }
        }
        emptyCard.GetComponent<CardBehavior>().value = value;
        emptyCard.GetComponent<CardBehavior>().suit = suit;
        foreach (Sprite s in DeckManager.deckManager.cardFace)
        {
            if (s.name == value + suit)
            {
                emptyCard.GetComponent<Image>().sprite = s;
            }
        }

        switch (index)
        {
            case 0:
                if (isServer)
                {
                    foreach (Transform child in discard1.transform)
                    {
                        GameObject.Destroy(child.gameObject);
                    }
                    emptyCard.transform.SetParent(discard1.transform);
                }
                else
                {
                    foreach (Transform child in discard3.transform)
                    {
                        GameObject.Destroy(child.gameObject);
                    }
                    emptyCard.transform.SetParent(discard3.transform);
                }
                break;
            case 1:
                foreach (Transform child in discard2.transform)
                {
                    GameObject.Destroy(child.gameObject);
                }
                emptyCard.transform.SetParent(discard2.transform);
                break;
            case 2:
                if (isServer)
                {
                    foreach (Transform child in discard3.transform)
                    {
                        GameObject.Destroy(child.gameObject);
                    }
                    emptyCard.transform.SetParent(discard3.transform);
                }
                else
                {
                    foreach (Transform child in discard1.transform)
                    {
                        GameObject.Destroy(child.gameObject);
                    }
                    emptyCard.transform.SetParent(discard1.transform);
                }
                break;
            case 3:
                foreach (Transform child in discard4.transform)
                {
                    GameObject.Destroy(child.gameObject);
                }
                emptyCard.transform.SetParent(discard4.transform);
                break;
        }
        emptyCard.transform.localScale = new Vector3(1, 1, 1);
    }

    [Command]
    public void SpawnHand()
    {
        foreach (Transform card in playerHand.transform)
        {
            NetworkServer.Spawn(card.gameObject);
        }
        spawnClientHand = false;
    }

    public Card MakeNewCard(int value, string suit)
    {
        Card tempCard = new Card();
        tempCard.value = value;
        tempCard.suit = suit;
        tempCard.imageName = value.ToString() + suit;
        foreach (Sprite s in DeckManager.deckManager.cardFace)
        {
            if (s.name == tempCard.imageName)
            {
                tempCard.image = s;
                break;
            }
        }
        return tempCard;
    }

    public void CheckClientPlay(int value, string suit)
    {
        if (DeckManager.deckManager.turnIndex == 2)
        {
            if (DeckManager.deckManager.turnCount < 4)
            {
                // check hand for valid play first, else return
                int numberOfLeadingSuit = 0;
                if (DeckManager.deckManager.turnCount > 0)
                {    
                    foreach (Transform c in playerHand.transform)
                    {
                        if (c.GetComponent<CardBehavior>().suit == DeckManager.deckManager.leadingSuit)
                        {
                            numberOfLeadingSuit += 1;
                        }
                    }
                }
                if (suit != leadingSuit && numberOfLeadingSuit > 0)
                {
                    DeckManager.deckManager.textHold = true;
                    DeckManager.deckManager.updateText.text = "Invalid play! You must play the leading suit if you have it.";
                    return;
                }
                if (suit == "spades" && !DeckManager.deckManager.spades && DeckManager.deckManager.turnCount == 0)
                {
                    int numOfSpades = 0;
                    foreach (Transform c in playerHand.transform)
                    {
                        if (c.GetComponent<CardBehavior>().suit == "spades")
                        {
                            numOfSpades += 1;
                        }
                    }
                    if (numOfSpades != playerHand.transform.childCount)
                    {
                        DeckManager.deckManager.textHold = true;
                        DeckManager.deckManager.updateText.text = "Invalid play! Spades have not been broken yet.";
                        return;
                    }
                }
                if (DeckManager.deckManager.firstTurn)
                {
                    if (suit != "clubs" || value != 2)
                    {
                        DeckManager.deckManager.textHold = true;
                        DeckManager.deckManager.updateText.text = "On the first turn you must play the 2 of Clubs!";
                        return;
                    }
                }
                if (DeckManager.deckManager.waitForNext)
                {
                    return;
                }
                DeckManager.deckManager.textHold = false;
                PlayClientCard(value, suit);
                foreach (Transform child in playerHand.transform)
                {
                    if (child.GetComponent<CardBehavior>().value == value && child.GetComponent<CardBehavior>().suit == suit)
                    {
                        GameObject.Destroy(child.gameObject);
                        break;
                    }
                }
                ReportNewP3Hand(value, suit);
            }
        }
    }
    //give the server p3's choice and tell server what to play
    [Command]
    public void PlayClientCard(int value, string suit)
    {
        Card tempCard = MakeNewCard(value, suit);
        DeckManager.deckManager.newCard = Instantiate(DeckManager.deckManager.cardPrefab);
        DeckManager.deckManager.newCard.GetComponent<Image>().sprite = tempCard.image;
        CardBehavior cardData = DeckManager.deckManager.newCard.GetComponent<CardBehavior>();
        cardData.value = tempCard.value;
        cardData.suit = tempCard.suit;
        p3Play = true;
        PlayServerCard(DeckManager.deckManager.newCard);
        DeckManager.deckManager.player3Hand.Remove(tempCard);
    }

    public void PlayServerCard(GameObject card)
    {
        if ((DeckManager.deckManager.turnIndex == 0 && player.isServer) || (DeckManager.deckManager.turnIndex == 2 && p3Play))
        {
            
            if (DeckManager.deckManager.turnCount < 4)
            {
                // check hand for valid play first, else return
                int numberOfLeadingSuit = 0;
                if (!p3Play)
                {
                    if (DeckManager.deckManager.turnCount > 0)
                    {    
                        foreach (Transform c in playerHand.transform)
                        {
                            if (c.GetComponent<CardBehavior>().suit == DeckManager.deckManager.leadingSuit)
                            {
                                numberOfLeadingSuit += 1;
                            }
                        }
                    }
                    if (card.GetComponent<CardBehavior>().suit != leadingSuit && numberOfLeadingSuit > 0)
                    {
                        DeckManager.deckManager.textHold = true;
                        DeckManager.deckManager.updateText.text = "Invalid play! You must play the leading suit if you have it.";
                        return;
                    }
                    if (card.GetComponent<CardBehavior>().suit == "spades" && !DeckManager.deckManager.spades && DeckManager.deckManager.turnCount == 0)
                    {
                        int numOfSpades = 0;
                        foreach (Transform c in playerHand.transform)
                        {
                            if (c.GetComponent<CardBehavior>().suit == "spades")
                            {
                                numOfSpades += 1;
                            }
                        }
                        if (numOfSpades != playerHand.transform.childCount)
                        {
                            DeckManager.deckManager.textHold = true;
                            DeckManager.deckManager.updateText.text = "Invalid play! Spades have not been broken yet.";
                            return;
                        }
                    }
                }
                if (DeckManager.deckManager.firstTurn)
                {
                    if (card.GetComponent<CardBehavior>().suit != "clubs" || card.GetComponent<CardBehavior>().value != 2)
                    {
                        DeckManager.deckManager.textHold = true;
                        DeckManager.deckManager.updateText.text = "On the first turn you must play the 2 of Clubs!";
                        return;
                    }
                }
                if (DeckManager.deckManager.waitForNext)
                {
                    return;
                }
                DeckManager.deckManager.textHold = false;
                p3Play = false;
                if (DeckManager.deckManager.firstTurn)
                {
                    DeckManager.deckManager.firstTurn = false;
                    DeckManager.deckManager.amountOfGuessers = 0;
                }
                if (DeckManager.deckManager.turnIndex == 0)
                {
                    card.transform.SetParent(discard1.transform);
                }
                else
                {
                    card.transform.SetParent(discard3.transform);
                }
                card.transform.localScale = new Vector3(1, 1, 1);
                Card newCard = new Card();
                newCard.value = card.GetComponent<CardBehavior>().value;
                newCard.suit = card.GetComponent<CardBehavior>().suit;
                newCard.image = card.GetComponent<Image>().sprite;
                DeckManager.deckManager.discardList.Add(newCard);
                if (isServer)
                {
                    DeckManager.deckManager.player1Hand.Remove(newCard);
                }
                else
                {
                    DeckManager.deckManager.player3Hand.Remove(newCard);
                }
                DeckManager.deckManager.discardListValue = newCard.value;
                DeckManager.deckManager.discardListSuit = newCard.suit;
                if (DeckManager.deckManager.turnCount == 0)
                {
                    DeckManager.deckManager.leadingSuit = card.GetComponent<CardBehavior>().suit;
                    DeckManager.deckManager.winningCard = card.GetComponent<CardBehavior>().value;
                    DeckManager.deckManager.winningPlayer = DeckManager.deckManager.turnIndex;
                    DeckManager.deckManager.suitDisplay.GetComponent<Image>().sprite = card.GetComponent<Image>().sprite;
                    DeckManager.deckManager.suitDisplay.gameObject.SetActive(true);
                    if (DeckManager.deckManager.leadingSuit == "spades")
                    {
                        DeckManager.deckManager.spadesPlayed = true;
                    }
                }
                else
                {
                    if (newCard.suit == DeckManager.deckManager.leadingSuit || newCard.suit == "spades")
                    {
                        if (newCard.value > DeckManager.deckManager.winningCard && !DeckManager.deckManager.spadesPlayed)
                        {
                            DeckManager.deckManager.winningCard = newCard.value;
                            DeckManager.deckManager.winningPlayer = DeckManager.deckManager.turnIndex;
                        }
                        if (DeckManager.deckManager.spadesPlayed && newCard.suit == "spades" && newCard.value > DeckManager.deckManager.winningCard)
                        {
                            DeckManager.deckManager.winningCard = newCard.value;
                            DeckManager.deckManager.winningPlayer = DeckManager.deckManager.turnIndex;
                        }
                        if (!DeckManager.deckManager.spadesPlayed && newCard.suit == "spades")
                        {
                            DeckManager.deckManager.winningCard = newCard.value;
                            DeckManager.deckManager.winningPlayer = DeckManager.deckManager.turnIndex;
                            DeckManager.deckManager.spadesPlayed = true;
                        }
                    }
                }
                if (card.GetComponent<CardBehavior>().suit == "spades")
                {
                    DeckManager.deckManager.spades = true;
                }
                GameObject emptyCard = Instantiate(DeckManager.deckManager.discardPrefab);
                NetworkServer.Spawn(emptyCard);
                UpdateDiscards(newCard.value, newCard.suit, DeckManager.deckManager.turnIndex);
                DeckManager.deckManager.turnIndex += 1;
                DeckManager.deckManager.turnCount += 1;
            }
        }
    }

    [Command]
    public void ReportNewP3Hand(int value, string suit)
    {
        Card card = MakeNewCard(value, suit);
        DeckManager.deckManager.player3Hand.Remove(card);
    }

    [Command]
    public void ReadyClient()
    {
        DeckManager.deckManager.readyPlayers += 1;
    }

    public void ReadyServer()
    {
        DeckManager.deckManager.readyPlayers += 1;
    }

    public void ServerNextTurn()
    {
        DeckManager.deckManager.turnCount = 0;
        DeckManager.deckManager.discardList.Clear();
        DeckManager.deckManager.waitForNext = false;
        DeckManager.deckManager.spadesPlayed = false;
        foreach (GameObject d in discards)
        {
            foreach (Transform child in d.transform)
            {
                GameObject.Destroy(child.gameObject);
            }
        }
        discard1.transform.GetChild(0).SetParent(null);
        discard2.transform.GetChild(0).SetParent(null);
        discard3.transform.GetChild(0).SetParent(null);
        discard4.transform.GetChild(0).SetParent(null);
        DeckManager.deckManager.turnIndex = DeckManager.deckManager.winningPlayer;
        DeckManager.deckManager.winningCard = 0;
        GameObject.Find("Next Turn Button").SetActive(false);
        DeckManager.deckManager.suitDisplay.gameObject.SetActive(false);
    }

    [ClientRpc]
    public void ClientNextTurn()
    {
        DeckManager.deckManager.turnCount = 0;
        DeckManager.deckManager.discardList.Clear();
        DeckManager.deckManager.waitForNext = false;
        DeckManager.deckManager.suitDisplay.gameObject.SetActive(false);
    }

    public void ApplyGuess()
    {
        int.TryParse(DeckManager.deckManager.guessText.GetComponent<TMPro.TextMeshProUGUI>().text, out guessNumber);
        DeckManager.deckManager.guessButton.SetActive(false);
        DeckManager.deckManager.guessCounter.SetActive(false);
        DeckManager.deckManager.guessText.SetActive(false);
        if (!isServer)
        {
            if (guessNumber == 0)
            {
                DeckManager.deckManager.nil3.gameObject.SetActive(true);
            }
            TotalGuessesClient(guessNumber);
            DeckManager.deckManager.waitForNext = false;
        }
        else
        {
            TotalGuessesServer();
        }
    }
    
    [Command]
    public void TotalGuessesClient(int guess)
    {
        if (guess == 0)
        {
            DeckManager.deckManager.nil3.gameObject.SetActive(true);
        }
        DeckManager.deckManager.p3Guess = guess;
        DeckManager.deckManager.amountOfGuessers += 1;
    }

    public void TotalGuessesServer()
    {
        if (guessNumber == 0)
        {
            DeckManager.deckManager.nil1.gameObject.SetActive(true);
            ClientNil1();
        }
        DeckManager.deckManager.amountOfGuessers += 1;
    }

    [ClientRpc]
    public void ClientNil1()
    {
        DeckManager.deckManager.nil1.gameObject.SetActive(true);
    }
}
