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
def add_row(tableName, row):
    c.execute(f"INSERT INTO {tableName} VALUES({"?," for _ in range(len(row) - 1)})")

get_stories_list()