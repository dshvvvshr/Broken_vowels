#!/usr/bin/env python3
"""
Simple HTTP server for Broken Vowels project.
Serves content at http://localhost:8000/
"""

import http.server
import os
import socketserver

PORT = int(os.environ.get("PORT", 8000))

Handler = http.server.SimpleHTTPRequestHandler

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving at http://0.0.0.0:{PORT}/")
    httpd.serve_forever()
