def ROUTER_do_GET(self):
	self.ROUTER_send_response(
			200,
			'.html',
			'<h1>IN HOME!</h1>')

def ROUTER_do_POST(self):
	make_h_tag = lambda content, level: '<h'+str(level)+'>'+str(content)+'</h'+str(level)+'>'
	content = make_h_tag('echo POST Data',1)
	data = self.ROUTER_get_JSON()
	if data != None:
		for key,value in data.items():
			content += make_h_tag(key,2)
			content += make_h_tag(value,3)
	self.ROUTER_send_response(200,'.html',content)
