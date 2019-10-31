import requests

import Api
from CommitCache import CommitCache


class IONet(object):
    # 删除commit表内数据
    @staticmethod
    def clearCommitTable():
        cache = CommitCache()
        cache.clear_commit_record()


    # 清空服务器上的output数据
    @staticmethod
    def clearOutputInServer(self2):
        response = requests.post(Api.DELETE_OUTPUT_DIR)
        self2.send_response(200)
        self2.end_headers()
        self2.wfile.write(response.content)
