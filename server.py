import socket

server = socket.socket()
server.bind(("", 6767))
server.listen()

method, path, proto, body = "", "", "", ""
headers = {}

def parse_request(req):
    lines = req.splitlines() 
    for i in range(len(lines)):
        if i == 0:
            info = lines[i].split()
            method = info[0]
            path = info[1]
            proto = info[2]
            continue
        if lines[i-1] == "" and lines[i] == "" and lines[i+1] != "":
            for j in range(i+1, len(lines)):
                body += lines[j]
            break

        if ":" in lines[i]:
            key, value = lines[i].split(":", 1)
            headers[key.strip()] = value.strip()

    parsed = {'method': method, 'path': path, 'protocol': proto, 'headers': headers, 'body': body}
    return parsed

while True:
    client, address = server.accept()

    request = client.recv(1024).decode()
    print(request)
    info = parse_request(request)
    if info['method'] == "GET":
        respbody = "hello"
        code = "200 OK"
    else:
        respbody = "method not allowed"
        code = "405 Method Not Allowed"

    response = (
        f"HTTP/1.1 {code}\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(respbody)}\r\n"
        "\r\n"
        f"{respbody}"
    )
    client.sendall(response.encode())
    client.close()
