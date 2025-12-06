#!/usr/bin/env python3
"""
Simple HTTP server for Broken Vowels project.
Serves content at http://localhost:8000/
"""

import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}/")
    httpd.serve_forever()
