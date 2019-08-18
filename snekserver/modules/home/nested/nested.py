def ROUTER_do_GET(self):
	self.ROUTER_send_response(
			200,
			'.html',
			'<h1>IN NESTED!</h1>')
