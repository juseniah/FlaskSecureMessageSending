import socketserver
import sqlite3 as sql
import hmac
import hashlib

# pip install pycryptodomex
#### from Cryptodome.Cipher import AES
import Encryption


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        def verify(msg, sig):
            secret = b'1234'
            computed_sha = hmac.new(secret, msg, digestmod=hashlib.sha3_512).digest()
            if sig != computed_sha:
                return False
            else:
                return True

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()

        # Pre-processing message
        messageEncrypted = self.data[:len(self.data) - 64]
        message = bytes(Encryption.cipher.decrypt(messageEncrypted), encoding='utf-8')
        tag = self.data[-64:]

        # Print message if authenticated-- if not, print error message
        if verify(message, tag):
            # Use split to get both message and AgentId
            message = message.decode('utf-8')
            msg_arr = message.split('~')
            print(msg_arr[1] + " sent message:\n" + msg_arr[0])

            try:
                # Add message to table
                with sql.connect("sagent.db") as con:
                    cur = con.cursor()
                    cur.execute("Insert or Replace Into Messages (AgentId,Message) Values (?, ?)",
                                (msg_arr[1], msg_arr[0]))
                    con.commit()
            except:
                con.rollback()
            finally:
                con.close()

        else:
            print("unauthenticated message")


if __name__ == '__main__':
    try:
        HOST, PORT = "localhost", 8888
        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        # Activate the server; this	will keep running until you
        # interrupt	the	program	with Ctrl-C
        server.serve_forever()
    except server.error as e:
        print("Error:", e)
        exit(1)
    finally:
        server.close()
