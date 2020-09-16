from chat import ChatApp


if __name__ == "__main__":
    local_host = "127.0.0.1"
    local_port = 12346

    remote_host = "127.0.0.1"
    remote_port = 12345

    ChatApp(local_host, local_port, remote_host, remote_port)
