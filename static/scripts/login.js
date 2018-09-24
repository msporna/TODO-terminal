/*!
  * Copyright 2018 Michal Sporna
  * Licensed under MIT
  */

var ClickedButtons = [];

function attemptToLogin()
{

    window.location = "http://localhost:8787/do_login?login_set=" + ClickedButtons.join();

    ClickedButtons = [];
}

function loginChallengeClicked(button)
{
    ClickedButtons.push(button);
}
