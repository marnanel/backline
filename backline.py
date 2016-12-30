from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import socket
import cgi

class Backline(object):
	def __init__(self, initial=''):
		self._line = initial
		self._condition = threading.Condition()

	def get(self, blocking=False):

		if blocking:
			self._condition.acquire()
			self._condition.wait()
			self._condition.release()

		return self._line

	def set(self, s):
		self._condition.acquire()
		self._line = s
		self._condition.notify_all()
		self._condition.release()

backline = Backline()

class BacklineHandler(SimpleHTTPRequestHandler):

	def __init__(self, request, client_address, server):
		SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
    
	def _serve_backline(self, blocking=False):

		message = backline.get(blocking)

	        self.send_response(200)
		self.send_header('Content-Type', 'text/plain')
	        self.end_headers()
        	self.wfile.write(message)
	        self.wfile.write('\n')

	def do_GET(self):

		if self.path.startswith('/line'):
			self._serve_backline('blocking' in self.path)
		else:
			SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):

		if self.path.startswith('/line'):

			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			if not form.has_key("line"):
				self.send_error(400, "line not specified")
				self.end_headers()

			backline.set(str(form['line'].value))
			self._serve_backline(False)
			
		else:
			self.send_error(410, "forbidden")
			self.end_headers()

class BacklineServer(ThreadingMixIn, HTTPServer):

	def server_bind(self):
		HTTPServer.server_bind(self)
		# Set SO_REUSEADDR so we can bring the server up again
		# immediately if it crashes.
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if __name__ == '__main__':
	PORT = 8080
	server = BacklineServer(('localhost', PORT), BacklineHandler)
	print 'Serving on', PORT
	server.serve_forever()
