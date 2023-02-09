using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using TMPro;

using Unity.Netcode.Transports.UTP;
using Unity.Services.Authentication;
using Unity.Services.Core;
using Unity.Services.Relay;
using Unity.Services.Relay.Models;
using UnityEngine;
using System;
using UnityEngine.Networking;
using System.Text;
using UnityEngine.UI;
using Mirror;


public class Relay : MonoBehaviour
{
    [SerializeField] private TMP_Text joinCodeText;
    [SerializeField] private TMP_InputField joinInput;
    [SerializeField] private GameObject joinButton;
    [SerializeField] private GameObject createButton;
    [SerializeField] private GameObject background;
    [SerializeField] private GameObject titleScreen;
    [SerializeField] private GameObject nm;
    [SerializeField] private GameObject dm;

    private NetworkManager manager;
    //private UnityTransport transport;
    private const int maxPlayers = 2;

    private async void Awake()
    {   
        nm = GameObject.Find("Network Manager");
        manager = nm.GetComponent<NetworkManager>();
        //transport = FindObjectOfType<UnityTransport>();

        await Authenticate();

        joinButton.SetActive(true);
        createButton.SetActive(true);

    }
    
    private static async Task Authenticate()
    {
        await UnityServices.InitializeAsync();
        await AuthenticationService.Instance.SignInAnonymouslyAsync();
    }

    public async void CreateGame()
    {
        Allocation a = await RelayService.Instance.CreateAllocationAsync(maxPlayers);
        joinCodeText.text = await RelayService.Instance.GetJoinCodeAsync(a.AllocationId);
        //transport.SetHostRelayData(a.RelayServer.IpV4, (ushort)a.RelayServer.Port, a.AllocationIdBytes, a.Key, a.ConnectionData);


        manager.StartHost();
        titleScreen.SetActive(false);
        background.SetActive(false);
        dm.SetActive(true);
    }

    public async void JoinGame()
    {
        JoinAllocation a = await RelayService.Instance.JoinAllocationAsync(joinInput.text.ToUpper());
        manager.networkAddress = "localhost";
        manager.StartClient();
        titleScreen.SetActive(false);
        background.SetActive(false);
        dm.SetActive(true);
    }
}
