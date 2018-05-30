# coding=utf-8
from http.server import BaseHTTPRequestHandler
import cgi
import json
import requests
from requests_toolbelt.multipart import encoder

import Message
from CommitCache import CommitCache
from Query import Query
from Result import Result

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

        commit_hash = url.split('/')[-1]
        project_name = url.split('/')[-3]
        cache = CommitCache()
        isExist = cache.find(commit_hash)
        cache.close()
        if isExist:
            # 如果存在缓存，向服务器请求缓存
            a = {'commit_hash': commit_hash, 'project_name': project_name}
            print(commit_hash, project_name)
            r = requests.post('http://localhost:12007/DiffMiner/main/fetchMetaCache', json=a)
            print(r.status_code)
            print(r.content)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(r.content)
        else:
            # 没有缓存，向github请求meta信息
            query = Query(url)
            file_list, meta = query.query()
            if file_list is not None:
                if file_list == Message.invalid_url:
                    #     无效url，不访问服务器
                    self.send_response(200)
                    self.end_headers()
                    result = Result(True, "please enter correct commit url")
                    self.wfile.write(result.__dict__.__str__().encode())
                elif file_list == Message.no_parent_commit:
                    self.send_response(200)
                    self.end_headers()
                    result = Result(True, "commit has no parent commits")
                    self.wfile.write(result.__dict__.__str__().encode())
                else:
                    self.send_response(200)
                    self.end_headers()
                    result = Result(True, "")
                    # self.wfile.write(result.__dict__.__str__().encode())
                    # 访问服务器
                    # 此时已经获得所有文件，生成一个
                    multipart_encoder = initData(file_list, meta)
                    print(multipart_encoder)
                    r = requests.post('http://localhost:12007/DiffMiner/main', data=multipart_encoder,
                                      headers={'Content-Type': multipart_encoder.content_type})
                    self.wfile.write(r.content)
                    cache = CommitCache()
                    cache.add_commit_hash(commit_hash, project_name)
                #    请求结束
                # 写入数据库
                return
            else:
                self.send_response(200)
                result = Result(True, "please enter correct commit url")
                self.end_headers()
                self.wfile.write(result.__dict__.__str__().encode())
                return


def StartServer():
    port = 8081
    print('server started')
    from http.server import HTTPServer
    sever = HTTPServer(("", port), PostHandler)
    sever.serve_forever()


if __name__ == '__main__':
    StartServer()
