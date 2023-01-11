using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GuessSlider : MonoBehaviour
{
    public Slider slider;
    public TMPro.TextMeshProUGUI guessNumber;

    public void Start()
    {
        slider.onValueChanged.AddListener(delegate {ChangeValue();});
    }

    public void ChangeValue()
    {
        guessNumber.text = slider.value.ToString();
    }
}
