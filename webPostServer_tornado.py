import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('html/index.html')

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        if self.request.files:
            myfile = self.request.files['myfile'][0]
            fin = open("html/in.jpg","w")
            print "success to open file"
            fin.write(myfile["body"])
            fin.close()

application=tornado.web.Application([
                                     (r'/',MainHandler),
                                     (r'/upload', UploadHandler) ]
                                    )

if __name__=='__main__':
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
