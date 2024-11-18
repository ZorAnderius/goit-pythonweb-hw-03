from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import mimetypes

class MyHttpServer (BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlparse(self.path).path
        match route:
            case "/":
                self.send_HTML("index.html")
            case "/message":
                self.send_HTML("message.html")
            case _:
                self.send_HTML("error.html", 404)
    def do_POST(self):
        pass

    def send_HTML(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', mimetypes.guess_type(self.path)[0])
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

def run(server_class=HTTPServer, handler_class=MyHttpServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)  #noqa
    httpd.serve_forever()

if __name__ == '__main__':
    run()