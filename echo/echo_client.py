import argparse
import socket


BUFFER_SIZE = 1024
LOCAL_HOST = "127.0.0.1"


class EchoClient():

    def __init__(self, server, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((server, port))

    def send_request(self, request):
        request = request.encode("utf-8")
        self.conn.sendall(request)
        response = self.conn.recv(BUFFER_SIZE)
        response = request.decode("utf-8")
        return response


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port", default=12345, type=int)
    ap.add_argument("-r", "--request", default="Hi!!!", type=str)
    args = vars(ap.parse_args())
    port = args["port"]
    request = args["request"]

    client = EchoClient(LOCAL_HOST, port)

    print("REQUEST: ", request)

    response = client.send_request(request)
    print("RESPONSE: ", response)
