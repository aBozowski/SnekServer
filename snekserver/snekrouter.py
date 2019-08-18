import os 
from http.server import BaseHTTPRequestHandler
import json
from traceback import print_exc

from config import CONFIG
mime_types = CONFIG['MIME_TYPES']
encoding = CONFIG['ENCODING']

class SnekRouter(BaseHTTPRequestHandler):

	def do_GET(self): self.ROUTER_route('GET')
	def do_POST(self): self.ROUTER_route('POST')
	def do_PUT(self): self.ROUTER_route('PUT')
	def do_PATCH(self): self.ROUTER_route('PATCH')
	def do_DELETE(self): self.ROUTER_route('DELETE')

	def handle_unsupported(self):

		mod_path = 'modules'+self.path
		if not os.path.isdir(mod_path): self.send_error(404)
		else: self.send_error(501)

	def do_COPY(self): self.handle_unsupported()
	def do_OPTIONS(self): self.handle_unsupported()
	def do_LINK(self): self.handle_unsupported()
	def do_UNLINK(self): self.handle_unsupported()
	def do_PURGE(self): self.handle_unsupported()
	def do_LOCK(self): self.handle_unsupported()
	def do_UNLOCK(self): self.handle_unsupported()
	def do_PROPFIND(self): self.handle_unsupported()
	def do_VIEW(self): self.handle_unsupported()

	def ROUTER_send_response(self,code,content_type,data):
		
		self.send_response(code)
		self.send_header('Content-type', mime_types[content_type])
		self.end_headers()
		self.wfile.write(bytes(data,encoding))

	def ROUTER_get_JSON(self):
		
		if self.headers['Content-Type'] != 'application/json': return None
		content_length = int(self.headers['Content-Length'])
		return json.loads(self.rfile.read(content_length).decode(encoding))

	def list_modlues(self):
		
		mods = list()
		for dirname, dirnames, filenames in os.walk('modules'):
			for subdirname in dirnames:
				if '__pycache__' not in subdirname:
					mods.append(os.path.join(dirname, subdirname).replace('modules/',''))
		return mods

	def ROUTER_do_DEFAULT(self):
		
		index = '<ul>'
		for path in self.list_modlues(): index += '<li><a href="/'+path+'">'+path+'</a></li>'
		index += '</ul>'
		self.ROUTER_send_response(
			200,
			'.html',
			'<h1>SnekServer Index</h1> \
			 <h2><a href="https://github.com/aBozowski/SnekServer">GitHub</a></h2> \
			 <h3>Modules</h3>'+index)

	def ROUTER_route(self,verb):

		requested_mod = self.path
		if requested_mod[-1] == '/': requested_mod = requested_mod[:len(requested_mod)-1]
		if len(requested_mod) > 0: requested_mod = requested_mod[1:]
		mod_path = 'modules/'+requested_mod
		
		if requested_mod == '':
			if verb == 'GET': self.ROUTER_do_DEFAULT()
			else: self.send_error(501)
		
		elif not os.path.isdir(mod_path): self.send_error(404)
		else:
			try:
				requested_mod = requested_mod.replace('/','.')
				requested_mod_name = requested_mod[requested_mod.rfind('.')+1:]
				exec('from modules.'+requested_mod+' import '+requested_mod_name)
				exec('self.ROUTER_do_'+verb+' = '+requested_mod_name+'.ROUTER_do_'+verb)
			except (ImportError, AttributeError): self.send_error(501)
			try: getattr(self,'ROUTER_do_'+verb)(self)
			except Exception:
				print_exc()
				self.send_error(500)
