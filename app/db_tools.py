from re import T
import sqlite3

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #sqlite3.connect(DB_FILE)
c = db.cursor()

stories_header = "(storyName TEXT, fullStory TEXT, lastAdded TEXT, Contributors TEXT)"
users_header = ("(username TEXT, password TEXT)")

def create_table(name, header):
    c.execute(f"CREATE TABLE IF NOT EXISTS {name} {header}")

create_table("StoryInfo", stories_header)
create_table("UserInfo", users_header)

def get_table_list(tableName):
    res = c.execute(f"SELECT * from {tableName}")
    return res.fetchall()
#add data row to sqlTable, put row in list format
#if username already in db returns -1
def add_account(username, password):
    if not(account_exists(username)):
        c.execute("INSERT INTO UserInfo (username, password) VALUES (?, ?);", (username, password))
    else:
        return -1

def account_exists(username):
    accounts = get_table_list("UserInfo")
    for account in accounts:
        if account[0] == username:
            return True
    return False
#return true if username and password are in db, false if one isn't
def verify_account(username, password):
    accounts = get_table_list("UserInfo")
    for account in accounts:
        if account[0] == username and account[1] == password:
            return True
    return False


def story_exists(storyName):
    stories = get_table_list("StoryInfo")
    for story in stories:
        if story[0] == storyName:
            return True
    return False

#add new story to db
#if a story with that name already exists 
def add_story(storyName, newText, contributor):
    if not(story_exists):
        c.execute("INSERT INTO StoryInfo VALUES (?, ?, ?, ?)", (storyName, newText, newText, contributor))
    else:
        return -1
#return fullText, lastAdded, and contributors of a story
#return -1 if story is not in db
def get_story_info(storyName):
    storyInfo = get_table_list("StoryInfo")
    for row in storyInfo:
        if row[0] == storyName:
            return row[1:]
    return -1
#edit story
def edit_story(storyName, newText, contributor):
    if story_exists(storyName):
        storyInfo = get_story_info(storyName)
        fullText = storyInfo[0] + newText
        contributors = contributor + "," + storyInfo[2] 
        c.execute(f'''
        UPDATE storyInfo
        SET fullStory = "{fullText}",
        lastAdded = "{newText}",
        Contributors = "{contributors}"
        WHERE
        storyName = "{storyName}"
        ''')
    else:
        return -1

#add_story("beeInfo", "bees are cool", "SamLublsky")
# print(edit_story("beeInfo", ".  I hate bees :(", "Ayman"))
# print(get_table_list("storyInfo"))
#print(verify_account("hello", "world"))
#print(add_account("my", "name"))
#print(get_table_list("UserInfo"))


db.commit()
#db.close()
