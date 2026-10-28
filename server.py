import socket

server = socket.socket()
server.bind(("", 6767))
server.listen()

while True:
    client, address = server.accept()

    request = client.recv(1024).decode()
    print(request)

    body = "hello"
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )
    client.sendall(response.encode())
    client.close()
