from re import T
import sqlite3

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE)
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
def add_account(username, password):
    c.execute("INSERT INTO UserInfo (username, password) VALUES (?, ?);", (username, password))
def add_story(storyName, newText, contributor):
    c.execute("INSERT INTO StoryInfo VALUES (?, ?, ?, ?)", (storyName, newText, newText, contributor))
def get_story_info(storyName):
    storyInfo = get_table_list()
    targetStory = storyInfo[storyInfo.find(storyName)]
    return targetStory[1:]
def edit_story(storyName, newText, contributor):
    storyInfo = get_story_info(storyName)
    fullText = storyInfo[0] + newText
    contributors = contributor + "," + storyInfo[2] 
    c.execute(f'''
    UPDATE storyInfo
    SET fullStory = {fullText},
    lastAdded = {newText},
    Contributors = {contributors}
    WHERE
    storyName = {storyName}
    ''')

#add_story("beeInfo", "bees are cool", "SamLublsky")
#edit_story("beeInfo")
#print(get_table_list("storyInfo"))

db.commit()
db.close()
