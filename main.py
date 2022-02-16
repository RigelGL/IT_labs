import mimetypes
import os
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader

root = os.path.dirname(os.path.abspath(__file__))
jinja_env: Environment = Environment(loader=FileSystemLoader(os.path.join(root, 'templates')))

poem = "Нам не дано предугадать,\nКак слово наше отзовется,\nИ нам сочувствие да-ется,\nКак нам дается благодать...\n\nФ. И. Тютчев."


class Student:
    __slots__ = ['name']

    def __init__(self, name):
        self.name = name


student = Student('Сусанин Станислав Ильич')


class HttpGetHandler(BaseHTTPRequestHandler):
    def get_static(self):
        path = self.path[1:]

        mimetype = mimetypes.guess_type(path)[0]
        if not mimetype:
            mimetype = 'text/plain'

        file = None
        try:
            file = open(os.path.join(root, path), 'rb')
            data = file.read()
            self.send_response(200)
            self.send_header("Content-type", mimetype)
            self.end_headers()
            self.wfile.write(data)

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write('Not Found'.encode('utf-8'))
        finally:
            if file:
                file.close()

    def do_POST(self):
        pass

    def do_GET(self):
        path = urlparse(self.path).path
        query = dict()

        for e in urlparse(self.path).query.split("&"):
            splited = e.split('=')
            if len(splited) == 2:
                query[splited[0]] = splited[1]

        if path.startswith('/static/'):
            self.get_static()

        if path.startswith('/laba_1/'):
            template = jinja_env.get_template('index.html')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                template.render(
                    student=student,
                    poem=poem.replace('\n', '<br>'),
                    table={
                        'heads': ['Вид издания', 'Получено', 'Сдано'],
                        'rows': [
                            ['Учебники', 125, 36],
                            ['Монографии', 36, 4],
                            ['Справочники', 5, '-'],
                        ]
                    }
                ).encode('utf-8')
            )
        elif path == '/':
            template = jinja_env.get_template('titul.html')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(template.render().encode('utf-8'))
        else:
            self.send_response(404)


if __name__ == '__main__':
    server_address = ('195.19.54.45', 8080)
    httpd = HTTPServer(server_address, HttpGetHandler)
    httpd.serve_forever()
