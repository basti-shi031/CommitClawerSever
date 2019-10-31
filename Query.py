import Message
import NetUtil
import ContentConverter
import threading
import U
import re


class Query(object):
    def __init__(self, url):
        self.url = url

    # return
    # 1 status_code
    # 2 message
    # 3 content
    def query(self):
        U.p(self.url)
        if not re.match('^https://github.com/', self.url):
            return -1, Message.invalid_url, None
        else:
            status_code, message, content = fetch(self.url)
            if status_code == 200:
                if message is not Message.success:
                    # 无内容
                    return status_code, message, None
                else:
                    file_list = content[0]
                    meta = content[1]
                    download(file_list)
                    return status_code, Message.success, (file_list, meta)
            else:
                return status_code, Message.internet_error, None


# return
# 1 status code
# 2 message
# 3 content

def fetch(url):
    commit_response, status_code = NetUtil.fetch_info(url)
    if status_code == 200:
        # 变化文件、parent commit 地址、id
        file_list, meta = ContentConverter.convert_commit_info(commit_response, url)
        if file_list is None:
            # 没有找到
            return 200, Message.no_parent_commit, None
        elif len(file_list) == 0:
            return 200, Message.no_related_java_file, None
        else:
            for file in file_list:
                NetUtil.convert2_raw_url(file)
            return 200, Message.success, (file_list, meta)
    else:
        return status_code, Message.internet_error, None


def download_file(file):
    U.p(file.raw_url)
    # if 'ThreadPoolTaskExecutor.java' in file.raw_url:
    #     a = 1
    try:
        raw, status_code = NetUtil.fetch_file_info(file.raw_url)
        if status_code == 200:
            # file.raw = str(raw_soup)
            file.raw = raw
        else:
            file.raw = ''
        parent_raws = []
        parent_size = len(file.get_parent_raw_urls())
        for index in range(parent_size):
            raw, status_code = NetUtil.fetch_file_info(file.get_parent_raw_urls()[index])
            if status_code == 200:
                parent_raw = raw
            else:
                # 网络错误
                # 无文件
                parent_raw = ''
            parent_raws.insert(index, parent_raw)
        file.set_parent_raws(parent_raws)
    except Exception:
        print(Message.internet_error)


# 下载
def download(file_list):
    file_size = len(file_list)
    threads = []
    for index in range(file_size):
        t = threading.Thread(target=download_file, args=(file_list[index],), name=index)
        threads.append(t)
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
