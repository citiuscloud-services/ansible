from __future__ import annotations

import http.server
import socketserver
import sys

if __name__ == '__main__':
    PORT = int(sys.argv[1])

    # This HTTP server is intended for local/testing use only.
    # It does not handle sensitive data, so HTTPS is not required here.
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)  # NOSONAR
    httpd.serve_forever()
