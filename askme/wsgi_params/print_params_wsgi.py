import re

import astroid
from urllib.parse import parse_qs

#@todo тело POST в вывод
def app(environ, start_response):
    """Simplest possible application object"""
    print(environ)
    res = [str.encode(environ['REQUEST_METHOD'] + ":\n")]

    for param in environ:
        if re.match(r"^HTTP_\w+$", param) or re.match(r"^QUERY_\w+$", param):
            res.append(str.encode(param + ": " + environ[param] + "\n"))
    body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))
    print(body.decode())
    res.append(body)
    # print(res)
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(str(" ".join(i.decode() for i in res)))))
    ]
    start_response(status, response_headers)
    return iter([str.encode((" ".join(i.decode() for i in res)))])
