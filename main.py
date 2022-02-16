from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


class HttpGetHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('hello'.encode('utf-8'))


if __name__ == '__main__':
    server_address = ('195.19.54.45', 8080)
    httpd = HTTPServer(server_address, HttpGetHandler)
    httpd.serve_forever()
