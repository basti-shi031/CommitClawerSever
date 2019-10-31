import json
from requests_toolbelt.multipart import encoder


class DataNet(object):
    # 生成参数
    @staticmethod
    def initData(file_list, meta):
        divider = '----'

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
