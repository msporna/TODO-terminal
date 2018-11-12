'''
* Copyright 2018 Michal Sporna
* Licensed under MIT
'''



from datetime import datetime, timedelta
import requests
from flask import render_template, request, Flask, redirect, url_for, make_response
import create_database
from flask_cors import CORS
import json
import os
import sqlite3
from oauth2client import client


CONNECTION_STRING = 'todo.db'
app = Flask(__name__)
CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True

###############################################
# G O O G L E    T A S K S     D E T A I L S 
# (required for google tasks integration)
###############################################

GOOGLE_SECRET = ''
GOOGLE_CLIENT_ID = ''
GOOGLE_REFRESH_TOKEN = ''
GOOGLE_TASK_LIST_ID = ''

###############################################
# /GOOGLE TASK DETAILS
###############################################


XP_REWARD_FOR_SUBTASK = 5
XP_REWARD_FOR_TASK = 10
XP_MAX = 100  # after reaching 100xp, levelup

###############################################
# L O G I N   S E T
###############################################
expected_number_0='6'
expected_number_1='7'
expected_number_2='1'
expected_number_3='1'

# region routes


@app.route('/')
def login():

    resp = make_response(render_template('login.html',
                                         title='TODO_TERMINAL'))
    resp.set_cookie('auth', 'NULL')
    return resp


@app.route('/logout')
def logout():

    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('auth', 'NULL')
    return resp


@app.route('/home')
def home():

    # if tag filter is applied, save this fact to settings
    # so indication can be shown on ui so user knows that he/she is viewing
    # filtered list
    tag_filter_applied = 0
    tag_filter_applied_param = request.args.get(
        'tagFilterApplied', default='', type=int)
    filter_tag_list_param = request.args.get('tags', default='', type=str)

    filter_tag_list = []
    if filter_tag_list_param != "":
        filter_tag_list = filter_tag_list_param.split(",")
    else:
        filter_tag_list = get_setting("tagFilterList")
        if filter_tag_list != None:
            filter_tag_list = filter_tag_list["value"].split(",")

    if tag_filter_applied_param != "":
        tag_filter_applied = tag_filter_applied_param
    else:
        # no param, get setting to see what was set recently
        filter_setting = get_setting("tagFilterOn")
        if filter_setting != None:
            tag_filter_applied = int(filter_setting["value"])

    set_setting("tagFilterOn", str(tag_filter_applied))
    set_setting("tagFilterList", filter_tag_list_param)

    # get today's date

    current_date = datetime.now().strftime('%Y-%m-%d')
    previous_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    results = get_all_tasks()
    todo_items = []
    # filter out results,we want only tasks scheduled for today
    for r in results:
        if r["due_date"] == previous_date:
            # update date to today
            update_task(r["id"], r["title"], r["description"], current_date)
            if r["g_tasks_enabled"]:
                try:
                    g_task_id = update_google_task(
                        r["title"], r["description"], current_date, r["g_task_id"])
                except:
                    print("something went wrong when updating google task. Skipping. No internet?")
                    continue
                # am not updating subtasks on purpose, to see that the task is
                # overdue
            r["due_date"] = current_date
        if r["due_date"] == current_date:
            if tag_filter_applied == 1:
                for filter_tag in filter_tag_list:
                    for task_tag in r["raw_tags"]:
                        if filter_tag == task_tag:
                            todo_items.append(r)
            else:
                todo_items.append(r)

    current_xp_value, level, pending_xp = get_xp()

    return render_template(
        'index.html',
        todo_items=todo_items,
        XP=current_xp_value,
        pending_xp=pending_xp,
        level=level,
        filterApplied=int(tag_filter_applied),
        title='TODO_TERMINAL'
    )


@app.route('/add_todo')
def add_todo():
    """Renders the add_todo page"""
    return render_template(
        'add_todo.html',
        title='Add',
        mode="Add"
    )


@app.route('/filter_tag')
def filter_tag():
    """Renders the filter_tag page"""
    tags = []
    raw_tags = get_all_raw_tags()

    for raw_tag in raw_tags:
        tag = {}
        tag["id"] = raw_tag[0]
        tag["name"] = raw_tag[1]
        tags.append(tag)

    return render_template(
        'tagFilterPage.html',
        tags=tags

    )


@app.route('/add_subtask')
def add_subtask():
    """Renders the add_subtask page"""
    parent_id = request.args.get('parent_id', default='', type=str)
    return render_template(
        'add_subtask.html',
        title='New Subtask',
        parent_id=parent_id
    )

@app.route('/show_action_menu')
def show_action_menu():
    """Renders the action menu page"""
    task_id= request.args.get('task_id', default='', type=str)
    return render_template(
        'action_menu.html',
        title='Action Menu',
        task_id=task_id
    )

@app.route('/show_backlog_action_menu')
def show_backlog_action_menu():
    """Renders the backlog action menu page"""
    task_id= request.args.get('task_id', default='', type=str)
    return render_template(
        'backlog_action_menu.html',
        title='Action Menu',
        task_id=task_id
    )

@app.route('/show_history_action_menu')
def show_history_action_menu():
    """Renders the history action menu page"""
    task_id= request.args.get('task_id', default='', type=str)
    return render_template(
        'history_action_menu.html',
        title='Action Menu',
        task_id=task_id
    )

@app.route('/edit_todo')
def edit_todo():
    """Renders the edit_todo page but for task editing,not adding."""
    task_id = int(request.args.get('task_id'))
    task_details = get_task(task_id)
    # prepare serializable obj
    todo = {}
    todo["id"] = int(task_details[0][0])
    todo["title"] = task_details[0][1]
    todo["description"] = task_details[0][2]
    todo["is_current"] = bool(task_details[0][3])
    todo["is_history"] = bool(task_details[0][4])
    todo["due_date"] = task_details[0][5]
    todo["has_google_sync"] = task_details[0][6]
    todo["has_notifications"] = task_details[0][7]
    todo["tags"] = ",".join(get_all_tags(int(task_details[0][0])))

    # get task and return all fields to edit
    return render_template(
        'add_todo.html',
        title='Edit',
        mode="Edit",
        todo_item=todo

    )


@app.route('/history')
def history():
    """Renders the history page."""

    results = get_all_tasks(active=False)
    todo_items = []

    # filter out results,we want only tasks scheduled for today
    for r in results:
        todo_items.append(r)

    return render_template(
        'history.html',
        title='History',
        todo_items=todo_items
    )


@app.route('/backlog')
def backlog():
    """Renders the backlog page."""
    current_date = datetime.now().strftime('%Y-%m-%d')
    results = get_all_tasks()
    todo_items = []
    # filter out results,we want only tasks that are not scheduled for today
    for r in results:
        if r["due_date"] != current_date:
            todo_items.append(r)
    return render_template(
        'backlog.html',
        title='Backlog',
        todo_items=todo_items
    )


@app.route('/integrations')
def integrations():
    """Renders the integrations  page."""
    return render_template(
        'integrations.html',
        title='Integrations',
        message='Integartions'
    )


@app.route("/do_login")
def do_login():
    # data=json.loads(request.data)
    #login_set = data["login_set"]

    login_set = request.args.get('login_set')
    login_set = login_set.split(',')

    valid = False
    if len(login_set) == 4:
        if login_set[0] == expected_number_0 and login_set[1] == expected_number_1 and login_set[2] == expected_number_2 and login_set[3] == expected_number_3:
            valid = True

    if valid:
        resp = make_response(redirect(url_for('home')))
        resp.set_cookie('auth', 'true')
        return resp
    else:
        resp = make_response(redirect(url_for('login')))
        return resp
# endregion

# region APIS


@app.route("/sync_with_tasks", methods=["GET"])
def sync_with_tasks():
    sync_with_google_tasks()
    return "204"


@app.route("/move_to_backlog", methods=["POST"])
def move_to_backlog():
    data = json.loads(request.data)
    task_id = data["task_id"]
    mode = int(data["mode"])
    task_data = get_task(task_id)
    task_date = datetime.strptime(task_data[0][5], '%Y-%m-%d')
    # add 1 day to the date, moving to backlog means schedule it to tomorrow
    if mode == 1:  # move to tomorrow
        task_date = task_date + timedelta(days=1)
    else:
        # move to future
        task_date = task_date + timedelta(days=300)
    task_date = task_date.strftime('%Y-%m-%d')
    # update google tasks
    if bool(task_data[0][6]):
        g_task_id = update_google_task(task_data[0][1], task_data[0][
                                       2], task_date, task_data[0][8])

        # update due date in subtask google tasks if any
        raw_subtasks = get_task_subtasks(task_data[0][0])
        for raw_subtask in raw_subtasks:
            g_task_id = update_google_task(
                raw_subtask[1], "", task_date, raw_subtask[3])

    # save changes to db
    update_task(task_data[0][0], task_data[0][1], task_data[0][2], task_date)
    return "204"


@app.route("/save_todo", methods=["POST"])
def save_todo():
    '''
    save todo_object into database
    '''
    data = json.loads(request.data)
    task_title = data["title"]
    task_description = data["description"]
    task_dueDate = data["dueDate"]
    tags = data["tags"]
    is_google_sync_enabled = bool(data["allowGoogleSync"])
    # is_notification_enabled=bool(data["allowNotificationsCheckbox"])
    is_notification_enabled = False
    mode = data["mode"]  # add or edit

    task_id = None
   

    try:
        task_id = data["task_id"]
    except:
        task_id = None

    create_or_update_task(task_title,task_description,task_dueDate,tags,is_google_sync_enabled,is_notification_enabled,task_id)
    return '200'


@app.route("/create_subtask", methods=["POST"])
def create_subtask():
    '''
    create subtask.
    NOTE:subtask cannot be updated. To update,user must remove subtask then add it updated.
    To remove, subtask needs to completed by clicking a checkbox on ui.
    '''
    data = json.loads(request.data)
    subtask_title = data["title"]
    subtask_progress = data["progress"]
    parent_task_id = int(data["parent"])
    

    parent_task_data = get_task(parent_task_id)
    # find out if parent has g sync enabled to know if subtask needs to be
    # attached to some gtask
    g_sync_enabled = bool(parent_task_data[0][6])

    create_subtask(subtask_title,subtask_progress,parent_task_id,g_sync_enabled,None,parent_task_data[0][5],parent_task_data[0][8])
    return '200'


@app.route("/complete_subtask", methods=["POST"])
def complete_subtask():
    '''
    complete subtask todo and update overall task progress by defined subtask progress.
    '''
    data = json.loads(request.data)
    subtask_id = int(data["subtask_id"])
    parent_task_id = int(data["parent_id"])
    g_task_id = None

    subtask_data = get_subtask(subtask_id)

    g_sync_enabled = bool(is_task_gsynced(subtask_data[0][5]))
    if g_sync_enabled:
        createupdate_google_task(None, None, str(
            datetime.now()), task_id=subtask_data[0][3], complete=True)

    mark_subtask_as_completed(subtask_id)

    return '200'


@app.route("/make_task_active", methods=["POST"])
def make_task_active():
    '''
    change date of task to today
    '''
    data = json.loads(request.data)
    task_id = data["task_id"]
    task_data = get_task(task_id)

    task_date = datetime.now().strftime('%Y-%m-%d')
    # update google tasks
    if bool(task_data[0][6]):
        g_task_id = update_google_task(task_data[0][1], task_data[0][
                                       2], task_date, task_data[0][8])

        # update due date in subtask google tasks if any
        raw_subtasks = get_task_subtasks(task_data[0][0])
        for raw_subtask in raw_subtasks:
            g_task_id = update_google_task(
                raw_subtask[1], "", task_date, raw_subtask[3])

    # save changes to db
    update_task(task_data[0][0], task_data[0][1], task_data[0][2], task_date)
    return "204"


@app.route("/delete_task", methods=["POST"])
def delete_task():
    '''
    delete task
    '''
    data = json.loads(request.data)
    task_id = int(data["task_id"])
    g_task_id = None

    task_data = get_task(task_id)
    g_sync_enabled = bool(task_data[0][6])
    if g_sync_enabled:
        delete_google_task(task_data[0][8])

    delete_task_from_db(task_id)

    subtasks = get_task_subtasks(task_id)
    for subtask in subtasks:
        delete_subtask_from_db(subtask[0])

    return '204'


@app.route("/complete_task", methods=["POST"])
def complete_task():
    '''
    complete todo task
    '''
    data = json.loads(request.data)
    task_id = int(data["task_id"])
    g_task_id = None

    task_data = get_task(task_id)
    g_sync_enabled = bool(task_data[0][6])
    if g_sync_enabled:
        createupdate_google_task(task_data[0][1], task_data[0][2], task_data[
                                 0][5], task_data[0][8], complete=True)

    mark_task_as_completed(task_id)

    subtasks = get_task_subtasks(task_id)
    for subtask in subtasks:
        mark_subtask_as_completed(subtask[0])

    return '200'


@app.route("/save_xp", methods=["POST"])
def save_xp():
    data = json.loads(request.data)
    xp_to_save = int(data["xp"])
    level_to_save = int(data["level"])
    set_setting("xp", xp_to_save)
    set_setting("level", level_to_save)
    set_setting("pending_xp_award", 999)  # reset
    return '204'

# endregion

# region SQL


def execute_non_query(sql, params=None):
    '''
    generic method used to execute sql query against db
    :param sql:
    :param params:
    :return:
    '''
    result = None
    conn = sqlite3.connect(CONNECTION_STRING)
    c = conn.cursor()
    if params != None:
        result = c.execute(sql, params)
    else:
        result = c.execute(sql)

    conn.commit()
    conn.close()

    inserted_row_id = -1
    try:
        inserted_row_id = result.lastrowid
    except:
        inserted_row_id = -1
    return inserted_row_id


def execute_select(sql, params, fetchall):
    rows = []
    conn = sqlite3.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    if fetchall:
        rows = cursor.fetchall()
    else:
        rows = cursor.fetchone()
    conn.close()
    return rows

# endregion

# region UTIL
# region TAGS


def update_tags(task_id, tags_string):
    tags_collection=""
    if ";" in tags_string:
        tags_collection = tags_string.split(';')
    else:
        tags_collection=tags_string
    if len(tags_collection) > 0:
        unassign_all_tags(task_id)
        for tag in tags_collection:
            inserted_tag_id = insert_tag(tag)
            assign_tag_to_todo(task_id, inserted_tag_id)


def get_all_tags(task_id=None):
    sql = ''
    params = None
    if task_id == None:
        sql = "SELECT * FROM TAGS"
    else:
        sql = "SELECT TAGS.ID,TAGS.tag FROM TAGS INNER JOIN TAGS_TODOS ON TAGS.ID=TAGS_TODOS.tag_id WHERE TAGS_TODOS.todo_id=:tid"
        params = {"tid": task_id}
    results = execute_select(sql, params, fetchall=True)
    # tuple is returned, convert to simple array
    tags_list = []
    fetched_tags = []
    if len(results) > 0:
        try:
            fetched_tags = results[0][1].split(',')
        except:
            fetched_tags = results[0][1]

    return fetched_tags


def get_all_raw_tags():
    sql = "SELECT * FROM TAGS"
    results = execute_select(sql, None, fetchall=True)
    return results


def assign_tag_to_todo(todo_id, tag_id):
    sql = "INSERT INTO TAGS_TODOS(tag_id,todo_id) VALUES(?,?)"
    execute_non_query(sql, (tag_id, todo_id))


def remove_tag_from_todo(todo_id, tag_id):
    # todo
    pass


def insert_tag(tag):
    tags = get_all_tags()
    for t in tags:
        if t.lower() == tag.lower():
            return t[0]
    # if got here, it means specified tag does not exist
    sql = "INSERT INTO TAGS(tag) VALUES(?)"
    inserted_tag_id = execute_non_query(sql, [tag])
    return inserted_tag_id


def unassign_all_tags(task_id):
    sql = "DELETE FROM TAGS_TODOS WHERE todo_id=:tid"
    param = {"tid": task_id}
    execute_non_query(sql, param)


# endregion

# region TASKS

def mark_task_as_completed(task_id):
    sql = "UPDATE TODO SET is_history=1 WHERE ID=:tid"
    param = {"tid": task_id}
    execute_non_query(sql, param)
    
    award_xp(XP_REWARD_FOR_TASK)


def delete_task_from_db(task_id):
    sql = "DELETE FROM TODO WHERE ID=:tid"
    param = {"tid": task_id}
    execute_non_query(sql, param)


def mark_subtask_as_completed(subtask_id):
    sql = "UPDATE TODO_CHILD SET is_history=1 WHERE ID=:tid"
    param = {"tid": subtask_id}
    execute_non_query(sql, param)

    award_xp(XP_REWARD_FOR_SUBTASK)


def delete_subtask_from_db(subtask_id):
    sql = "DELETE FROM TODO_CHILD WHERE ID=:tid"
    param = {"tid": subtask_id}
    execute_non_query(sql, param)


def create_subtask(subtask_title,subtask_progress,parent_task_id,g_sync_enabled=False,g_task_id=None,parent_due_date=None,parent_g_task_id=None):
    if g_sync_enabled and g_task_id==None:
        # create gtask of this subtask
        if parent_due_date==None:
            parent_due_date=datetime.now().strftime('%Y-%m-%d')
        else:
            #make sure that date is in the right format
            try:
                # sometimes date of the task is 2018-09-22 00:00:00 
                # that 00:00:00 need to be removed,so change date to string and then to date without time
                # this is valid only for tasks improted from gtasks via sync
                parent_due_date=datetime.strptime(parent_due_date,'%Y-%m-%d %H:%M:%S')
                parent_due_date=datetime.now().strftime('%Y-%m-%d')
            except:
                # just use parent due date, no converting needed
                print("Using parent due date without any change.")
        g_task_id = createupdate_google_task(
            subtask_title, "", parent_due_date)
        move_google_task(parent_g_task_id, g_task_id)

    # insert subtask to db
    subtask_id=None
    if g_task_id !=None:
        sql = "INSERT INTO TODO_CHILD(title,is_history,g_task_id,defined_progress,parent) VALUES(?,?,?,?,?)"
        subtask_id = execute_non_query(
            sql, (subtask_title, 0, g_task_id, subtask_progress, parent_task_id))
    return subtask_id


def create_or_update_task(task_title,task_description,task_dueDate,tags,is_google_sync_enabled=False,is_notification_enabled=False,task_id=None,g_task_id=None):
    if task_id == None:
        if g_task_id ==None:
            if is_google_sync_enabled:
                google_sync_status = 1
                g_task_id = createupdate_google_task(
                    task_title, task_description, task_dueDate)
            if is_notification_enabled:
                ifft_status = 1
                # todo : start ifft timer
                pass

        sql = "INSERT INTO TODO(title,description,is_current,is_history,due_date,has_google_sync,has_notifications,g_task_id) VALUES(?,?,?,?,?,?,?,?)"
        task_id = execute_non_query(sql, (task_title, task_description,
                                          1, 0, task_dueDate, is_google_sync_enabled, is_notification_enabled, g_task_id))
    else:
        # update
        if g_task_id ==None:
            if is_google_sync_enabled:
                google_sync_status = 1
                g_task_id = update_google_task(
                    task_title, task_description, task_dueDate, get_g_task_id(task_id))
            if is_notification_enabled:
                ifft_status = 1
                # todo : start ifft timer
                pass

        sql = "UPDATE TODO SET title=:title,description=:d,due_date=:dd,has_google_sync=:hgs,has_notifications=:hn,g_task_id=:gtid WHERE id=:id"
        params = {"id": task_id, "title": task_title, "d": task_description,
                  "dd": task_dueDate, "hgs": is_google_sync_enabled, "hn": is_notification_enabled, "gtid": g_task_id}
        execute_non_query(sql, params)

    update_tags(task_id, tags)
    return task_id


def get_task_by_g_id(g_task_id):
    '''
    get task instance by google task id
    '''
    sql = "SELECT * FROM TODO WHERE g_task_id=:gid"
    params = {"gid": g_task_id}
    results = execute_select(sql, params, fetchall=True)
    if len(results)==0:
        return None
    return results


def get_task(task_id=None, active_only=True):
    '''
    return all tasks if id not specified
    return 1 specific task if task id specified
    by default, it returns only active tasks (that are not completed yet)
    active_only applies to getting all tasks only, when getting specific task by id it does not matter. We want specific task.
    '''
    params = None
    sql = None
    if task_id == None:
        sql = "SELECT * FROM TODO"
        if active_only:
            sql += " WHERE is_history=0"
        else:
            sql += " WHERE is_history=1"

    else:
        sql = "SELECT * FROM TODO WHERE ID=:tid"
        params = {"tid": task_id}
    results = execute_select(sql, params, fetchall=True)
    return results


def get_all_tasks(active=True):
    '''
    get all task along with subtasks
    '''
    todo_items = []
    results = get_task(task_id=None, active_only=active)
    for r in results:
        todo = {}
        todo["id"] = int(r[0])
        todo["title"] = r[1]
        todo["description"] = r[2]
        todo["is_current"] = bool(r[3])
        todo["is_history"] = bool(r[4])
        todo["due_date"] = r[5]
        todo["g_task_id"] = r[8]
        todo["g_tasks_enabled"] = bool(r[6])
        all_tags = get_all_tags(int(r[0]))
        todo["tags"] = ",".join(all_tags)
        todo["raw_tags"] = all_tags
        raw_subtasks = get_task_subtasks(todo["id"], active_only=active)
        subtasks = []

        for raw_subtask in raw_subtasks:
            subtask = {}
            subtask["id"] = raw_subtask[0]
            subtask["title"] = raw_subtask[1]
            subtask["g_task_id"] = raw_subtask[3]
            subtasks.append(subtask)
        todo["subtasks"] = subtasks

        todo_items.append(todo)

    return todo_items


def get_subtask(subtask_id=None):
    '''
    return all subtasks if id not specified
    return 1 specific subtask if subtask id specified
    '''
    params = None
    sql = None
    if subtask_id == None:
        sql = "SELECT * FROM TODO_CHILD"
    else:
        sql = "SELECT * FROM TODO_CHILD WHERE ID=:tid"
        params = {"tid": subtask_id}
    results = execute_select(sql, params, fetchall=True)
    return results


def get_task_subtasks(task_id=None, active_only=True):
    '''
    return all subtasks of given task
    '''
    params = None
    sql = None
    sql = "SELECT * FROM TODO_CHILD WHERE parent=:p"
    if active_only:
        sql += " AND is_history=0"
    else:
        sql += " AND is_history=1"
    params = {"p": task_id}
    results = execute_select(sql, params, fetchall=True)
    return results


def get_g_task_id(task_id):
    '''
    get id of task id related to specified task id
    '''
    sql = "SELECT g_task_id FROM TODO WHERE ID=:tid"
    params = {"tid": task_id}
    results = execute_select(sql, params, fetchall=True)
    return results[0][0]


def is_task_gsynced(task_id):
    '''
    get info if task is synced with google tasks
    '''
    sql = "SELECT has_google_sync FROM TODO WHERE ID=:tid"
    params = {"tid": task_id}
    results = execute_select(sql, params, fetchall=True)
    return bool(results[0][0])


def update_task(id, title, description, date):
    sql = "UPDATE TODO SET title=:title,description=:description,due_date=:date WHERE ID=:task_id"
    param = {"task_id": id, "title": title,
             "description": description, "date": date}
    execute_non_query(sql, param)


# endregion

# region SETTIGS

def get_setting(key):
    '''
    setting is in form of : key,value
    '''
    sql = "SELECT * FROM TODO_SETTINGS"
    results = execute_select(sql, None, fetchall=True)
    for r in results:
        setting = r[1].split(',')
        if setting[0] == key:
            setting_dict = {}
            setting_dict["id"] = r[0]
            setting_dict["key"] = setting[0]
            setting_dict["value"] = setting[1]
            return setting_dict
    return None


def set_setting(key, value):
    setting_value = get_setting(key)
    if setting_value == None:
        sql = "INSERT INTO TODO_SETTINGS(setting) VALUES(?)"
        execute_non_query(sql, (key + "," + str(value),))
    else:
        sql = "UPDATE TODO_SETTINGS SET setting=:s WHERE ID=:sid"
        param = {"sid": setting_value["id"], "s": key + "," + str(value)}
        execute_non_query(sql, param)

# endregion

# region XP


def award_xp(xp):
    '''
    this is called when task or subtask is marked as complete
    xp is pending award and is awarded by javascript then post is called
    after the ui animations are done
    to save it
    '''
    pending_xp_setting = get_setting("pending_xp_award")
    value = 0
    if pending_xp_setting != None:
        db_xp = int(pending_xp_setting["value"])
        if db_xp == 999:
            db_xp = 0  # because 999 is a placeholder, meaning there is no new pending value
        value = db_xp + xp
    else:
        value = xp

    set_setting("pending_xp_award", value)


def get_xp():
    pending_xp_setting = get_setting("pending_xp_award")
    current_level_setting = get_setting("level")
    current_xp_setting = get_setting("xp")

    xp_value = 0
    level_value = 0
    pending_xp_value = 999

    if current_level_setting != None:
        level_value = current_level_setting["value"]
    if current_xp_setting != None:
        xp_value = current_xp_setting["value"]
    if pending_xp_setting != None:
        pending_xp_value = pending_xp_setting["value"]

    return int(xp_value), int(level_value), int(pending_xp_value)


# endregion

# endregion

# region GOOGLE TASKS


def sync_with_google_tasks():
    '''
    get all tasks from g tasks and mark those completed as is_history=true
    '''
    # first clear completed tasks from the task list
    clear_completed_google_tasks()
    add_non_existing_google_tasks()
    # now get all the tasks and update status of their instance in todo.db
    headers=prepare_google_tasks_headers()
    response = None
    

    tasks = get_all_tasks()
    for task in tasks:
        if task["g_tasks_enabled"]:
            url = 'https://www.googleapis.com/tasks/v1/lists/' + \
                GOOGLE_TASK_LIST_ID + '/tasks/' + task["g_task_id"]
            response_data = json.loads(
                requests.get(url, None, headers=headers).text)
            if check_if_google_response_has_errors(response_data):
                continue  # skip failed
            if response_data["status"] == "completed":
                mark_task_as_completed(task["id"])
                # now, if task has any subtasks, mark them as completed too
                for subtask in task["subtasks"]:
                    mark_subtask_as_completed(subtask["id"])
            else:
                # task not complete, but subtask possibly is
                for subtask in task["subtasks"]:
                    url = 'https://www.googleapis.com/tasks/v1/lists/' + \
                        GOOGLE_TASK_LIST_ID + '/tasks/' + subtask["g_task_id"]
                    response_data = json.loads(
                        requests.get(url, None, headers=headers).text)
                    if check_if_google_response_has_errors(response_data):
                        continue  # skip failed
                    if response_data["status"] == "completed":
                        mark_subtask_as_completed(subtask["id"])


def clear_completed_google_tasks():
    '''
    Clears all completed tasks from the specified task list. The affected tasks will be marked as 'hidden' and no longer be returned by default when retrieving all tasks for a task list
    '''
    # authorize
    headers=prepare_google_tasks_headers()

    response = None
    url = ''
    # clear
    url = 'https://www.googleapis.com/tasks/v1/lists/' + GOOGLE_TASK_LIST_ID + '/clear'
    response = requests.post(url,
                             None, headers=headers)

    if response.status_code != 204:
        print("unfortunetely completed tasks could not be removed from the task list ( due to error: " +
              str(response.status_code))
        return None

def add_non_existing_google_tasks():
    '''
    if task was created in g tasks but does not yet exist in our db
    create
    '''
    ct=0
    all_google_tasks=get_all_google_tasks()
    for gtask in all_google_tasks["items"]:
        # check if task exists in db 
        task_instance=get_task_by_g_id(gtask["id"])
        if task_instance == None:
            is_parent=False 
            try:
                parent_id=gtask["parent"]
            except:
                # no parent, means this is a parent,not subtask 
                is_parent=True 
            # I want only parents here, no subtasks (adding subtasks for each parent later) so skip if not a parent 
            if not is_parent:
                continue
            gtask_date=None 
            try:
                gtask_date=datetime.strptime(gtask["due"].split("T")[0],'%Y-%m-%d')
            except:
                gtask_date=datetime.now()
            date_obj=gtask_date
            # if not existing, add:
            notes=""
            try:
                notes=gtask["notes"]
            except:
                # no notes ,just copy the title
                notes=gtask["title"]
            task_id=create_or_update_task(gtask["title"],notes,date_obj,["gtask_import"],True,False,None,gtask["id"])
            ct+=1
            print("created task id:"+str(task_id))
            # look for subtasks 
            for subtask_candidate in all_google_tasks["items"]:
                try:
                    if subtask_candidate["parent"]==gtask["id"]:
                        # create
                        create_subtask(subtask_candidate["title"],"0",task_id,True,subtask_candidate["id"])
                        print("created subtask of "+str(task_id))
                except:
                    continue # subtask_candidate without parent - this is no subtask.

    print("all non existing tasks from gtasks imported ("+str(ct)+")")



def prepare_google_tasks_headers():
    access_token = get_google_access_token()
    if access_token == None:
        return None
    headers = {"Authorization": "Bearer " +
               access_token, "Content-Type": "application/json"}
    return headers


def get_all_google_tasks():
    url = 'https://www.googleapis.com/tasks/v1/lists/' + GOOGLE_TASK_LIST_ID + '/tasks' 
    headers=prepare_google_tasks_headers()
    response_data = json.loads(
        requests.get(url, None, headers=headers).text)
    return response_data


def move_google_task(parent_task_id, task_id):
    if task_id==None:
        return
    # authorize
    headers=prepare_google_tasks_headers()
    response = None
    url = ''
    # move
    url = 'https://www.googleapis.com/tasks/v1/lists/' + GOOGLE_TASK_LIST_ID + \
        '/tasks/' + task_id + '/move?parent=' + parent_task_id
    response = requests.post(url,
                             None, headers=headers)

    response_data = json.loads(response.text)

    if check_if_google_response_has_errors(response_data):
        print("unfortunetely task was not created/updated (" +
              str(task_id) + " due to error: " + response.text)
        return None


def createupdate_google_task(title, description, dueDate, task_id=None, complete=False):
    '''
    https://developers.google.com/tasks/v1/reference/tasks/insert
    /
    https://developers.google.com/tasks/v1/reference/tasks/patch
    (creates or updates task)
    :return:
    '''
    dueDate = dueDate + "T22:00:00.000Z"  # we don't care about time, task are always until end of day...
    payload = {}

    if complete:
        payload["status"] = "completed"
    else:
        payload = {

            "kind": "tasks#task",
            "title": title,
            "notes": description,
            "due": dueDate
        }

    # authorize
    headers=prepare_google_tasks_headers()
    response = None
    url = ''
    if task_id == None:
        # create
        url = 'https://www.googleapis.com/tasks/v1/lists/' + GOOGLE_TASK_LIST_ID + '/tasks'
        response = requests.post(url,
                                 data=json.dumps(payload), headers=headers)

    else:
        # update
        url = 'https://www.googleapis.com/tasks/v1/lists/' + \
            GOOGLE_TASK_LIST_ID + '/tasks/' + task_id
        response = requests.patch(url,
                                  data=json.dumps(payload), headers=headers)

    try:
        response_data = json.loads(response.text)

        if check_if_google_response_has_errors(response_data):
            print("unfortunetely task was not created/updated (" +
                  title + " due to error: " + response.text)
            return None

        print("google task created/updated: " + str(response_data["id"]))

        return str(response_data["id"])  # return google task id
    except:
        # if something went wrong, return none
        return None


def delete_google_task(g_task_id):
    headers=prepare_google_tasks_headers()
    response = None
    url = 'https://www.googleapis.com/tasks/v1/lists/' + \
        GOOGLE_TASK_LIST_ID + '/tasks/' + g_task_id

    response = requests.delete(url, headers=headers)
    if not response.ok:
        print("unfortunetely task was not deleted (" +
              g_task_id + " due to error: " + response.text)
    else:
        print("google task: " + g_task_id + " deleted.")


def update_google_task(title, description, dueDate, g_task_id):
    if g_task_id == None:
        g_task_id = createupdate_google_task(title, description, dueDate)
    else:
        createupdate_google_task(title, description, dueDate, g_task_id)

    return g_task_id


def check_if_google_response_has_errors(response):
    try:
        error_element = response["error"]
        print(str(error_element))
    except:
        return False  # no error found, all good

    return True


def get_google_access_token():
    post_payload = {"grant_type": "refresh_token", "client_secret": GOOGLE_SECRET,
                    "client_id": GOOGLE_CLIENT_ID, "refresh_token": GOOGLE_REFRESH_TOKEN}
    access_token = None
    response = None
    try:
        response = requests.post(
            'https://www.googleapis.com/oauth2/v4/token', data=post_payload)
        response_data = json.loads(response.text)
        access_token = response_data["access_token"]
        print("stored access token.")
    except:
        return None

    return access_token
# endregion


def init_db():
    '''
    if db does not exist, create
    :return:
    '''
    if not os.path.exists("todo.db"):
        create_database.create_db()


# BOOTS HERE #####################################################


if __name__ == "__main__":
    init_db()

    app.run(host="0.0.0.0", port=8787)
