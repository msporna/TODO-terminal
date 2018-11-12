
var TASK_ID="";

function initActionMenu(taskId)
{
    TASK_ID=taskId;
}

function onActionMenuCompleteClicked()
{
    completeTask(TASK_ID);
}

function onActionMenuDeleteClicked() {
    if (confirm('DELETE, realy?')) {
        deleteTask(TASK_ID);
    } 
}

function onActionMenuEditClicked(url) {
    window.location.href = "http://localhost:8787"+url;
}

function onActionMenuAddSubtaskClicked(url) {
    window.location.href = "http://localhost:8787" +url;
}

function onActionMenuMoveToTomorrowClicked() {
    moveToBacklog(TASK_ID, 1)
}

function onActionMenuMoveToBacklogClicked() {
    moveToBacklog(TASK_ID, 2)
}



function onActionMenuDoItNowClicked() {
    makeTaskActive(TASK_ID)
}