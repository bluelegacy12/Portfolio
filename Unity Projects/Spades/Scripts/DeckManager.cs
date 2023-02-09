using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Mirror;
using UnityEngine.UI;
using static Player;
using System.Linq;
using TMPro;

public class DeckManager : NetworkBehaviour
{
    [SyncVar]
    public int goal = 300;
    public TMPro.TextMeshProUGUI goalText;
    public GameObject goalInput;
    public static DeckManager deckManager;
    public GameObject cardPrefab;
    public GameObject discardPrefab;
    public TMPro.TextMeshProUGUI updateText;
    [SyncVar]
    public int readyPlayers = 0;
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
    public List<int> player3values = new List<int>();
    public List<string> player3suits = new List<string>();
    public List<string> player3imageName = new List<string>();
    public GameObject nm;
    public GameObject discard1;
    public GameObject discard2;
    public GameObject discard3;
    public GameObject discard4;
    public GameObject guessCounter;
    public GameObject guessButton;
    public GameObject guessText;
    public GameObject nextRoundButton;
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
    public TMPro.TextMeshProUGUI p1PointsText;
    public TMPro.TextMeshProUGUI p2PointsText;
    public TMPro.TextMeshProUGUI p3PointsText;
    public TMPro.TextMeshProUGUI p4PointsText;
    public TMPro.TextMeshProUGUI nil1;
    public TMPro.TextMeshProUGUI nil2;
    public TMPro.TextMeshProUGUI nil3;
    public TMPro.TextMeshProUGUI nil4;
    public GameObject endScreen;
    public GameObject restartButton;
    public TMPro.TextMeshProUGUI team13endScore;
    public TMPro.TextMeshProUGUI team24endScore;
    public TMPro.TextMeshProUGUI endText;

    // Start is called before the first frame update
    void Start()
    {
        deckManager = this;
        waitForNext = true;
        nextTurnButton.SetActive(false);
        nextRoundButton.SetActive(false);
        suitDisplay.SetActive(false);
        startButton.SetActive(true);
        guessCounter.SetActive(false);
        guessButton.SetActive(false);
        endScreen.SetActive(false);
        nil1.gameObject.SetActive(false);
        nil2.gameObject.SetActive(false);
        nil3.gameObject.SetActive(false);
        nil4.gameObject.SetActive(false);
        updateText = GameObject.Find("UpdateText").GetComponent<TMPro.TextMeshProUGUI>();
        discard1 = GameObject.Find("Discard1");
        discard2 = GameObject.Find("Discard2");
        discard3 = GameObject.Find("Discard3");
        discard4 = GameObject.Find("Discard4");
        guessText = GameObject.Find("Guess Number");
        nm = GameObject.Find("Network Manager");
        if (!isServer)
        {
            goalInput.SetActive(false);
        }
        else
        {
            goalInput.SetActive(true);
            updateText.text = "Welcome to Spades! Please set the winning score to compete for.";
        }
    }

    void Update()
    {
        if (goalInput.activeSelf)
        {
            TMP_InputField input = goalInput.GetComponent<TMP_InputField>();
            if (input.text != null)
            {
                int.TryParse(input.text, out goal);
            }
        }
        if (nextRoundButton.activeSelf)
        {
            player3values.Clear();
            player3suits.Clear();
            player3imageName.Clear();
            if (p1Points + p3Points >= p1p3Total)
            {
                team13PointsText.text = "Team 1&3 Points: " + team13Points.ToString();
                team13BagsText.text = "Team 1&3 Bags: " + team13Bags.ToString();
                updateText.text = "Your total points are now: " + team13Points.ToString() + ", and your bags are: " + team13Bags.ToString() + ".";
            }
            else
            {
                updateText.text = "Your team busted! No points were earned this round.";
            }
            team24PointsText.text = "Team 2&4 Points: " + team24Points.ToString();
            team24BagsText.text = "Team 2&4 Bags: " + team24Bags.ToString();
            p1PointsText.text = "P1 Books: " + p1Points.ToString();
            p2PointsText.text = "P2 Books: " + p2Points.ToString();
            p3PointsText.text = "P3 Books: " + p3Points.ToString();
            p4PointsText.text = "P4 Books: " + p4Points.ToString();
        }
        
        if (readyPlayers == 3 && !guessButton.activeSelf)
        {
            updateText.text = "Waiting for other players";
        }
        if (guessButton.activeSelf)
        {
            updateText.text = "How many books do you think you can win?";
            team13Guess.text = "Team 1&3 Guess: 0";
            team24Guess.text = "Team 2&4 Guess: 0";
            p1Points = 0;
            p2Points = 0;
            p3Points = 0;
            p4Points = 0;
            p1PointsText.text = "P1 Books: 0";
            p2PointsText.text = "P2 Books: 0";
            p3PointsText.text = "P3 Books: 0";
            p4PointsText.text = "P4 Books: 0";
        }
        if (amountOfGuessers == 2)
        {
            p1p3Total = Player.player.guessNumber + p3Guess;
            waitForNext = false;
        }
        if (firstTurn && !waitForNext)
        {
            team13Guess.text = "Team 1&3 Guess: " + p1p3Total.ToString();
            team24Guess.text = "Team 2&4 Guess: " + p2p4Total.ToString();
            amountOfGuessers = 0;
            readyPlayers = 0;
        }
        if (firstTurn && turnCount > 0)
        {
            firstTurn = false;
        }
        if (readyPlayers == 2)
        {
            readyPlayers = 3;
            if (goal > 1000)
            {
                goal = 1000;
            }
            if (goal < 300)
            {
                goal = 300;
            }
            goalText.text = "Score to Win: " + goal.ToString();
            UpdateClientGoal(goal);
            playerReconnect = readyPlayers;
            foreach (GameObject c in GameObject.FindGameObjectsWithTag("Card"))
            {
                if (c.name == "Suit Display")
                {
                    continue;
                }
                Destroy(c);
            }
            foreach (GameObject c in Resources.FindObjectsOfTypeAll<GameObject>().Where(obj => obj.name == "New Game Object"))
            {
                if (c.name == "New Game Object")
                {
                    Destroy(c);
                }                
            }
            foreach (GameObject c in GameObject.FindGameObjectsWithTag("Discard"))
            {
                Destroy(c);
            }
            if (isServer)
            {
                ShuffleAndDeal();
                ServerUpdateP3Hand();
                ClientUpdateP3Hand(player3values, player3suits, player3imageName);
                SpawnP3Hand();
                Player.player.DealHandP3();
            }
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
            GameObject.Find("P3 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P3 Books: " + p3Points.ToString();
            updateText.text = "Your turn!";
        }
        if ((isServer && turnIndex == 2) || (!isServer && turnIndex == 0))
        {
            if (waitForNext || textHold){return;}
            GameObject.Find("P3 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P3 Books: " + p3Points.ToString();
            updateText.text = "It's your partner's turn";
        }
        if (turnIndex == 1 || turnIndex == 3)
        {
            SyncClientPoints();
            if (waitForNext || textHold){return;}
            GameObject.Find("P3 Books").GetComponent<TMPro.TextMeshProUGUI>().text = "P3 Books: " + p3Points.ToString();
            updateText.text = "Player " + (turnIndex + 1) + "'s turn";

        }
        if (turnCount == 4)
        {
            turnCount = 5;
            waitForNext = true;
            UpdateServerPoints(winningPlayer);

            // calc points at end of each round
            if (Player.player.playerHand.transform.childCount == 0)
            {
                if (isServer)
                {
                    if (p1Points + p3Points >= p1p3Total)
                    {
                        if ((nil1.gameObject.activeSelf && p1Points > 0) || (nil3.gameObject.activeSelf && p3Points > 0))
                        {
                            updateText.text = "Your team busted on nil! The player with nil must get 0 points to win big.";
                        }
                        else if ((nil1.gameObject.activeSelf && p1Points == 0) || (nil3.gameObject.activeSelf && p3Points == 0))
                        {
                            team13Points += 100;
                        }
                        if ((!nil1.gameObject.activeSelf && !nil3.gameObject.activeSelf) || ((nil1.gameObject.activeSelf && p1Points == 0) || (nil3.gameObject.activeSelf && p3Points == 0)))
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
                    }
                    else
                    {
                        updateText.text = "Your team busted! No points were earned this round.";
                    }
                    if (p2Points + p4Points >= p2p4Total)
                    {
                        
                        if ((nil2.gameObject.activeSelf && p2Points == 0) || (nil4.gameObject.activeSelf && p4Points == 0))
                        {
                            team24Points += 100;
                        }
                        if ((!nil2.gameObject.activeSelf && !nil4.gameObject.activeSelf) || ((nil2.gameObject.activeSelf && p2Points == 0) || (nil4.gameObject.activeSelf && p4Points == 0)))
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
                }
                firstTurn = true;
                if (team13Points >= goal || team24Points >= goal)
                {
                    string winningTeam;
                    if (team13Points > team24Points)
                    {
                        winningTeam = "Player 1 and 3";
                    }
                    else if (team13Points < team24Points)
                    {
                        winningTeam = "Player 2 and 4";
                    }
                    else
                    {
                        if (team13Bags < team24Bags)
                        {
                            winningTeam = "Player 1 and 3";
                        }
                        else if (team13Bags > team24Bags)
                        {
                            winningTeam = "Player 2 and 4";
                        }
                        else
                        {
                            winningTeam = "tie";
                        }
                    }
                    float delay = 0;
                    while (delay < 1.5f)
                    {
                        delay += Time.deltaTime;
                    }
                    EndGame(winningTeam);
                    EndClientGame(winningTeam);
                    return;
                }
                ClientNextRound();
                nextRoundButton.SetActive(true);
                readyPlayers = 0;
                amountOfGuessers = 0;
                spades = false;
                spadesPlayed = false;
                winningCard = 0;
                leadingSuit = "clubs";
                nil1.gameObject.SetActive(false);
                nil2.gameObject.SetActive(false);
                nil3.gameObject.SetActive(false);
                nil4.gameObject.SetActive(false);
            }
            else if (isServer)
            {
                nextTurnButton.SetActive(true);
            }
        }
        if (turnCount == 5 && !firstTurn)
        {
            UpdateClientPoints(winningPlayer);
        }
        if (!Player.player.isServer)
        {
            return;
        }
        if (turnIndex != 0 && turnCount < 4 && turnIndex != 2 && !waitForNext)
        {
            // ai card play logic
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
                    // if player is not starting the round, play the highest card of the correct suit
                    if (turnCount != 0 && currentCard.value < c.value && leadingSuit == c.suit)
                    {
                        // if the chosen card is not going to win the hand or is going to undermine their partner, don't play it
                        if (c.value > winningCard && ((turnIndex == 1 && winningPlayer != 3) || (turnIndex == 3 && winningPlayer != 1)))
                        {
                            // if a spade has been played, then don't play high
                            if ((spadesPlayed && c.suit == "spades") || !spadesPlayed)
                            {
                                currentCard = c;
                                cardFound = true;
                            }
                        }
                    }
                    // if player is starting the round, play the highest card
                    if (turnCount == 0)
                    {
                        if (currentCard.value < c.value)
                        {
                            if ((c.suit == "spades" && spades) || c.suit != "spades")
                            {
                                currentCard = c;
                                cardFound = true;
                            }
                        }
                    }
                }
                if (!cardFound)
                {
                    // if no good play yet, play lowest card of correct suit
                    currentCard.value = 14;
                    foreach (Card c in currentPlayer)
                    {
                        if (currentCard.value >= c.value && leadingSuit == c.suit)
                        {
                            currentCard = c;
                            cardFound = true;
                        }
                    }
                }
                if (!cardFound)
                {
                    // if no good play found yet, play the lowest spade
                    currentCard.value = 14;
                    foreach (Card c in currentPlayer)
                    {
                        if (c.suit == "spades" && c.value <= currentCard.value)
                        {
                            // if player is going to undermine their partner, don't play it
                            if ((turnIndex == 1 && winningPlayer != 3) || (turnIndex == 3 && winningPlayer != 1))
                            {
                                currentCard = c;
                                cardFound = true;
                            }
                        }
                    }
                }
                if (!cardFound)
                {
                    // if no good play, throw lowest card
                    currentCard.value = 14;
                    foreach (Card c in currentPlayer)
                    {
                        // if trying to throw, don't play a spade
                        if (currentCard.value >= c.value && c.suit != "spades")
                        {
                            currentCard = c;
                            cardFound = true;
                        }
                    }
                }
                if (!cardFound)
                {
                    // if spades are all that's left, play the lowest
                    currentCard.value = 14;
                    foreach (Card c in currentPlayer)
                    {
                        if (currentCard.value >= c.value)
                        {
                            currentCard = c;
                            cardFound = true;
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
        deck.Clear();
        discardList.Clear();
        player1Hand.Clear();
        player2Hand.Clear();
        player3Hand.Clear();
        player4Hand.Clear();
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
        player1Hand = OrganizeHand(player1Hand);
        player3Hand = OrganizeHand(player3Hand);
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

    [Command(requiresAuthority = false)]
    public void ServerDealP3Hand()
    {
        ClientRefreshP3Hand();
        Player.player.DealHandP3();
    }

    public void ClientRefreshP3Hand()
    {
        ClientUpdateP3Hand(player3values, player3suits, player3imageName);
    }

    [ClientRpc]
    public void ClientUpdateP3Hand(List<int> values, List<string> suits, List<string> images)
    {
        player3Hand.Clear();
        guessCounter.SetActive(true);
        guessButton.SetActive(true);
        guessText.SetActive(true);
        for (int i = 0; i < values.Count; i++)
        {
            Card tempCard = new Card();
            tempCard.value = values[i];
            tempCard.suit = suits[i];
            tempCard.imageName = images[i];
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
        Debug.Log("player 3 hand: " + player3Hand[0].value.ToString());
        
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
    [ClientRpc]
    public void UpdateClientGoal(int num)
    {
        goal = num;
        goalText.text = "Score to Win: " + goal.ToString();
    }

    public void SyncClientPoints()
    {
        p1PointsText.text = "P1 Books: " + p1Points.ToString();
        p2PointsText.text = "P2 Books: " + p2Points.ToString();
        p3PointsText.text = "P3 Books: " + p3Points.ToString();
        p4PointsText.text = "P4 Books: " + p4Points.ToString();
    }

    [ClientRpc]
    public void ClientNextRound()
    {
        nextRoundButton.SetActive(true);        
        readyPlayers = 0;
        amountOfGuessers = 0;
        firstTurn = true;
        deck.Clear();
        player1Hand.Clear();
        player2Hand.Clear();
        player3Hand.Clear();
        player4Hand.Clear();
        turnCount = 0;
        discardList.Clear();
        suitDisplay.gameObject.SetActive(false);
        spades = false;
        winningCard = 0;
        leadingSuit = "clubs";
        nil1.gameObject.SetActive(false);
        nil2.gameObject.SetActive(false);
        nil3.gameObject.SetActive(false);
        nil4.gameObject.SetActive(false);
    }

    public void EndGame(string text)
    {
        endScreen.SetActive(true);
        if (text == "tie")
        {
            endText.text = "It's a tie! Well played.";
        }
        else
        {
            endText.text = text + " won the game!";
        }
        team13endScore.text = "Team 1 & 3 Score: " + team13Points.ToString() + " & " + team13Bags.ToString() + " Bags";
        team24endScore.text = "Team 2 & 4 Score: " + team24Points.ToString() + " & " + team24Bags.ToString() + " Bags";
        
    }

    [ClientRpc]
    public void EndClientGame(string text)
    {
        endScreen.SetActive(true);
        if (text == "tie")
        {
            endText.text = "It's a tie! Well played.";
        }
        else
        {
            endText.text = text + " won the game!";
        }
        team13endScore.text = "Team 1 & 3 Score: " + team13Points.ToString() + " & " + team13Bags.ToString() + " Bags";
        team24endScore.text = "Team 2 & 4 Score: " + team24Points.ToString() + " & " + team24Bags.ToString() + " Bags";
    }

    public List<Card> OrganizeHand(List<Card> hand)
    {
        List<Card> newHand = new List<Card>();
        List<Card> tempHandH = new List<Card>();
        List<Card> tempHandC = new List<Card>();
        List<Card> tempHandD = new List<Card>();
        List<Card> tempHandS = new List<Card>();
        foreach (Card c in hand)
        {
            if (c.suit == "hearts")
            {
                tempHandH.Add(c);
            }
            if (c.suit == "clubs")
            {
                tempHandC.Add(c);
            }
            if (c.suit == "diamonds")
            {
                tempHandD.Add(c);
            }
            if (c.suit == "spades")
            {
                tempHandS.Add(c);
            }
        }
        tempHandH = OrganizeSuit(tempHandH);
        tempHandC = OrganizeSuit(tempHandC);
        tempHandD = OrganizeSuit(tempHandD);
        tempHandS =  OrganizeSuit(tempHandS);

        foreach (Card c in tempHandH)
        {
            newHand.Add(c);
        }
        foreach (Card c in tempHandC)
        {
            newHand.Add(c);
        }
        foreach (Card c in tempHandD)
        {
            newHand.Add(c);
        }
        foreach (Card c in tempHandS)
        {
            newHand.Add(c);
        }
        return newHand;
    }

    public List<Card> OrganizeSuit(List<Card> hand)
    {
        List<Card> newHand = hand;
        Card tempCard = new Card();
        int counter = 1;
        while (counter > 0)
        {
            counter = 0;
            for (int i = 1; i < hand.Count; i++)
            {
                if (newHand[i].value < newHand[i - 1].value)
                {
                    tempCard = hand[i];
                    newHand.RemoveAt(i);
                    newHand.Insert(i - 1, tempCard);
                    counter++;
                }
            }
        }
        return newHand;
    }

    public class Card
    {
        public int value;
        public string suit;
        public Sprite image;
        public string imageName;
    }
}
