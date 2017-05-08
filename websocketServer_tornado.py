import tornado.web
import tornado.websocket 
import tornado.ioloop
import json

class SocketHandler(tornado.websocket.WebSocketHandler):
        clients = set()
	@staticmethod
	def send_to_all(message):
    		for c in SocketHandler.clients:
       			c.write_message(json.dumps(message))

	def open(self):
	        self.write_message(json.dumps({
                                      'type': 'sys',
                                      'message': 'Welcome to WebSocket',
                                      }))
       		SocketHandler.send_to_all({
                                      'type': 'sys',
                                      'message': str(id(self)) + ' has joined',
                                      })
       		SocketHandler.clients.add(self)


	def on_close(self):
		SocketHandler.clients.remove(self)
        	SocketHandler.send_to_all({
       		 'type': 'sys',
       		 'message': str(id(self)) + ' has left',
    		})
	def on_message(self, message):
        	SocketHandler.send_to_all({
                          'type': 'user',
                          'id': id(self),
                          'message': message,})

class Index(tornado.web.RequestHandler):
	def get(self):
		self.render('html/index.html')


if __name__ == '__main__':

    app = tornado.web.Application([
        ('/', Index),
        ('/soc', SocketHandler),
    ])
    app.listen(8001)
    tornado.ioloop.IOLoop.instance().start()

