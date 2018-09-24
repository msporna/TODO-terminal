/*!
  * Copyright 2018 Michal Sporna
  * Licensed under MIT
  */

var ChosenDueDate = new Date();
var Mode = "Add";//default is add,possible also:Edit
var TaskID = undefined; //filled only when editing task
var addNewTagsInput;

function init() {
    //http://selectize.github.io/selectize.js/
    var $select = $('#addNewTagsInput1').selectize({
        plugins: ['remove_button'],
        delimiter: ',',
        persist: false,
        maxItems:3,
        create: function (input) {
            return {
                value: input,
                text: input
            }
        }
    });

    addNewTagsInput = $select[0].selectize;

    //https://github.com/Mottie/Keyboard/wiki/Setup
    $('#todoTitleTextBox').keyboard({
        usePreview: false,
        stayOpen : true,
        accepted: function (e, keyboard, el) {
            $("#todoTitleTextBox").attr('class', 'add-new-title-element-class')
        },
        canceled: function (e, keyboard, el) {
            $("#todoTitleTextBox").attr('class', 'add-new-title-element-class')
        }
    });
    $('#todoDescriptionTextArea').keyboard({
        usePreview: false,
        accepted: function (e, keyboard, el) {
            $("#todoDescriptionTextArea").attr('class', 'add-new-description-area-class')
        },
        canceled: function (e, keyboard, el) {
            $("#todoDescriptionTextArea").attr('class', 'add-new-description-area-class')
        }
    });
    //the one below is for the tags component;
    //it shows keyboard upon clicking the keyboard button
    //then shows it for hidden input and after text is accepted, text is obtained from the hidden input
    //and isnerted into the tags control (new tag created)
    $('#addNewTagsInputHidden1').keyboard({
        usePreview: false,
        accepted: function (e, keyboard, el) {
            addNewTagsInput.createItem($("#addNewTagsInputHidden1").val(), false);
            $("#addNewTagsInputHidden1").attr('class', 'add-new-tags-hidden-class')
        },
        canceled: function (e, keyboard, el) {
            addNewTagsInput.createItem($("#addNewTagsInputHidden1").val(), false);
            $("#addNewTagsInputHidden1").attr('class', 'add-new-tags-hidden-class')
        }
    });

    //https://uxsolutions.github.io/bootstrap-datepicker/
    var $datepicker = $('#addNewDatePicker1').datepicker({
        weekStart: 1,
        todayBtn: "linked",
        orientation: "bottom left",
        daysOfWeekDisabled: "0,6",
        daysOfWeekHighlighted: "1,2,3,4,5",
        todayHighlight: true,
        autoclose: true

    }).on("changeDate", function (e) {
        //alert(e.format(0,"mm/dd/yyyy"));
        //console.log("chosen date on add new todo page " + e.date);
        ChosenDueDate = e.date;

        console.log("chosen due date:"+ChosenDueDate);
    });

    $('#addNewDatePicker1').val(getCurrentDate()); //display current date in the deadline date


    //hide xp bar
    $("#xp-bar").attr('class', 'hidden');
    $("#account-bar-next-level").attr('class', 'hidden');


}

function saveTODO() {
    var validation_done = false;

   var title = $("#todoTitleTextBox").val();
   var description = $("#todoDescriptionTextArea").val();
   var tags = $("#addNewTagsInput1").val();

   if (title.length > 0 && description.length > 0 && tags.length > 0)
   {
       $.ajax({
           url: "/save_todo",
           type: "post",
           async: true,
           contentType: 'application/json',
           data: JSON.stringify({
               "title": title,
               "description": description,
               "dueDate":  moment(ChosenDueDate).format("YYYY-MM-DD"),
               "tags": tags,
               "allowGoogleSync": document.getElementById('allowGoogleSyncCheckbox').checked,
               "mode": Mode,
               "task_id":TaskID
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
   else
   {
       alert("Fill title,description, due date and tags!");
   }


}

function setValuesToEdit(dueDate,title,description,tags,id,hasGoogleSync,hasNotifications)
{

    $("#todoTitleTextBox").val(title);
    $("#todoDescriptionTextArea").val(description);
    $('#addNewDatePicker1').val(dueDate);
    ChosenDueDate = dueDate;

    var tagCollection = tags.split(",");
    for (i = 0; i < tagCollection.length; i++)
    {
        addNewTagsInput.createItem(tagCollection[i], false);
    }

    if (hasGoogleSync == 1)
    {
        $('#allowGoogleSyncCheckbox').prop('checked', true);
    }


    $('#allowGoogleSyncCheckbox').prop('disabled', true);


    TaskID = id;
    Mode = "Edit";
}

function getCurrentDate() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();

    if (dd < 10) {
        dd = '0' + dd
    }

    if (mm < 10) {
        mm = '0' + mm
    }

    today = mm + '/' + dd + '/' + yyyy;

    return today;


}

function cancelTODO()
{
    window.location.href = "http://localhost:8787/home";
}


//EVENTS
function onTagsIconClicked() {
    $('#addNewTagsInputHidden1').getkeyboard().reveal();
    $('#addNewTagsInputHidden1').val("");
    $('#addNewTagsInputHidden1').attr('class', 'add-new-tags-keyboard-visible-class-focused')
}


function onKeyboard1FocusReceived() {
    $("#todoTitleTextBox").attr('class', 'add-new-title-element-class-focused')
}


function onKeyboard2FocusReceived() {
    $("#todoDescriptionTextArea").attr('class', 'add-new-description-area-class-focused')

}
