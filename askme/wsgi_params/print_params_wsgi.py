import re

import astroid


def app(environ, start_response):
    """Simplest possible application object"""
    res = [str.encode(environ['REQUEST_METHOD'] + ":\n")]
    for param in environ:
        if re.match(r"^HTTP_\w+$", param):
            res.append(str.encode(param + ": " + environ[param] + "\n"))
    print(res)
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(str(" ".join(i.decode() for i in res)))))
    ]
    start_response(status, response_headers)
    return iter([str.encode((" ".join(i.decode() for i in res)))])
