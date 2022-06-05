import socket
import os

HOST = "127.0.0.1"
PORT = 9000


def parseHeaders(bytes): #Pretty rusty parsing
    splitHead = bytes.decode().split("\r\n")
    headers = {}
    for x in splitHead[1:]:
        d = x.split(":",1)
        if len(d) < 2: continue
        headers[d[0].strip()] = d[1].strip()
    method, path, version = splitHead[0].split(" ")
    headers["method"] = method
    headers["path"] = path
    headers["version"] = version
    return headers

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Running on: http://{HOST}:{PORT}")
    while True:
        sock, addr = s.accept()
        
        headers = parseHeaders(sock.recv(1024))
        status = "200 OK"
        contType = "text/html"
        resp = ""

        if headers["path"] == "/":
            resp = "<head><link rel='stylesheet' href='/static/app.css' /></head> Welcome home <script src='/static/app.js'></script>"
        elif headers["path"] == "/about":
            resp = "About page"
        elif headers["path"].startswith("/static"):
            filePath = f".{headers['path']}"
            if os.path.exists(filePath):
                ext = headers["path"].split(".")[-1]
                contType = f"text/{ext}"

                if ext == "json":
                    contType = "application/json"

                with open(filePath,"r") as f:
                    resp = f.read()
        else:
            status = "404 Not-Found"
            resp = "Not found"

        sock.send(f"""HTTP/1.1 {status}
Content-Type: {contType}; charset=utf-8
Content-Length: {len(resp)}
Connection: close
Server: A-fandino Custom Server
Set-Cookie: YourSecretLove=http://github.com/A-fandino/

{resp}""".encode());
        sock.close()
