import socket
import sys
from datetime import datetime


class HTTPRequest(object):
    def __init__(self, raw_request, client_address):
        self.method = None
        self.uri = None
        self.headers = dict()
        self.http_version = '1.1'
        self.parse(raw_request)
        self.client_host = client_address[0]
        self.client_port = client_address[1]

    def parse(self, raw_request):
        lines = raw_request.split('\r\n')

        self.request_line = lines[0]
        self.parse_request_line()

    def parse_request_line(self):
        words = self.request_line.split()
        if len(words) == 3:
            self.method, self.uri, self.http_version = words


class TCPServer:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.host = host
        self.port = port

    def start(self):
        print(f"Serve via address: {self.host}:{self.port}")
        self.socket.listen(1)
        while True:
            connection, addr = self.socket.accept()
            data = connection.recv(1024)

            response = self.handle_request(data.decode('utf-8'), addr)

            connection.sendall(response)
            connection.close()

    def handle_request(self, data, address):
        return data

    def stop(self):
        self.socket.close()


class HttpLogger(object):
    """
    127.0.0.1 - - [10/Jul/2020 04:04:32] "GET / HTTP/1.1" 200 -
    """
    FORMAT = '{address} [{time}] "{request_line}" {response_code}'
    DATETIME_FMT = "%Y-%m-%d %H:%M:%S"

    def info(self, request, response_code=''):
        message = self.FORMAT.format(**{
            'address': str(request.client_host),
            'time': str(datetime.now().strftime(self.DATETIME_FMT)),
            'request_line': request.request_line,
            'response_code': response_code,
        })
        print(message)


class HTTPServer(TCPServer):
    DEFAULT_HEADERS = {
        'Server': 'Simple HTTP echo server',
        'Content-Type': 'text/plain',
    }
    ECHO_FMT = 'Hi! You request to see path [%s] with method [%s]'

    def __init__(self, host, port, *args, **kwargs):
        super(HTTPServer, self).__init__(host, port)
        self.__logger = HttpLogger()

    def get_response_line(self, code):
        return f"HTTP/1.1 {code}\r\n"

    def get_response_headers(self, extra=None):
        header_dict = self.DEFAULT_HEADERS.copy()

        if extra:
            header_dict.update(extra)

        headers = ""
        for name in header_dict:
            value = header_dict[name]
            headers += "%s: %s\r\n" % (name, value)

        return headers

    @staticmethod
    def get_response(line, headers, body):
        return f"{line}{headers}\r\n{body}"

    def log_request(self, request, response_code):
        self.__logger.info(request, response_code)

    def handle_request(self, request, address):
        http_request = HTTPRequest(request, address)

        try:
            handler = getattr(self, f'handle_{http_request.method}')
        except AttributeError:
            handler = self.HTTP_501_HANDLER

        response, response_code = handler(http_request)
        self.log_request(http_request, response_code)
        return bytes(response, 'utf-8')

    def HTTP_501_HANDLER(self, request):
        code = 501
        response_line = self.get_response_line(code)
        response_headers = self.get_response_headers()
        message = "Not implemented"
        response = self.get_response(response_line, response_headers, message)

        return response, code

    def handle_GET(self, request):
        code = 200
        response_line = self.get_response_line(code)
        response_headers = self.get_response_headers()
        message = self.ECHO_FMT % (request.uri, request.method)
        response = self.get_response(response_line, response_headers, message)

        return response, code

    handle_POST = handle_GET


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 2:
        print("Usage: python server.py <host> <port>")
        sys.exit(1)

    host, port = args
    port = int(port)

    server = HTTPServer(host, port)

    try:
        server.start()
    except KeyboardInterrupt:
        print("Received exit signal from keyboard . . .")
        server.stop()
        sys.exit(0)
