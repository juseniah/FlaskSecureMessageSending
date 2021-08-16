import socketserver
import Encryption
import sqlite3 as sql


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()

        # Using split to get message and AgentId
        msg = str(Encryption.cipher.decrypt(self.data))
        msg_arr = msg.split('~')
        print(msg_arr[1] + " sent message:\n" + msg_arr[0])

        try:
            # Add message to table
            with sql.connect("sagent.db") as con:
                cur = con.cursor()
                cur.execute("Insert or Replace Into Messages (AgentId,Message) Values (?, ?)", (msg_arr[1], msg_arr[0]))
                con.commit()
        except:
            con.rollback()
        finally:
            con.close()


if __name__ == '__main__':
    try:
        HOST, PORT = "localhost", 9999
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
