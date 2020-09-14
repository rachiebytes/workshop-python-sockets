import argparse
import socket


BUFFER_SIZE = 1024
LOCAL_HOST = "127.0.0.1"


class EchoServer():

    def __init__(self, host, port):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen()

    def accept(self):
        conn, addr = self.socket.accept()
        return conn, addr
    
    def send_response(self, conn):
        with conn:
            request = conn.recv(BUFFER_SIZE)
            print("REQUEST: ", request.decode("utf-8"))
            conn.sendall(request)
            print("RESPONSE: ", request.decode("utf-8"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port", default=12345, type=int)
    args = vars(ap.parse_args())
    port = args["port"]

    server = EchoServer(LOCAL_HOST, port)

    while True:
        conn, addr = server.accept()
        print("Client address: ", addr) # notice the client's port keeps changing
        server.send_response(conn)
