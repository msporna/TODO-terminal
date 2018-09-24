
Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Media](#media)
- [Usage](#usage)
   * [Creating tasks](#creating-tasks)
   * [Current tasks](#current-tasks)
   * [Creating subtasks](#creating-subtasks)
   * [Completing subtasks](#completing-subtasks)
   * [Completing tasks](#completing-tasks)
   * [Gaining XP](#gaining-xp)
   * [Updating tasks](#updating-tasks)
   * [Updating subtasks](#updating-subtasks)
   * [Deleting subtasks](#deleting-subtasks)
   * [Filter by tags](#filter-by-tags)
   * [Move task to tomorrow](#move-task-to-tomorrow)
   * [Move task to backlog](#move-task-to-backlog)
   * [Sync with Google Tasks](#sync-with-google-tasks)
      + [Scenario 1 - Task created on device, sync with Google Tasks](#scenario-1---task-created-on-device-sync-with-google-tasks)
      + [Scenario 2 - Task completed via Google Tasks, sync with device](#scenario-2---task-completed-via-google-tasks-sync-with-device)
      + [Scenario 3- Task compelted via device, sync with Google tasks](#scenario-3--task-compelted-via-device-sync-with-google-tasks)
- [Login](#login)
- [Deployment](#deployment)
- [License](#license)

# Introduction

This is yet another web TODO app but designed for 3.5" inch screen and Raspberry pi. The idea is for this device to serve as task tracking device, replacing regular notebook and having to write stuff with pen. Editing tasks on paper is, let's say, not user friendly. As I'm a person who likes to write tasks down physically, I figured this project would make my life easier. <br>

# Features:

- Create,modify,delete todo tasks on your raspberry pi screen via stylus
- Create subtasks
- Assign tags to tasks
- The main tab presents tasks scheduled for current day, the rest is in the backlog
- If today's task was not done, it will be automatically scheduled for the next day
- Tasks can be freely moved between active and backlog sections
- Designed for touch screen, input is handled by virtual keyboard
- Tasks&subtasks can be synced with Google Task app on android/ios - there is a checkbox to enable it during task creation. All tasks created in TODO TERMINAL are then created in Google Tasks. If Task is completed, it gets marked as such in Google Tasks app and vice versa.
- History tab for historical data
- Filter active tasks by tag
- Login screen

# Media

![screenshot1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/main.jpg)

![input](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/2.jpg)

![action menu](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/3.jpg)

![main menu](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/4.jpg)

![add task screen](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/7.jpg)

![sync with Google Tasks](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/IMG_0087.JPG)

# Usage

## Creating tasks

1. Open main menu <br>

![step1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/create/create1.PNG)

2. Tap on 'New' <br>

![step2](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/create/create2.PNG)

3. New window will be shown <br>

![step3](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/create/create3.PNG)

4. Set due date (1), check whether this task should sync with Google Tasks or not (2), set title (3), description (4), add at least 1 tag (5)

5. Accept by clicking 'Save' (6)
6. If everything goes well, the main page (current tab) will be shown

## Current tasks

Tasks with due date set to today's date are always displayed under 'Current' tab. It is the main page of the app.

## Creating subtasks

1. Go to current tab or backlog and focus on task for which subtask needs to be added
2. Tap on [A] button standing for 'Action'

![step1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/subtask/subtask1.PNG)

3. Select 'add subtask'

![step2](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/subtask/subtask2.PNG)

4. New subtask page will be shown with only 1 field - subtask title

![step3](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/subtask/subtask3.PNG)

5. Specify the title and accept by clicking 'Save'

6. The main page (current tab) will be shown. The Subtask will be shown as a checkbox under the specific task. To expand Task, click on task's title.

![step4](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/subtask/subtask4.PNG)

## Completing subtasks

To complete subtask, simply check the corresponding checkbox. The subtask will dissapear from the task.

![step1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/completingSubtask/completeSubtask1.PNG)

## Completing tasks

To complete a task, expand the Action menu [A] and select "it's done!". Page will be reloaded.

![step1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/completeTask/completeTask1.PNG)

## Gaining XP

XP points are given everytime a subtask or task is completed. When the bar is fully filled, level is increased and xp points go back to 0 just to be gained again to get another level. Pure fun.

![xp](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/xp.PNG)

## Updating Tasks

To update a task, click on [A] Action menu and select Edit. New window will be shown - update title,description,due date and tags. The only thing that cannot be updated is Google Tasks checkbox.

![step1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/deleteEditTask.PNG)

## Updating Subtasks

Subtask cannot be updated. To update, mark subtask as complete and then add it again, updated.

## Deleting Tasks

Click on Action [A] menu to open it and then select 'Delete'.

![step1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/deleteEditTask.PNG)

Task can be deleted from current,backlog and history tabs.

## Deleting Subtasks

Subtask cannot be deleted per say, it can be completed. So if you need to make subtask dissapear, just complete it.

## Filter by tags

Once you have some tasks in place with various tags, you can filter them to show only those, related to selected task.

1. Go to Filter window by clicking on Action [A] menu and selecting Filter

![step1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/filter/filter1.PNG)

2. Select tags you want to show tasks related to. If you want to show all, uncheck all

![step2](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/filter/filter2.PNG)

3. Apply
4. Main page (current tab) will be shown. It will have '\*' symbol in tab's title to indicate that filter is ON.

![step3](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/filter/filter3.PNG)

## Move task to tomorrow

A task can be moved to the next day if it is known that it won't be done in the current day. To do so, go to Action [A] menu and select 'Todo tomorrow'

![step1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/move/move1.PNG)

## Move task to backlog

A task can be moved to backlog if will be done in unspecified future. By doing that, 300 days will be added to task's due date.

Go to Action [A] menu and select '-> backlog'

![step1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/move/moveBacklog.PNG)

## Sync with Google Tasks

### Setup

Rest API experience needed.

You need to provide 4 things in order to enable Google Task sync:
GOOGLE_SECRET,GOOGLE_CLIENT_ID,GOOGLE_REFRESH_TOKEN,GOOGLE_TASK_LIST_ID

Those are specified in views.py, line 25.

**How to obtain GOOGLE_SECRET,GOOGLE_CLIENT_ID?**

https://developers.google.com/identity/protocols/OAuth2WebServer?authuser=0 <br>
Paragraph:Obtaining OAuth 2.0 access tokens

**How to obtain GOOGLE_REFRESH_TOKEN?**

This is described under link: https://developers.google.com/identity/protocols/OAuth2WebServer?authuser=0 <br>
paragraph: Step 5: Exchange authorization code for refresh and access tokens<br>
Response will contain both access_token and refresh_token. Refresh token is what you need here.

**How to obtain GOOGLE_TASK_LIST_ID?**

1. create a new list in Google Tasks app
2. fetch all tasklists via https://www.googleapis.com/tasks/v1/users/@me/lists GET call (do it manually via Postman or similar tool)
3. get tasklist id that you want and specify it in views.py

### Scenario 1 - Task created on device, sync with Google Tasks

1. create a task on device with Google Task sync enabled
2. make sure the task shows up in Google Tasks app on your device or web
   (if setup was done correctly)

### Scenario 2 - Task completed via Google Tasks, sync with device

1. create task on device with Google Task sync enabled
2. make sure the task shows up in Google Tasks app on your device or web
3. finish task in Google Tasks app
4. go to menu on device
5. Select 'Sync'

![step1](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/guide/Sync.PNG)

6. Task on device will be marked as completed after the sync is done correctly & moved to history tab

### Scenario 3- Task compelted via device, sync with Google tasks

1. create task on device with Google Task sync enabled
2. make sure the task shows up in Google Tasks app on your device or web
3. finish task on device, from the current tab
4. task will be finished on device & moved to the history tab and completed in the Google Tasks app

# Login

Login screen is the first screen that user sees. Login is required to view main app. Login is based on a simple, yet sufficient for such project mechanism: there are 8 buttons and 4 of them need to be tapped in a correct order.

Default combination is this:

![login screen](https://github.com/msporna/TODO-terminal/blob/master/docs/screenshots/6.jpg)

It can be modified in views.py file, line 245:<br/>
`if login_set[0] == '6' and login_set[1] == '7' and login_set[2] == '1' and login_set[3] == '1': valid = True`

The values: 6,7,1,1 are passed from login.js script and those are defined in login.html template:<br>

`<button onclick="loginChallengeClicked(1);" class="login-challenge-b1">?</button>`
`<button onclick="loginChallengeClicked(2);" class="login-challenge-b2">?</button>`
`<button onclick="loginChallengeClicked(3);" class="login-challenge-b3">?</button>`
`<button onclick="loginChallengeClicked(4);" class="login-challenge-b4">?</button>`
`<button onclick="loginChallengeClicked(5);" class="login-challenge-b5">?</button>`
`<button onclick="loginChallengeClicked(6);" class="login-challenge-b6">?</button>`
`<button onclick="loginChallengeClicked(7);" class="login-challenge-b7">?</button>`
`<button onclick="loginChallengeClicked(8);" class="login-challenge-b8">?</button>`

So after you decide which 4 buttons and in which order are required for login, just update line 245 in views.py with your selected values corresponding to buttons from login.html.

# Deployment

todo

# License

Licensed under MIT
