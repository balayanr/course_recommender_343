from builtins import input
from db_core import *
from handler import *
from magic_numbers import *

def verify_yn(ans):
    while True:
        if ans == "y" or ans == "n":
            return ans
        else: ans = input("Unrecognised input, please enter 'y' or 'n': ")

# Establish connection
conn = db_init();
cursor = conn.cursor()

username = "madame_id"
user = login(conn, username)
handler = Handler(user, conn)
user.setup_skills_and_interests()

handler.create_table()
handler.get_nearest_courses()
handler.recommend_courses()
