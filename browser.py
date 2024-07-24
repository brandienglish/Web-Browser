#### comand line for ex. python3 browser.py https://browser.engineering/examples/xiyouji.html 


import socket
import sys
import tkinter
import ssl
import certifi

class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]

        self.port = 80 if self.scheme == "http" else 443

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
        s.connect((self.host, self.port))

        if self.scheme == "https":
            ctx = ssl.create_default_context(cafile=certifi.where())
            s = ctx.wrap_socket(s, server_hostname=self.host)

        request = f"GET {self.path} HTTP/1.0\r\n"
        request += f"Host: {self.host}\r\n"
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

def lex(body):
    text = ""
    in_tag = False
    for c in body:
        if c == '<':
            in_tag = True
        elif c == '>':
            in_tag = False
        elif not in_tag:
            text += c
    return text

def loadAndLex(url):
    url_obj = URL(url)
    body = url_obj.request()
    return lex(body)

def layout(text):
    HSTEP, VSTEP = 13, 18
    display_list= []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        if c == "\n":
            cursor_y += VSTEP
            cursor_x = HSTEP
        else:
            display_list.append((cursor_x, cursor_y, c))
            cursor_x += HSTEP
            if cursor_x >= Browser.WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP
    return display_list

           

class Browser:
    WIDTH, HEIGHT = 800, 600
    SCROLL_STEP = 100

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
       


    def scrolldown(self, e): 
        self.scroll += self.SCROLL_STEP
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            self.canvas.create_text(x, y - self.scroll,text=c)

    def load(self, url):
            text = loadAndLex(url)
            self.display_list = layout(text)
            self.draw()

        

if __name__ == "__main__":
        if len(sys.argv) != 2:
            print("Usage: python3 browser.py <url>")
            sys.exit(1)

        browser = Browser()
        browser.load(sys.argv[1])
        tkinter.mainloop()
