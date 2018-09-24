import sqlite3

SCHEMA_VER="1"
PATH = 'todo.db'


def create_db():
    conn = sqlite3.connect(PATH)
    c = conn.cursor()

    ######################################################################################
    ##################  T A B L E       C R E A T I O N S   ##############################
    ##################                                      ##############################
    ######################################################################################

    '''
    [TODO] table
    '''
    c.execute('''CREATE TABLE TODO(ID INTEGER PRIMARY KEY AUTOINCREMENT,title VARCHAR(160),description VARCHAR(4000),is_current INTEGER,is_history INTEGER,due_date DATETIME,has_google_sync INTEGER,has_notifications INTEGER,g_task_id VARCHAR(100))''')
    
    '''
    [TODO_CHILD] table
    '''
    c.execute('''CREATE TABLE TODO_CHILD(ID INTEGER PRIMARY KEY AUTOINCREMENT,title VARCHAR(160),is_history INTEGER,g_task_id VARCHAR(100),defined_progress VARCHAR(10),parent INTEGER)''')


    '''
    [TAGS] table
    '''
    c.execute('''CREATE TABLE TAGS(ID INTEGER PRIMARY KEY AUTOINCREMENT, tag VARCHAR(50))''')

    '''
    [TAGS_TODOS] table
    '''
    c.execute('''CREATE TABLE TAGS_TODOS(ID INTEGER PRIMARY KEY AUTOINCREMENT, tag_id INTEGER, todo_id INTEGER )''')

    '''
    [SETTINGS] table
    '''
    c.execute('''CREATE TABLE TODO_SETTINGS(ID INTEGER PRIMARY KEY AUTOINCREMENT, setting VARCHAR(100) )''')

    conn.close()


