import socket

server = socket.socket()
server.bind(("", 6767))
server.listen()

def parse_request(req):
    fline = req.splitlines()[0]
    info = fline.split()
    method = info[0]
    path = info[1]
    proto = info[2]
    parsed = {'method': method, 'path': path, 'protocol': proto}
    return parsed

while True:
    client, address = server.accept()

    request = client.recv(1024).decode()
    info = parse_request(request)
    if info['method'] == "GET":
        body = "hello"
        code = "200 OK"
    else:
        body = "method not allowed"
        code = "405 Method Not Allowed"

    response = (
        f"HTTP/1.1 {code}\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )
    client.sendall(response.encode())
    client.close()
