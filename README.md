# FlaskSecureMessageSending

A flask website in Python for secure message sending using encryption and HMAC authentication
* Utilizes a sqlite3 database for user information and message storage
* The menu allows the user to add a secret agent, list the secret agents, or send a secure message to the boss
* LocateMessagesAboutX.py counts how many messages have been received that contain the string X. At present, the program will count messages that contain ‘dog’ and ‘cat’.

## Run these scripts in this order:
* DBSetUp.py
* BossServer.py
* BossServerHMAC.py
* LocateMessagesAboutX.py
* newAgent.py

Then load http://127.0.0.1:5000 in your browser.

### Login credentials
* Username: James Bond
* Password: password
