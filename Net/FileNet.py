import requests

import Api


class FileNet(object):
    # 获取文件
    @staticmethod
    def fetchFile(form, self2):
        dict = {}
        for field in form.keys():
            field_item = form[field]
            key = field_item.name
            value = field_item.value
            dict[key] = value
        # 获取指定文件内容 link diff
        r = requests.post(Api.FETCH_FILE_CONTENT, data=dict)
        content = r.content
        # print(content)
        self2.send_response(r.status_code)
        self2.end_headers()
        self2.wfile.write(content)
