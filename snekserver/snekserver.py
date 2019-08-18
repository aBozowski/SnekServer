from config import CONFIG
from snekrouter import SnekRouter
import time, threading, socket
from http.server import HTTPServer
from validate_config import validate

validate()

sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
addr = (CONFIG['HOST'],CONFIG['PORT'])
number_threads = CONFIG['NUMBER_THREADS']
sock.bind(addr)
sock.listen(number_threads)

class Thread(threading.Thread):

	def __init__(self, i):

		threading.Thread.__init__(self)
		self.i, self.daemon = i, True
		self.start()

	def run(self):

		httpd = HTTPServer(addr, SnekRouter, False)
		httpd.socket = sock
		httpd.server_bind = self.server_close = lambda self: None
		httpd.serve_forever()

def main():

	threads = list(Thread(i) for i in range(number_threads))
	for thread in threads: thread.join()

if __name__ == '__main__':

	main()
