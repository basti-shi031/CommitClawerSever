import Message
import NetUtil
import ContentConverter
import threading
import U
import re


class Query(object):
    def __init__(self, url):
        self.url = url

    def query(self):
        U.p(self.url)
        if not re.match('^https://github.com/', self.url):
            return Message.invalid_url, None
        else:
            file_list, meta = fetch(self.url)
            U.p(file_list)
            if (file_list is None):
                # 为空，说明没有parent commit
                return Message.no_parent_commit, None
            else:
                download(file_list)
                return file_list, meta


def fetch(url):
    commit_response, status_code = NetUtil.fetch_info(url)
    if status_code == 200:
        # 变化文件、parent commit 地址、id
        file_list, meta = ContentConverter.convert_commit_info(commit_response, url)
        if file_list is None:
            return None, None
        else:
            for file in file_list:
                NetUtil.convert2_raw_url(file)
            return file_list, meta
    elif status_code == 404:
        # todo
        print('error')
        return None, None


def download_file(file):
    U.p(file.raw_url)
    # if 'ThreadPoolTaskExecutor.java' in file.raw_url:
    #     a = 1
    raw, status_code = NetUtil.fetch_file_info(file.raw_url)
    if status_code == 200:
        # file.raw = str(raw_soup)
        file.raw = raw
    else:
        file.raw = ''

    parent_raws = []
    parent_size = len(file.get_parent_raw_urls())
    for index in range(parent_size):
        raw_soup, status_code = NetUtil.fetch_info(file.get_parent_raw_urls()[index])
        if status_code == 200:
            parent_raw = raw_soup.text
        else:
            # 无文件
            parent_raw = ''
        parent_raws.insert(index, parent_raw)
    file.set_parent_raws(parent_raws)


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
