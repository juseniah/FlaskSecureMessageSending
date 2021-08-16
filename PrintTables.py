# Simple program to print database

import sqlite3

def printDB():
    # create connection to db and cursor
    conn = sqlite3.connect('sagent.db')
    # create Cursor to execute queries
    cur = conn.cursor()

    # printing SecretAgent table
    print("SecretAgent table:")
    for row in cur.execute('SELECT * FROM SecretAgent;'):
        print(row)

    # printing Messages table
    print("Messages table:")
    for row in cur.execute('SELECT * FROM Messages;'):
        print(row)

    # close database connection
    conn.close()
    print('Connection closed.')

printDB()