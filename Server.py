# coding=utf-8
from http.server import BaseHTTPRequestHandler
import cgi
import json
import requests
from requests_toolbelt.multipart import encoder

import Api
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
        boundary="xxx---fdse---xxx",
    )

    return multipart_encoder


# 获取文件
def fetchFile(self, form):
    dict = {}
    for field in form.keys():
        field_item = form[field]
        key = field_item.name
        value = field_item.value
        dict[key] = value
    # 获取指定文件内容 link diff
    r = requests.post(Api.FETCH_FILE_CONTENT,data=dict)
    print(r.status_code)
    content = r.content
    # print(content)
    self.send_response(200)
    self.end_headers()
    self.wfile.write(content)


# 请求meta信息
def fetchMeta(self, form):
    for field in form.keys():
        field_item = form[field]
        key = field_item.name
        value = field_item.value
        if key == 'url':
            url = value
            print(url)
    # https://github.com/basti-shi031/CommitClawerSever/commit/ad34ef79b84c8ec3a3f71608051c638510ccd330
    # 找不为空的最后一个字段是commit_id
    # 最后第三个不会空的id是project_name
    keys = url.split('/')
    keySize = len(keys)
    commit_hash = ''
    project_name = ''
    # 不为空的字段数量
    validKey = 0
    for i in range(0, keySize)[::-1]:
        if keys[i] != '':
            validKey += 1
            if validKey == 1:
                commit_hash = keys[i]
            elif validKey == 3:
                project_name = keys[i]
                break
    cache = CommitCache()
    isExist = cache.find(commit_hash)
    if isExist:
        # 如果存在缓存，向服务器请求缓存
        a = {'commit_hash': commit_hash, 'project_name': project_name}
        print(commit_hash, project_name)
        r = requests.post(Api.FETCH_META, json=a)
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
                r = requests.post(Api.GENERATE_META, data=multipart_encoder,
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


# 删除commit表内数据
def clearCommitTable():
    cache = CommitCache()
    cache.clear_commit_record()

# 清空服务器上的output数据
def clearOutputInServer(self):
    response = requests.post(Api.DELETE_OUTPUT_DIR)
    self.send_response(200)
    self.end_headers()
    self.wfile.write(response.content)



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
            fetchFile(self, form)
        elif path.startswith('/clearCommitRecord'):
            #     清空数据库缓存，清除
            clearCommitTable()
            clearOutputInServer(self)
        elif path.startswith('/fetchMeta'):
            # 根据本地是否有缓存请求数据
            # 如果有缓存，直接向minner请求meta数据
            # 如果没有，向github爬去文件和meta信息，交给minner存储。
            fetchMeta(self, form)



def StartServer():
    port = 8081
    print('server started')
    from http.server import HTTPServer
    sever = HTTPServer(("", port), PostHandler)
    sever.serve_forever()


if __name__ == '__main__':
    StartServer()
