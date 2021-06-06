"""
WSGI config for askme project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askme.settings')

application = get_wsgi_application()

# def app(environ, start_response):
#     """Simplest possible application object"""
#     data = b'Hello, World!\n'
#     status = '200 OK'
#     response_headers = [
#         ('Content-type', 'text/plain'),
#         ('Content-Length', str(len(data)))
#     ]
#     start_response(status, response_headers)
#     return iter([data])
#
