import NetUtil
import ContentConverter
import threading
import U

# 下载线程数量
THREAD_NUM = 3


def fetch(url):
    commit_response, status_code = NetUtil.fetch_info(url)
    if status_code == 200:
        # 变化文件、parent commit 地址、id
        file_list = ContentConverter.convert_commit_info(commit_response, url)
        if file_list is None:
            return
        else:
            for file in file_list:
                NetUtil.convert2_raw_url(file)
            return file_list
    elif status_code == 404:
        print('error')


def download_file(file):
    raw_soup, status_code = NetUtil.fetch_info(file.raw_url)
    if status_code == 200:
        file.raw = raw_soup.text
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
        U.p(file.name)
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


if __name__ == '__main__':
    commit_url = "https://github.com/basti-shi031/ApplicationRelease/commit/d52f2cc8e787feae36b043476c486045fe6e6668"
    print(commit_url)
    file_list = fetch(commit_url)
    if (file_list is None):
        # 为空，说明没有parent commit
        pass
    else:
        download(file_list)