import mimetypes
import os
import random
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader

root = os.path.dirname(os.path.abspath(__file__))
jinja_env: Environment = Environment(loader=FileSystemLoader(os.path.join(root, 'templates')))

jinja_env.globals.update({
    'randint': random.randint,
    'len': len,
    'sum': sum
})


class Discipline:
    __slots__ = ['name', 'lectures', 'seminars', 'labs']

    def __init__(self, name, lectures=0, seminars=0, labs=0):
        self.name = name
        self.lectures = lectures
        self.seminars = seminars
        self.labs = labs


class Lesson:
    __slots__ = ['discipline', 'type', 'number']

    def __init__(self, discipline, type, number):
        self.discipline = discipline
        self.type = type
        self.number = number


disciplines = [
    Discipline('Бизнес моделирование', 17, 17),
    Discipline('Государственное регулирование предпринимательской деятельности', 17, 17),
    Discipline('Иностранный язык', seminars=34),
    Discipline('Информационные технологии', labs=34),
    Discipline('Менеджмент', 34, 34),
]

daily = [
    Lesson(disciplines[3], 2, 3),
    Lesson(disciplines[3], 2, 4),
    Lesson(disciplines[0], 1, 5),
    Lesson(disciplines[0], 0, 6)
]

pictures = [
    '/static/pictures/pic1.jpg',
    '/static/pictures/pic2.jfif',
    '/static/pictures/pic3.jpg',

    '/static/pictures/pic4.jfif',
    '/static/pictures/pic5.jfif',
    '/static/pictures/pic6.avif',

    '/static/pictures/pic7.png',
    '/static/pictures/pic8.jfif',
    '/static/pictures/pic9.jfif',
]

pictures = [pictures[i:i + 3] for i in range(0, len(pictures), 3)]


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

        if path.startswith('/laba_4/'):
            template = jinja_env.get_template('index.html')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                template.render(
                    disciplines=disciplines,
                    disciplines_total=[
                        sum([d.lectures for d in disciplines]),
                        sum([d.seminars for d in disciplines]),
                        sum([d.labs for d in disciplines])
                    ],
                    daily=daily,
                    pictures=pictures
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
