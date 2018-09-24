/*!
  * Copyright 2018 Michal Sporna
  * Licensed under MIT
  * Parts of the code were taken from https://codepen.io/AfroDev/pen/gbXWjQ
  */

function flicker() {
    $("#xp-increase-fx-flicker").css("opacity", "1");
    $("#xp-increase-fx-flicker").animate({ "opacity": Math.random() }, 100, flicker);
}

$(document).ready(function () {
    flicker();
});

function awardXP(currentValue,percentValue,currentLevel) {
    var xpToSave = 0;
    var levelToSave = 0;

    //first , set current xp on the bar
    setBarValue(currentValue); //(restore)

    if (percentValue != 999) {

        var nextValue = currentValue + percentValue;
        if (nextValue > 100)
    {
        increaseBarValue("100%");//xp bar max is 100% , so first award 100% to levelup
        levelToSave = currentLevel += 1;
        $("#account-bar-next-level").text(levelToSave); //levelup
        xpToSave = nextValue - 100;
        increaseBarValue(xpToSave + "%"); //fill remaining xp after levelup

    }
        else if (nextValue == 100)
    {
        increaseBarValue("100%");//xp bar max is 100% , so first award 100% to levelup
        levelToSave=currentLevel += 1;
        $("#account-bar-next-level").text(levelToSave); //levelup
        //remaining xp is 0
    }
    else
    {
        xpToSave = currentValue + percentValue;
        increaseBarValue(xpToSave + "%");

        levelToSave = currentLevel;
    }
        $("#xp-bar-fill").attr("value", xpToSave);

        //save
        $.ajax({
            url: "/save_xp",
            type: "post",
            async: true,
            contentType: 'application/json',
            data: JSON.stringify({
                "xp": xpToSave,
                "level": levelToSave
            })


        }).done(function (data) {


            if (data != "204") {
                alert("!204: " + data);
            }
            xpToSave = 0;
            levelToSave = 0;

        });
    }

}

function increaseBarValue(value)
{
    $("#xp-increase-fx").css("display", "inline-block");
    $("#xp-bar-fill").css("box-shadow",/*"0px 0px 15px #06f,*/ "-5px 0px 10px #fff inset");
    setTimeout(function () {
        $("#xp-bar-fill").css("-webkit-transition", "all 2s ease");
        $("#xp-bar-fill").css("width", value);
    }, 100);
    setTimeout(function () { $("#xp-increase-fx").fadeOut(500); $("#xp-bar-fill").css({ "-webkit-transition": "all 0.5s ease", "box-shadow": "" }); }, 2000);
}

function setBarValue(value)
{
    $("#xp-bar-fill").css("width", value + "%"); //without animation
}
