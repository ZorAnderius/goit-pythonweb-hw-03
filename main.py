import mimetypes
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote_plus
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
jinja = Environment(loader=FileSystemLoader(str(BASE_DIR.joinpath("templates"))))

class MyHttpServer (BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlparse(self.path).path
        match route:
            case "/":
                self.send_HTML("index.html")
            case "/message":
                self.send_HTML("message.html")
            case "/messages":
                self.render_template("messages.jinja")
            case _:
                file = BASE_DIR.joinpath(route[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_HTML("error.html", 404)

    def do_POST(self):
        size = int(self.headers['Content-Length'])
        body = self.rfile.read(size).decode()
        print(body)
        print(unquote_plus(body))
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def render_template(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open("storage/data.json", 'r', encoding='utf-8') as f:
            content = json.load(f)
        template = jinja.get_template(filename)
        html = template.render(messages=content)
        self.wfile.write(html.encode())

    def send_HTML(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

    def send_static(self, filename, status=200):
        self.send_response(status)
        mimetype = mimetypes.guess_type(self.path)[0] or 'text/plain'
        self.send_header('Content-type', mimetype)
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

def run(server_class=HTTPServer, handler_class=MyHttpServer, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)  #noqa
    httpd.serve_forever()

if __name__ == '__main__':
    run()