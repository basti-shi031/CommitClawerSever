# coding=utf-8
from http.server import BaseHTTPRequestHandler
import cgi
from Net.FileNet import FileNet
from Net.IONet import IONet
from Net.MetaNet import MetaNet
from Net.DataNet import DataNet





class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     }
        )
        path = self.path
        if path.startswith('/fetchFile'):
            # 向minner请求指定文件和diff link
            FileNet.fetchFile(form, self2=self)
        elif path.startswith('/fetchMeta'):
            # 根据本地是否有缓存请求数据
            # 如果有缓存，直接向minner请求meta数据
            # 如果没有，向github爬去文件和meta信息，交给minner存储。
            MetaNet.fetchMeta(form,self2=self)
        else:
            self.send_response(200)
            DUMMY_RESPONSE = "dummy request"
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(DUMMY_RESPONSE))
            self.end_headers()
            self.wfile.write(DUMMY_RESPONSE.encode('utf-8'))

    def do_GET(self):
        path = self.path
        if path.startswith('/clearCommitRecord'):
            #     清空数据库缓存，清除
            print("clear record")
            IONet.clearCommitTable()
            IONet.clearOutputInServer(self2=self)
        else:
            self.send_response(200)
            DUMMY_RESPONSE = "dummy request"
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(DUMMY_RESPONSE))
            self.end_headers()
            self.wfile.write(DUMMY_RESPONSE.encode('utf-8'))


def StartServer():
    port = 8081
    print('server started')
    from http.server import HTTPServer
    sever = HTTPServer(("", port), PostHandler)
    sever.serve_forever()


if __name__ == '__main__':
    StartServer()
