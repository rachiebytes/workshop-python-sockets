import atexit
import errno
import fileinput
import socket
import threading
import time


class ChatApp(object):
    """ Chat application instance.
    """

    def __init__(self, local_host, local_port, remote_host, remote_port):
        self.local_host = local_host
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port

        threading.Thread(target=self.sender, name="Thread-Sender").start()
        threading.Thread(target=self.receiver, name="Thread-Receiver").start()
    
    def sender(self):

        # establish a connection with the remote chat app
        while True:
            try:
                self.remote_socket = socket.socket()
                self.remote_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.remote_socket.connect((self.remote_host, self.remote_port))
                atexit.register(self._sender_cleanup)
                break
            except socket.error as err:
                if err.errno != errno.ECONNREFUSED:
                    raise err
                print("Could not connect to peer. Trying again in 3 seconds.")
                time.sleep(3)
        print("Connection established with peer.")

        # send a message to the remote chat app
        while True:
            msg = fileinput.input()
            for line in msg:
                self.remote_socket.sendall(line.encode())

    def _sender_cleanup(self):
        self.remote_socket.close()

    def receiver(self):
        self.local_socket = socket.socket()
        self.local_socket.bind((self.local_host, self.local_port))
        atexit.register(self._receiver_cleanup)

        self.local_socket.listen(1)
        client_connection, address = self.local_socket.accept()
        while True:
            data = client_connection.recv(1024)
            if data:
                print(data.decode())

    def _receiver_cleanup(self):
        self.local_socket.close()



