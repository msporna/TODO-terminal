/*!
  * Copyright 2018 Michal Sporna
  * Licensed under MIT
  */

var ParentId;

function init_subtask_page(parent_id) {

    ParentId = parent_id;

    //https://github.com/Mottie/Keyboard/wiki/Setup
    $('#subtaskTitleTextBox').keyboard({
        usePreview: false,
        stayOpen: true,
        accepted: function (e, keyboard, el) {
            $("#subtaskTitleTextBox").attr('class', 'add-new-title-element-class')
        },
        canceled: function (e, keyboard, el) {
            $("#subtaskTitleTextBox").attr('class', 'add-new-title-element-class')
        }
    });

    //hide xp bar
    $("#xp-bar").attr('class', 'hidden');
    $("#account-bar-next-level").attr('class', 'hidden');

}

function saveSUBTASK() {
    var validation_done = false;

    var title = $("#subtaskTitleTextBox").val();



    if (title.length > 0) {
        $.ajax({
            url: "/create_subtask",
            type: "post",
            async: true,
            contentType: 'application/json',
            data: JSON.stringify({
                "title": title,
                "progress":0,
                "parent": ParentId

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
    else {
        alert("Fill title and define progress!");
    }


}

function cancelSUBTASK()
{
    window.location.href = "http://localhost:8787/home";
}


//EVENTS

function onSubtaskKeyboard1FocusReceived() {
    $("#subtaskTitleTextBox").attr('class', 'add-new-title-element-class-focused')
}


function onSubtaskKeyboard2FocusReceived() {
    $("#subtaskDefinedProgressTextBox").attr('class', 'add-new-defined-progress-class-focused')

}
