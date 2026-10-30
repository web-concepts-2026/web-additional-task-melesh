import socket
import json
server = socket.socket()
server.bind(("", 7777))
server.listen()

def parse_request(req):
    method, path, proto = "", "", ""
    headers = {}
    lines = req.splitlines() 
    for i in range(len(lines)):
        if i == 0:
            info = lines[i].split()
            method = info[0]
            path = info[1]
            proto = info[2]
            continue

        if ":" in lines[i]:
            key, value = lines[i].split(":", 1)
            headers[key.strip()] = value.strip()
    body = req.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in req else ""
    parsed = {'method': method, 'path': path, 'protocol': proto, 'headers': headers, 'body': body}
    return parsed

while True:
    client, address = server.accept()
    respbody = ""
    request = client.recv(1024).decode()
    info = parse_request(request)
    content_type = ""
    if info['method'] == "GET":
        content_type = "text/plain"
        respbody = "hey"
        code = "200 OK"
    elif info['method'] == "POST":
        data = json.loads(info['body'])
        respbody = json.dumps({"received": data})
        content_type = "application/json"
        code = "200 OK"
    else:
        respbody = "method not allowed"
        code = "405 Method Not Allowed"

    response = (
        f"HTTP/1.1 {code}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(respbody)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{respbody}"
    ).encode()

    client.sendall(response)
    client.close()
