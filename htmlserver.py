# -*- coding: UTF-8 -*-
import SimpleHTTPServer
import SocketServer

PORT = 3333

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()