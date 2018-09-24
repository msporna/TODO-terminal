/*!
  * Copyright 2018 Michal Sporna
  * Licensed under MIT
  */

var TagFilterChosen = [];

$(document).ready(function () {
    var c = Cookies.get('auth');
    if (c != "true") {
        window.location.href = "http://localhost:8787";
    }

    console.log("VERSION 0.1");


});

function onTabSwitched(whichTab)
{
    console.log("tab switch. Which tab: " + whichTab);

    //show xp bar
    $("#xp-bar").removeAttr('class');
    $("#account-bar-next-level").removeAttr('class');

    if(whichTab==0)
    {
        $("#tab1").attr("class","active");

        $("#tab2").removeAttr("class");
        $("#tab3").removeAttr("class");
        $("#tab4").removeAttr("class");


    }
    else if(whichTab==1)
    {


            $("#tab2").attr("class", "active");

            $("#tab1").removeAttr("class");
            $("#tab3").removeAttr("class");
            $("#tab4").removeAttr("class");



    }
    else if(whichTab==2)
    {
         $("#tab3").attr("class","active");

        $("#tab1").removeAttr("class");
        $("#tab2").removeAttr("class");
        $("#tab4").removeAttr("class");
    }
    else
    {
         $("#tab4").attr("class","active");

        $("#tab1").removeAttr("class");
        $("#tab2").removeAttr("class");
        $("#tab3").removeAttr("class");
    }
}

function doSync()
{
    $.ajax({
        url: "/sync_with_tasks",
        type: "get",
        async: true,
        contentType: 'application/json'


    }).done(function (data) {
        if (data == "204") {
            //refresh
            console.log("204");
            window.location.href = "http://localhost:8787/home";
        } else {
            alert("!204: " + data);

        }

    });
}

function completeTask(taskID)
{

    $.ajax({
        url: "/complete_task",
        type: "post",
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            "task_id": taskID
        })


    }).done(function (data) {


        if (data == "200") {
            //refresh
            console.log("200");
            window.location.href = "http://localhost:8787/home";
        } else {
            alert("!200: " + data);

        }

    });
}

function completeSubtask(subtaskID,parentID) {

    $.ajax({
        url: "/complete_subtask",
        type: "post",
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            "parent_id": parentID,
            "subtask_id": subtaskID
        })


    }).done(function (data) {


        if (data == "200") {
            //refresh
            console.log("200");
            window.location.href = "http://localhost:8787/home";
        } else {
            alert("!200: " + data);

        }

    });
}

function moveToBacklog(taskID,mode)
{
    //1-tomorrow
    //2-future

    $.ajax({
        url: "/move_to_backlog",
        type: "post",
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            "task_id": taskID,
            "mode": mode
        })


    }).done(function (data) {


        if (data == "204") {
            //refresh
            console.log("204");
            window.location.href = "http://localhost:8787/home";
        } else {
            alert("!204: " + data);

        }

    });
}

function deleteTask(taskID)
{
    $.ajax({
        url: "/delete_task",
        type: "post",
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            "task_id": taskID
        })


    }).done(function (data) {


        if (data == "204") {
            //refresh
            console.log("204");
            window.location.href = "http://localhost:8787/home";
        } else {
            alert("!204: " + data);

        }

    });
}

function makeTaskActive(taskID)
{
    $.ajax({
        url: "/make_task_active",
        type: "post",
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            "task_id": taskID
        })


    }).done(function (data) {


        if (data == "204") {
            //refresh
            console.log("204");
            window.location.href = "http://localhost:8787/home";
        } else {
            alert("!204: " + data);

        }

    });
}

function onFilterTagSelected(tag)
{
    TagFilterChosen.push(tag);
}

function onFilterTagUnSelected(tag) {
    var index = array.indexOf(tag);
    if (index > -1) {
        TagFilterChosen.splice(index, 1);
    }
}

function applyFilter() {
    if (TagFilterChosen.length > 0) {
            window.location.href = "http://localhost:8787/home?tagFilterApplied=1&tags=" + TagFilterChosen.join();
        }
        else {
            window.location.href = "http://localhost:8787/home?tagFilterApplied=0";
        }


}
