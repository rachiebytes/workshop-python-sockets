import argparse
import socket

from collections import defaultdict


BUFFER_SIZE = 1024
LOCAL_HOST = "127.0.0.1"
PATHS = defaultdict(
    lambda: "NOT FOUND",
    {
        "/fruits": "apples, mangos, cherries",
        "/nuts": "almonds, peanuts, pistachios",
        "/veggies": "carrots, squash, broccoli",
        "/tacos": "pueblo viejo > torchys",
        # TODO: add another request type and response
    }
)


class ApiServer():

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
            request = request.decode("utf-8")
            print("REQUEST: ", request)
            response = PATHS[request].encode("utf-8")
            conn.sendall(response)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port", default=22345, type=int)
    args = vars(ap.parse_args())
    port = args["port"]

    server = ApiServer(LOCAL_HOST, port)

    while True:
        conn, addr = server.accept()
        server.send_response(conn)