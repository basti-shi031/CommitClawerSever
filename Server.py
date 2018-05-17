# coding=utf-8
from http.server import BaseHTTPRequestHandler
import cgi
import json
import requests
from requests_toolbelt.multipart import encoder

import Message
from Query import Query

divider = '----'


# 生成参数
def initData(file_list, meta):
    multiple_files = []
    for file in file_list:
        multiple_files.append((file.url + '/' + file.name, file.raw))
        size = len(file.parent_urls)
        for index in range(size):
            parent_url = file.parent_urls[index]
            parent_raw = file.parent_raws[index]
            print(parent_url, parent_raw)
            print(type(parent_url))
            print(type(file.name))
            print(type(divider))
            print(type(index))
            multiple_files.append((parent_url + '/' + str(file.name) + divider + 'parent' + str(index), parent_raw))
    multiple_files.append(('meta', json.dumps(meta.__dict__)))
    print(json.dumps(meta.__dict__))
    multipart_encoder = encoder.MultipartEncoder(
        fields=multiple_files,
        boundary="xxx---------------xxx",
    )

    return multipart_encoder


class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     }
        )

        groupId = None
        artifactId = None
        version = None
        content = None
        url = None
        for field in form.keys():
            field_item = form[field]
            key = field_item.name
            value = field_item.value
            # filesize = len(filevalue)#文件大小(字节)
            # print len(filevalue)
            # print(key)
            if key == 'artifactId':
                artifactId = value
            if key == 'groupId':
                groupId = value
            if key == 'version':
                version = value
            if key == 'url':
                url = value
                print(url)
            # print(value)
            # with open(filename+".txt",'wb') as f:
            #     f.write(filevalue)
        if groupId != None and artifactId != None and version != None:
            # content = get_pom(groupId, artifactId, version)
            pass

        query = Query(url)
        file_list, meta = query.query()
        if file_list is not None:
            if file_list == Message.invalid_url:
                #     无效url，不访问服务器
                self.send_response(200, file_list)
            else:
                # 访问服务器
                # 此时已经获得所有文件，生成一个
                multipart_encoder = initData(file_list, meta)
                r = requests.post('http://httpbin.org/post', data=multipart_encoder,
                                  headers={'Content-Type': multipart_encoder.content_type})
                print(r.request.body)
                print(r.status_code)
                self.send_response(200)
                self.end_headers()
            # self.wfile.write(('Client: %sn \n' % str(self.client_address)).encode())
            # self.wfile.write(('User-agent: %sn\n' % str(self.headers['user-agent'])).encode())
            # self.wfile.write(('Path: %sn\n'%self.path).encode())
            # self.wfile.write(('Form data:n\n').encode())
            # self.wfile.write('File:fileName.pom\n'.encode())
            # if content is None:
            #     self.wfile.write("".encode(encoding="utf-8"))
            # else:
            #     self.wfile.write(content)
            return
        else:
            self.send_response(404)
            self.end_headers()
            return


def StartServer():
    print('server started')
    from http.server import HTTPServer
    sever = HTTPServer(("", 8080), PostHandler)
    sever.serve_forever()


if __name__ == '__main__':
    StartServer()
