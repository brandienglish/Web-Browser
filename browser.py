import socket
import sys
import tkinter

#####downloading webpages
class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme == "http"

        if "/" not in url:
            self.host = url
            self.path = "/"
        else:
            self.host, self.path = url.split("/", 1)
            self.path = "/" + self.path

    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, 80))

        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"

        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n")

        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        s.close()

        return content

def show(body):
    in_tag = False
    for c in body:
        if c == '<':
            in_tag = True
        elif c == '>':
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    url_obj = URL(url)
    body = url_obj.request()
    show(body)

if __name__ == "__main__":
    load(sys.argv[1])

#run python3 browser.py http://example.org/ to display

#####downloading webpages
    
##Drawing to Screen ###
    


import tkinter

class Browser:
    WIDTH, HEIGHT = 800, 600

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()

    def load(self, url):
        # test to show graphics
        self.canvas.create_rectangle(10, 20, 400, 300, outline="blue", fill="white")
        self.canvas.create_oval(100, 100, 150, 150, outline="red", fill="yellow")
        self.canvas.create_text(200, 150, text="Hello World!", fill="black")

if __name__ == "__main__":
    import sys
    browser = Browser()
    if len(sys.argv) > 1:
        url = sys.argv[1]
        browser.load(url)
    tkinter.mainloop()

 #run python3 browser.py http://example.org/ to display