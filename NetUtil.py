import requests
from bs4 import BeautifulSoup


# 根据url返回soup信息
def fetch_info(url):
    response = requests.get(url, timeout=30)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    return soup, response.status_code


# 根据url返回soup信息
def fetch_file_info(url):
    response = requests.get(url, timeout=30)
    response.encoding = 'utf-8'
    # soup = BeautifulSoup(response.text,from_encoding='utf-8')
    return response.text, response.status_code


def convert2_raw_url(file):
    file.set_raw_url(convert_2_raw_url(file.url, file.name))
    size = len(file.parent_urls)
    parent_raw_urls = []
    for index in range(size):
        parent_raw_urls.append(convert_2_raw_url(file.parent_urls[index], file.name))
    file.set_parent_raw_urls(parent_raw_urls)


# url转化成rawUrl
# url:https://github.com/basti-shi031/ScreenRecordManager/commit/5d08c3cc50a492158208340e354a2c608e2e4732/README.md
# rawUrl: https://raw.githubusercontent.com/basti-shi031/ScreenRecordManager/5d08c3cc50a492158208340e354a2c608e2e4732/README.md
def convert_2_raw_url(url, file):
    index = url.find('commit')
    raw_url = 'https://raw.githubusercontent.com' + url[18:index] + url[index + 7:] + '/' + file
    return raw_url
