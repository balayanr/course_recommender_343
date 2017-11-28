import sqlite3
from User import *

def db_init():
    conn = sqlite3.connect('A3.db')
    return conn

def login(conn, username):
    cursor = conn.cursor()
    res = cursor.execute('select * from students where username = ?', (username,) )
    tup = res.fetchone()
    if tup:
        user = User(tup, conn)
        print("Login successful!")
    else:
        print("User not found, creating a new user.")
        try:
            cursor.execute('insert into students values (?, NULL, NULL, NULL, NULL)', (username, ))
            user = User((username, None, None, None, None), conn)
            print("User created, all ready to go")
        except:
            print("Something went wrong when creating a new user!")
            user = None
    print("Welcome, %s!" % username)
    return user
