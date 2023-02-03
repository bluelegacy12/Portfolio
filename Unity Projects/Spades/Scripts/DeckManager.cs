using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Mirror;
using UnityEngine.UI;
using static Player;

public class DeckManager : NetworkBehaviour
{
    public static DeckManager deckManager;
    public GameObject cardPrefab;
    public GameObject discardPrefab;
    public TMPro.TextMeshProUGUI updateText;
    [SyncVar]
    public int readyPlayers = 0;
    [SyncVar]
    public bool activate = false;
    [SyncVar]
    public float playDelay = 0;
    [SyncVar]
    public int turnIndex = 0;
    [SyncVar]
    public int turnCount = 0;
    public List<Card> deck = new List<Card>();
    public string[] suitArr = {"hearts", "clubs", "diamonds", "spades"};
    public Sprite[] cardFace;
    public GameObject newCard;
    public GameObject nextTurnButton;
    public GameObject startButton;
    [SyncVar]
    public string leadingSuit;
    [SyncVar]
    public int winningCard = 0;
    [SyncVar]
    public int winningPlayer;
    public GameObject suitDisplay;
    [SyncVar]
    public int p1Points = 0;
    [SyncVar]
    public int p2Points = 0;
    [SyncVar]
    public int p3Points = 0;
    [SyncVar]
    public int p4Points = 0;
    [SyncVar]
    public int team13Points = 0;
    [SyncVar]
    public int team24Points = 0;
    [SyncVar]
    public int team13Bags = 0;
    [SyncVar]
    public int team24Bags = 0;
    public TMPro.TextMeshProUGUI team13Guess;
    public TMPro.TextMeshProUGUI team24Guess;
    public TMPro.TextMeshProUGUI team13PointsText;
    public TMPro.TextMeshProUGUI team24PointsText;
    public TMPro.TextMeshProUGUI team13BagsText;
    public TMPro.TextMeshProUGUI team24BagsText;
    public List<Card> discardList = new List<Card>();
    [SyncVar]
    public int discardListValue;
    [SyncVar]
    public string discardListSuit;
    public List<Card> player1Hand = new List<Card>();
    public List<Card> player2Hand = new List<Card>();
    public List<Card> player3Hand = new List<Card>();
    public List<Card> player4Hand = new List<Card>();
    public readonly SyncList<int> player3values = new SyncList<int>();
    public readonly SyncList<string> player3suits = new SyncList<string>();
    public readonly SyncList<string> player3imageName = new SyncList<string>();
    public GameObject nm;
    public GameObject discard1;
    public GameObject discard2;
    public GameObject discard3;
    public GameObject discard4;
    public GameObject guessCounter;
    public GameObject guessButton;
    public GameObject guessText;
    public GameObject readyButton;
    public bool textHold = false;
    [SyncVar]
    public bool spadesPlayed = false;
    [SyncVar]
    public bool spades = false; //true or false if spades has been broken
    [SyncVar]
    public bool waitForNext = true;
    [SyncVar]
    public bool firstTurn = true;
    [SyncVar]
    public int playerReconnect;
    [SyncVar]
    public int amountOfGuessers = 0;
    [SyncVar]
    public int p3Guess;
    [SyncVar]
    public int p1p3Total;
    [SyncVar]
    public int p2p4Total;

    // Start is called before the first frame update
    void Start()
    {
        deckManager = this;
        waitForNext = true;
        nextTurnButton.SetActive(false);
        suitDisplay.SetActive(false);
        startButton.SetActive(true);
        guessCounter.SetActive(false);
        guessButton.SetActive(false);
        updateText = GameObject.Find("UpdateText").GetComponent<TMPro.TextMeshProUGUI>();
        discard1 = GameObject.Find("Discard1");
        discard2 = GameObject.Find("Discard2");
        discard3 = GameObject.Find("Discard3");
        discard4 = GameObject.Find("Discard4");
        guessText = GameObject.Find("Guess Number");
        nm = GameObject.Find("Network Manager");
        foreach (string s in suitArr)
        {
            for (int i = 2; i <= 14; i++)
            {
                Card tempCard = new Card();
                tempCard.value = i;
                tempCard.suit = s;
                foreach (Sprite sp in cardFace)
                {
                    if (sp.name == i + s)
                    {
                        tempCard.image = sp;
                        tempCard.imageName = i.ToString() + s;
                    }
                }
                deck.Add(tempCard);
            }
        }
    }

    void Update()
    {
        if (amountOfGuessers == 2 && isServer)
        {
            p1p3Total = Player.player.guessNumber + p3Guess;
            waitForNext = false;
        }
        if (firstTurn && !waitForNext)
        {
            team13Guess.text = "Team 1&3 Guess: " + (p1p3Total).ToString();
            team24Guess.text = "Team 2&4 Guess: " + p2p4Total.ToString();
            amountOfGuessers = 0;
        }
        if (readyPlayers == 2 && isServer)
        {
            team13Guess.text = "Team 1&3 Guess: 0";
            team24Guess.text = "Team 2&4 Guess: 0";
            readyPlayers = 3;
            playerReconnect = readyPlayers;
            ShuffleAndDeal();
            ServerUpdateP3Hand();
            ClientUpdateP3Hand();
            SpawnP3Hand();
            Player.player.DealHandP3();
            startButton.SetActive(false);

            // player with 2 of clubs goes first
            foreach (Card c in player1Hand)
            {
                if (c.value == 2 && c.suit == "clubs")
                {
                    turnIndex = 0;
                    break;
                }
            }
            foreach (Card c in player2Hand)
            {
                if (c.value == 2 && c.suit == "clubs")
                {
                    turnIndex = 1;
                    break;
                }
            }
            foreach (Card c in player3Hand)
            {
                if (c.value == 2 && c.suit == "clubs")
                {
                    turnIndex = 2;
                    break;
                }
            }
            foreach (Card c in player4Hand)
            {
                if (c.value == 2 && c.suit == "clubs")
                {
                    turnIndex = 3;
                    break;
                }
            }
            
            // ai guessing logic
            int p2guess = 0;
            int p2spadeCount = 0;
            foreach (Card c in player2Hand)
            {
                if (c.value > 12 || (c.suit == "spades" && c.value > 8))
                {
                    p2guess += 1;
                    if (c.suit =="spades")
                    {
                        p2spadeCount += 1;
                    }
                }
            }
            if (p2spadeCount > 3)
            {
                p2guess -= 1;
            }
            int p4guess = 0;
            int p4spadeCount = 0;
            foreach (Card c in player4Hand)
            {
                if (c.value > 12 || (c.suit == "spades" && c.value > 8))
                {
                    p4guess += 1;
                    if (c.suit =="spades")
                    {
                        p4spadeCount += 1;
                    }
                }
            }
            if (p4spadeCount > 3)
            {
                p4guess -= 1;
            }
            p2p4Total = p2guess + p4guess;
        }
     /*    if (readyPlayers > playerReconnect)
        {
            playerReconnect = readyPlayers;
            player3values.Clear();
            player3suits.Clear();
            player3imageName.Clear();
            Player.player.discards = GameObject.FindGameObjectsWithTag("Card");
            foreach (GameObject c in Player.player.discards)
            {
                if (c.transform.parent = null)
                {
                    Destroy(c);
                }
            }
            ServerUpdateP3Hand();
            ClientUpdateP3Hand();
            SpawnP3Hand();
            Player.player.DealHandP3();
            Player.player.DealHandP1();
        } */
        if (turnIndex > 3 && turnCount < 4 && !waitForNext)
        {
            turnIndex = 0;
        }
        if ((isServer && turnIndex == 0) || (!isServer && turnIndex == 2))
        {
            if (waitForNext || textHold){return;}
            updateText.text = "Your turn!";
        }
        if ((isServer && turnIndex == 2) || (!isServer && turnIndex == 0))
        {
            if (waitForNext || textHold){return;}
            updateText.text = "It's your partner's turn";
        }
        if (turnIndex == 1 || turnIndex == 3)
        {
            if (waitForNext || textHold){return;}
            updateText.text = "Player " + (turnIndex + 1) + "'s turn";
        }
        if (turnCount == 4)
        {
            Debug.Log(player2Hand.Count + "in p2 hand");
            Debug.Log(player1Hand.Count + "in p1 hand");
            turnCount = 5;
            waitForNext = true;
            UpdateServerPoints(winningPlayer);

            // calc points at end of each round
            if (player2Hand.Count == 0)
            {
                if (isServer)
                {
                    if (p1Points + p3Points >= p1p3Total)
                    {
                        team13Points += p1p3Total * 10;
                        if (p1Points + p3Points > p1p3Total)
                        {
                            team13Bags += (p1Points + p3Points) - p1p3Total;
                        }
                        team13PointsText.text = "Team 1&3 Points: " + team13Points.ToString();
                        team13BagsText.text = "Team 1&3 Bags: " + team13Bags.ToString();
                        updateText.text = "Your total points are now: " + team13Points.ToString() + ", and your bags are: " + team13Bags.ToString() + ".";
                        if (team13Bags >= 10)
                        {
                            team13Bags -= 10;
                            team13Points -= 100;
                        }
                    }
                    else
                    {
                        updateText.text = "Your team busted! No points were earned this round.";
                    }
                    if (p2Points + p4Points >= p2p4Total)
                    {
                        team24Points += p2p4Total * 10;
                        if (p2Points + p4Points > p2p4Total)
                        {
                            team24Bags += (p2Points + p4Points) - p2p4Total;
                        }
                        team24PointsText.text = "Team 2&4 Points: " + team24Points.ToString();
                        team24BagsText.text = "Team 2&4 Bags: " + team24Bags.ToString();
                        if (team24Bags >= 10)
                        {
                            team24Bags -= 10;
                            team24Points -= 100;
                        }
                    }
                }
                readyPlayers = 0;
                amountOfGuessers = 0;
                readyButton.SetActive(true);
            }
            else if (isServer)
            {
                nextTurnButton.SetActive(true);
            }
        }
        if (turnCount == 5)
        {
            UpdateClientPoints(winningPlayer);
        }
        if (!Player.player.isServer)
        {
            return;
        }
        if (turnIndex != 0 && turnCount < 4 && turnIndex != 2 && !waitForNext)
        {
            playDelay += Time.deltaTime;
            List<Card> currentPlayer = new List<Card>();
            Card currentCard = new Card();
            bool cardFound = false;
            if (playDelay >= 1.5f)
            {
                switch (turnIndex)
                {
                    case 0:
                        foreach (Card c in player1Hand)
                        {
                            currentPlayer.Add(c);
                        }
                        break;
                    case 1:
                        foreach (Card c in player2Hand)
                        {
                            currentPlayer.Add(c);
                        }
                        break;
                    case 2:
                        foreach (Card c in player3Hand)
                        {
                            currentPlayer.Add(c);
                        }
                        break;
                    case 3:
                        foreach (Card c in player4Hand)
                        {
                            currentPlayer.Add(c);
                        }
                        break;
                }                
                foreach (Card c in currentPlayer)
                {
                    if (turnCount != 0 && currentCard.value < c.value && leadingSuit == c.suit)
                    {
                        currentCard = c;
                        cardFound = true;
                    }
                    if (turnCount == 0)
                    {
                        if (currentCard.value < c.value)
                        {
                            if (c.suit == "spades" && spades || c.suit != "spades")
                            {
                                currentCard = c;
                                cardFound = true;
                            }
                        }
                    }
                }
                if (!cardFound)
                {
                    foreach (Card c in currentPlayer)
                    {
                        if (c.suit == "spades")
                        {
                            currentCard = c;
                            cardFound = true;
                            break;
                        }
                    }
                }
                if (!cardFound)
                {
                    currentCard.value = 14;
                    foreach (Card c in currentPlayer)
                    {
                        if (currentCard.value > c.value)
                        {
                            currentCard = c;
                        }
                    }
                }
                if (firstTurn)
                {
                    foreach (Card c in currentPlayer)
                    {
                        if (c.value == 2 && c.suit == "clubs")
                        {
                            currentCard = c;
                            break;
                        }
                    }
                    firstTurn = false;
                    amountOfGuessers = 0;
                }
                int x = currentPlayer.IndexOf(currentCard);
                CreateCard(currentPlayer[x]);
                if (currentCard.suit == "spades")
                {
                    spades = true;
                }
                if (turnCount == 0)
                {
                    leadingSuit = newCard.GetComponent<CardBehavior>().suit;
                    winningCard = newCard.GetComponent<CardBehavior>().value;
                    winningPlayer = turnIndex;
                    suitDisplay.GetComponent<Image>().sprite = newCard.GetComponent<Image>().sprite;
                    suitDisplay.SetActive(true);
                    if (leadingSuit == "spades")
                    {
                        spadesPlayed = true;
                    }
                }
                else
                {
                    if (currentCard.suit == leadingSuit || currentCard.suit == "spades")
                    {
                        if (currentCard.value > winningCard && !spadesPlayed)
                        {
                            winningCard = currentCard.value;
                            winningPlayer = turnIndex;
                        }
                        if (spadesPlayed && currentCard.suit == "spades" && currentCard.value > winningCard)
                        {
                            winningCard = currentCard.value;
                            winningPlayer = turnIndex;
                        }
                        if (!spadesPlayed && currentCard.suit == "spades")
                        {
                            winningCard = currentCard.value;
                            winningPlayer = turnIndex;
                            spadesPlayed = true;
                        }
                    }
                }
                discardList.Add(currentPlayer[x]);
                discardListValue = currentPlayer[x].value;
                discardListSuit = currentPlayer[x].suit;
                currentPlayer.Remove(currentPlayer[x]);
                if (turnIndex == 1)
                {
                    newCard.transform.SetParent(discard2.transform);
                }
                else
                {
                    newCard.transform.SetParent(discard4.transform);
                }
                GameObject emptyCard = Instantiate(discardPrefab);
                NetworkServer.Spawn(emptyCard);
                Player.player.UpdateDiscards(currentCard.value, currentCard.suit, turnIndex);
                newCard.transform.localScale = new Vector3(1, 1, 1);
                switch (turnIndex)
                {
                    case 0:
                        player1Hand.Clear();
                        foreach (Card c in currentPlayer)
                        {
                            player1Hand.Add(c);
                        }
                        break;
                    case 1:
                        player2Hand.Clear();
                        foreach (Card c in currentPlayer)
                        {
                            player2Hand.Add(c);
                        }
                        break;
                    case 2:
                        player3Hand.Clear();
                        foreach (Card c in currentPlayer)
                        {
                            player3Hand.Add(c);
                        }
                        break;
                    case 3:
                        player4Hand.Clear();
                        foreach (Card c in currentPlayer)
                        {
                            player4Hand.Add(c);
                        }
                        break;
                }
                turnIndex += 1;
                turnCount += 1;
                playDelay = 0;
            }
        }
    }

    public void ShuffleAndDeal()
    {
        if (!isServer)
        {
            return;
        }        
        List<Card> tempDeck = new List<Card>();
        while (deck.Count > 0)
        {
            int index = UnityEngine.Random.Range(0, deck.Count);
            tempDeck.Add(deck[index]);
            deck.Remove(deck[index]);
        }
        foreach (Card c in tempDeck)
        {
            deck.Add(c);
        }
        while (deck.Count > 0)
        {
            player1Hand.Add(deck[0]);
            deck.Remove(deck[0]);
            player2Hand.Add(deck[0]);
            deck.Remove(deck[0]);
            player3Hand.Add(deck[0]);
            deck.Remove(deck[0]);
            player4Hand.Add(deck[0]);
            deck.Remove(deck[0]);
        }
        Player.player.DealHandP1();
        guessCounter.SetActive(true);
        guessButton.SetActive(true);
        guessText.SetActive(true);
    }

    void ServerUpdateP3Hand()
    {
        if (!isServer)
        {
            return;
        }
        foreach (Card c in player3Hand)
        {
            player3values.Add(c.value);
            player3suits.Add(c.suit);
            player3imageName.Add(c.imageName);
        }
    }

    [ClientRpc]
    public void ClientUpdateP3Hand()
    {
        for (int i = 0; i < player3values.Count; i++)
        {
            Card tempCard = new Card();
            tempCard.value = player3values[i];
            tempCard.suit = player3suits[i];
            tempCard.imageName = player3imageName[i];
            foreach (Sprite s in cardFace)
            {
                if (s.name == tempCard.imageName)
                {
                    tempCard.image = s;
                    break;
                }
            }
            player3Hand.Add(tempCard);
        }
        guessCounter.SetActive(true);
        guessButton.SetActive(true);
        guessText.SetActive(true);
    }

    public void CreateCard(Card tempCard)
    {
        newCard = Instantiate(cardPrefab);
        Image newCardImage = newCard.GetComponent<Image>();
        newCardImage.sprite = tempCard.image;
        newCard.GetComponent<CardBehavior>().value = tempCard.value;
        newCard.GetComponent<CardBehavior>().suit = tempCard.suit;
    }

    public void SpawnP3Hand()
    {
        foreach (Card c in player3Hand)
        {
            GameObject card = Instantiate(cardPrefab);
            NetworkServer.Spawn(card);
        }
    }

    public void UpdateServerPoints(int winner)
    {
        switch (winner)
        {
            case 0:
                p1Points += 1;
                GameObject.Find("P1 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P1 Books: " + p1Points.ToString();
                updateText.text = "P1 wins the hand";
                break;
            case 1:
                p2Points += 1;
                GameObject.Find("P2 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P2 Books: " + p2Points.ToString();
                updateText.text = "P2 wins the hand";
                break;
            case 2:
                p3Points += 1;
                GameObject.Find("P3 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P3 Books: " + p3Points.ToString();
                updateText.text = "P3 wins the hand";
                break;
            case 3:
                p4Points += 1;
                GameObject.Find("P4 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P4 Books: " + p4Points.ToString();
                updateText.text = "P4 wins the hand";
                break;
        }
        UpdateClientPoints(winner);
    }

    [ClientRpc]
    public void UpdateClientPoints(int winner)
    {
        DownloadClientPoint(winner);
    }

    public void DownloadClientPoint(int winner)
    {
        switch (winner)
        {
            case 0:
                GameObject.Find("P1 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P1 Books: " + p1Points.ToString();
                updateText.text = "P1 wins the hand";
                break;
            case 1:
                GameObject.Find("P2 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P2 Books: " + p2Points.ToString();
                updateText.text = "P2 wins the hand";
                break;
            case 2:
                GameObject.Find("P3 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P3 Books: " + p3Points.ToString();
                updateText.text = "P3 wins the hand";
                break;
            case 3:
                GameObject.Find("P4 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P4 Books: " + p4Points.ToString();
                updateText.text = "P4 wins the hand";
                break;
        }
    }


    public class Card
    {
        public int value;
        public string suit;
        public Sprite image;
        public string imageName;
    }
}
