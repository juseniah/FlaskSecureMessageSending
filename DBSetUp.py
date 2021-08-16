"""
Name: Jussi Doherty
Date: March 12, 2021
Assignment: Module 10 - Using Processes
Due Date: March 14, 2021
About this project: Notify if any new messages about X are sent
Assumptions: N/A
All work below was performed by Jussi Doherty
"""

# pip install sqlcipher3
import sqlite3
import Encryption
from PrintTables import printDB


# create connection to db and cursor
conn = sqlite3.connect('sagent.db')
# create Cursor to execute queries
cur = conn.cursor()


# Messages table
# drop Messages table
try:
    conn.execute('''Drop table Messages''')
    # save changes
    conn.commit()
    print('Messages table dropped.')
except:
    print('Messages table did not exist')


# create table in database
cur.execute('''CREATE TABLE IF NOT EXISTS Messages(
MessageId INTEGER PRIMARY KEY NOT NULL,
AgentId INTEGER NOT NULL,
Message TEXT NOT NULL);
''')

# save changes
conn.commit()
print('Messages table created.')

# adding rows to Messages table
# Message 1
agent = 1
msg = "Your mission, should you choose/decide to accept it..."
cur.execute("Insert or Replace Into Messages (AgentId,Message) Values (?, ?)", (agent, msg))
conn.commit()

# Message 2
agent = 2
msg = "Need emergency extraction"
cur.execute("Insert or Replace Into Messages (AgentId,Message) Values (?, ?)", (agent, msg))
conn.commit()

# Message 3
agent = 3
msg = "Will rendezvous with 007 in Budapest"
cur.execute("Insert or Replace Into Messages (AgentId,Message) Values (?, ?)", (agent, msg))
conn.commit()

# Message 4
agent = 4
msg = "I would like a burger, a coke, and small fries"
cur.execute("Insert or Replace Into Messages (AgentId,Message) Values (?, ?)", (agent, msg))
conn.commit()

# Message 5
agent = 5
msg = "Something strange is afoot at the Circle K"
cur.execute("Insert or Replace Into Messages (AgentId,Message) Values (?, ?)", (agent, msg))
conn.commit()

# Message 6
agent = 6
msg = "Be excellent to each other"
cur.execute("Insert or Replace Into Messages (AgentId,Message) Values (?, ?)", (agent, msg))
conn.commit()


# SecretAgent table
# drop SecretAgent table
try:
    conn.execute('''Drop table SecretAgent''')
    # save changes
    conn.commit()
    print('SecretAgent table dropped.')
except:
    print('SecretAgent table did not exist')


# create table in database
cur.execute('''CREATE TABLE IF NOT EXISTS SecretAgent(
AgentId INTEGER PRIMARY KEY NOT NULL,
AgentName TEXT NOT NULL,
AgentAlias TEXT NOT NULL,
AgentSecurityLevel INTEGER NOT NULL,
LoginPassword TEXT NOT NULL);
''')

# save changes
conn.commit()
print('SecretAgent table created.')

# Adding rows to SecretAgent table
# James Bond
nm = str(Encryption.cipher.encrypt(b'James Bond').decode("utf-8"))
alias = str(Encryption.cipher.encrypt(b'007').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'password').decode("utf-8"))
cur.execute("Insert or Replace Into SecretAgent (AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) Values (?, ?, ?, ?)", (nm, alias, 1, pwd))
conn.commit()

# David Webb
nm = str(Encryption.cipher.encrypt(b'David Webb').decode("utf-8"))
alias = str(Encryption.cipher.encrypt(b'Jason Bourne').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'password').decode("utf-8"))
cur.execute("Insert or Replace Into SecretAgent (AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) Values (?, ?, ?, ?)", (nm, alias, 2, pwd))
conn.commit()

# Kim Possible
nm = str(Encryption.cipher.encrypt(b'Kim Possible').decode("utf-8"))
alias = str(Encryption.cipher.encrypt(b'Kimmie').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'asdf').decode("utf-8"))
cur.execute("Insert or Replace Into SecretAgent (AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) Values (?, ?, ?, ?)", (nm, alias, 2, pwd))
conn.commit()

# Jack Bauer
nm = str(Encryption.cipher.encrypt(b'Jack Bauer').decode("utf-8"))
alias = str(Encryption.cipher.encrypt(b'Jack Roush').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'qweoriuqasldkfh').decode("utf-8"))
cur.execute("Insert or Replace Into SecretAgent (AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) Values (?, ?, ?, ?)", (nm, alias, 2, pwd))
conn.commit()

# Jack Bauer
nm = str(Encryption.cipher.encrypt(b'Johnny B Goode').decode("utf-8"))
alias = str(Encryption.cipher.encrypt(b'Johnny').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'askdjf1923847').decode("utf-8"))
cur.execute("Insert or Replace Into SecretAgent (AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) Values (?, ?, ?, ?)", (nm, alias, 2, pwd))
conn.commit()

# Duke of York
nm = str(Encryption.cipher.encrypt(b'Duke of York').decode("utf-8"))
alias = str(Encryption.cipher.encrypt(b'Dukey').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'llkopqwerh').decode("utf-8"))
cur.execute("Insert or Replace Into SecretAgent (AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) Values (?, ?, ?, ?)", (nm, alias, 3, pwd))
conn.commit()

# close database connection
conn.close()
print('Connection closed.')

# printing both tables
printDB()
