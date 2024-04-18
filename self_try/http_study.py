"""
@Time : 2024/1/13 18:39
@Author : rainmon
@File : http_study.py.py
@Project : StudyNotes-Python
@feature : programming with HTTP for the Internet
@description：from 'Python Network Programming Cookbook (Second Edition)'--预备部分，用的库比较老
"""

import argparse

import io
import gzip
import urllib
import http.cookiejar
import http.client
from http.server import HTTPServer, BaseHTTPRequestHandler

REMOTE_SERVER_HOST = 'http://www.cnn.com'
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8800
HTML_CONTENT = b"<html><body><h1>Compress Hello World!</h1></body></html>"


class HTTPClient:

    def __init__(self, host):
        self.host = host

    def fetch(self):
        response = urllib.request.urlopen(self.host)
        data = response.read()
        text = data.decode('utf8')
        return text


def simple_parse():
    parser = argparse.ArgumentParser(description='HTTP Client Example')
    parser.add_argument('--host', action='store', dest='host', default=REMOTE_SERVER_HOST)

    given_args = parser.parse_args()
    host = given_args.host
    client = HTTPClient(host)
    print(client.fetch())


class RequestHandler(BaseHTTPRequestHandler):
    """custom request handler"""

    def do_GET(self):
        """handler for the GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Encoding', 'gzip')
        zbuf = self.compress_buffer(HTML_CONTENT)
        self.send_header('Content-Length', len(zbuf))
        # zbuf = HTML_CONTENT
        self.end_headers()
        # send the message to the browser
        self.wfile.write(zbuf)
        print(len(HTML_CONTENT))
        print(len(zbuf))

    def compress_buffer(self, buf):
        zbuf = io.BytesIO()
        zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=6)
        zfile.write(buf)
        zfile.close()
        return zbuf.getvalue()


class CustomHTTPServer(HTTPServer):
    """a custom HTTP server"""
    def __init__(self, host, port):
        server_address = (host, port)
        HTTPServer.__init__(self, server_address, RequestHandler)


def run_server(port):
    try:
        server = CustomHTTPServer(DEFAULT_HOST, port)
        print(f"custome HTTP server started on port: {port}")
        server.serve_forever()
    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("server interrupted and is shutting down...")
        server.socket.close()


def custom_http():
    parser = argparse.ArgumentParser(description='Simple HTTP Server Example')
    parser.add_argument('--port', action='store', dest='port', type=int, default=DEFAULT_PORT)
    given_args = parser.parse_args()
    port = given_args.port
    run_server(port)


def extract_cookie_info():
    """
    login for example
    BTW, https://github.com/login 是GET
    """
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    resp = opener.open('https://github.com/login')
    for cookie in cj:
        print(f'--first time cookie>> {cookie.name}: {cookie.value}')
    print(f'Headers: {resp.headers}')
    resp = opener.open('https://github.com')
    for cookie in cj:
        print(f'--second time cookie>> {cookie.name}: {cookie.value}')
    print(f'Headers: {resp.headers}')


def get_server_status_code(url):
    """download just the header of a URL and return the server's status code"""
    host, path = urllib.parse.urlparse(url)[1:3]    # ParseResult(scheme, netloc, path, params, query, fragment)
    try:
        conn = http.client.HTTPConnection(host)
        conn.request('HEAD', path)
        return f"OK>> {conn.getresponse().status}"
    except Exception as e:
        return f"Fail>> server: {url} status is: {e}"


if __name__ == '__main__':
    # print(get_server_status_code('http://www.baidu.com'))
    custom_http()
