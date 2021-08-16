from flask import Flask, render_template, request, session, flash, jsonify
import sqlite3 as sql
import os
import string
import base64
import Encryption
import pandas as pd
import socket
import hmac, hashlib


app = Flask(__name__)


# Home page of website
@app.route('/')
def home():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      return render_template('home.html', name=session['user'])


# Page to add new record to database
@app.route('/enternew')
def new_agent():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif not session.get('can_add'):
      flash('Query result: page not found')
      return render_template('agent.html')
   else:
      return render_template('agent.html')


# Page to send boss a message
@app.route('/sendMessage')
def sendmsg():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      return render_template('sendMsgToBoss.html', name=session['user'])


# If sending message
@app.route('/sendMessage', methods=['POST'])
def send_boss_message():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      if request.method == 'POST':
         try:
            msg = request.form['message']

            if not msg or msg.isspace():
               msg = "You can not enter in an empty message"
            else:
               # Appending AgentId to message with delimiter
               id_num = session['id_num']
               msg += " ~"
               msg += str(id_num)
               msg = str(Encryption.cipher.encrypt(bytes(msg, 'utf-8')).decode("utf-8"))
               HOST, PORT = "localhost", 9999
               sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               # Connect to server and send data
               sock.connect((HOST, PORT))
               sock.sendall(bytes(msg, "utf-8"))
               sock.close()
               msg = "Message successfully sent to boss"

         except sock.error as e:
            msg = "Error - Message NOT sent to boss", e
         finally:
            return render_template("result.html", msg=msg)


# Page to send boss an HMAC encrypted message
@app.route('/sendMessageHMAC')
def sendmsgHMAC():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      return render_template('sendMsgToBossHMAC.html', name=session['user'])


# If sending message
@app.route('/sendMessageHMAC', methods=['POST'])
def send_boss_messageHMAC():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      if request.method == 'POST':
         try:
            msg = request.form['message']

            if not msg or msg.isspace():
               msg = "You can not enter in an empty message"
            else:
               # Appending AgentId to message with delimiter
               id_num = session['id_num']
               msg += " ~"
               msg += str(id_num)
               print("Original message with no tag:\n" + msg)
               msg = bytes(msg, 'utf-8')

               # Encrypting message
               msgEncrypted = Encryption.cipher.encrypt(msg)
               print("Encrypted message:\n", msgEncrypted)

               # Implementing HMAC and sha3_512 authentication
               secret = b'1234'
               computedSig = hmac.new(secret, msg, digestmod=hashlib.sha3_512).digest()
               print("tag of message=", computedSig)
               print("length of tag of message=", len(computedSig))
               messageToSend = msgEncrypted + computedSig

               # Connect to server and send data
               HOST, PORT = "localhost", 8888
               sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               sock.connect((HOST, PORT))
               sock.sendall(messageToSend)
               sock.close()
               msg = "Message successfully sent to boss"

         except sock.error as e:
            msg = "Error - Message NOT sent to boss", e
         finally:
            return render_template("result.html", msg=msg)


# Function to add record to SecretAgent database
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif not session.get('can_add'):
      flash('Query result: page not found')
      return render_template('agent.html')
   else:
      msg = ""  # If msg is still "" after input validation, it means all inputs are valid
      if request.method == 'POST':
         try:
            nm = request.form['AgentName']
            ag = request.form['AgentAlias']
            amt = request.form['AgentSecurityLevel']
            pwd = request.form['LoginPassword']

            # Input validation
            if not nm or nm.isspace():
               msg += "You cannot enter an empty name\n"
            if not ag or ag.isspace():
               msg += "You cannot enter an empty alias\n"
            if not pwd or pwd.isspace():
               msg += "You cannot enter an empty pwd\n"
            if not amt.isnumeric():
               msg += "The security level must be a numeric value between 1 and 10\n"
            else:
               temp = int(amt)
               print("amt value is: ", temp)
               if temp < 0 or temp > 10:
                  msg += "The security level must be a numeric value between 1 and 10\n"

            # Encrypting data
            temp = str(Encryption.cipher.encrypt(bytes(nm, 'utf-8')).decode("utf-8"))
            nm = str(Encryption.cipher.encrypt(bytes(nm, 'utf-8')).decode("utf-8"))
            ag = str(Encryption.cipher.encrypt(bytes(ag, 'utf-8')).decode("utf-8"))
            pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))

            # If msg is empty, go ahead and add the record
            if msg == "":
               with sql.connect("sagent.db") as conn:
                  cur = conn.cursor()

                  # SQL code to add entry to database
                  cur.execute(
                     "Insert or Replace Into SecretAgent (AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) Values (?, ?, ?, ?)",
                     (nm, ag, amt, pwd))

                  conn.commit()
                  msg = "Record successfully added"

         # if adding record fails, rollback and print error
         except:
            conn.rollback()
            msg = "error in insert operation"

         finally:
            print(msg)
            return render_template("result.html", msg=msg)
            conn.close()


# Function to print contents of database
@app.route('/list')
def list():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif not session.get('can_list'):
      flash('Query result: page not found')
      return render_template('list.html')
   else:
      conn = sql.connect("sagent.db")
      conn.row_factory = sql.Row

      cur = conn.cursor()
      cur.execute("SELECT AgentName,AgentAlias,AgentSecurityLevel,LoginPassword FROM SecretAgent")
      df = pd.DataFrame(cur.fetchall(), columns=['AgentName', 'AgentAlias', 'AgentSecurityLevel', 'LoginPassword']);

      # convert to an array
      # decrypting name, alias, pw for the list function
      index = 0
      for nm in df['AgentName']:
         nm = str(Encryption.cipher.decrypt(nm))
         df._set_value(index, 'AgentName', nm)
         index += 1
      index = 0
      for alias in df['AgentAlias']:
         alias = str(Encryption.cipher.decrypt(alias))
         df._set_value(index, 'AgentAlias', alias)
         index += 1
      index = 0
      for pw in df['LoginPassword']:
         pw = str(Encryption.cipher.decrypt(pw))
         df._set_value(index, 'LoginPassword', pw)
         index += 1
      conn.close()

      return render_template("list.html", rows=df)


@app.route('/login', methods=['POST'])
def do_admin_login():
   try:
     name = request.form['username']
     nm = str(Encryption.cipher.encrypt(bytes(name, 'utf-8')).decode("utf-8"))
     pwd = request.form['password']
     pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))

     with sql.connect("sagent.db") as conn:
        conn.row_factory = sql.Row
        cur = conn.cursor()

        sql_select_query = """select * from SecretAgent where AgentName = ? and LoginPassword = ?"""
        cur.execute(sql_select_query, (nm, pwd))

        row = cur.fetchone()
        if row != None:
           session['user'] = name
           session['logged_in'] = True

           # get security level
           session['sec_level'] = sec_level = row[3]
           session['id_num'] = row[0]

           # setting permissions to add a record
           if sec_level == 1:
              session['can_add'] = True
           else:
              session['can_add'] = False

           # setting permissions to list records
           if sec_level < 3:
              session['can_list'] = True
           else:
              session['can_list'] = False

        else:
           session['logged_in'] = False
           flash('invalid username and/or password!')
   except:
      conn.rollback()
      flash("error in insert operation")
   finally:
      conn.close()
   return home()


@app.route("/logout")
def logout():
   session['user'] = ""
   session['logged_in'] = False
   session['sec_level'] = None
   session['can_list'] = False
   session['can_add'] = False
   return home()


# Main function
if __name__ == '__main__':
   app.secret_key = os.urandom(12)
   app.run(debug=True)
