import U
import re
import File


# 如果没有parent branch，返回空
# 否则返回改变的文件列表
def convert_commit_info(soup, url):
    # 获取parentBranch Id,list形式
    parent_branch_id_html = soup.findAll('a', attrs={'class': 'sha'})
    if parent_branch_id_html is None or len(parent_branch_id_html) == 0:
        # 没有parent branch
        U.p("No Parent Branch")
        return
    else:
        parent_ids = []
        parent_urls = []
        for html in parent_branch_id_html:
            parent_branch_id = html.string
            parent_branch_url = html.get('href')
            parent_ids.append(parent_branch_id)
            parent_urls.append('https://github.com' + parent_branch_url)
        # /basti-shi031/LeetCode_Python/commit/d6e5d51963b237b0df4534aad0ffea9780390052
        # 查找改变的文件列表
        # 先找span标签 class 为diffstat float-right
        span_list = soup.findAll(name='span', attrs={"class": "diffstat float-right"})
        file_list = []
        for span in span_list:
            # 遍历列表，获得span的父元素li，通过li获得a标签内容
            li = span.parent
            file_name = li.findAll('a', attrs={'href': re.compile('^#diff')})[1].string
            action = li.find('svg').get("title")
            if filter_file(file_name):
                file_list.append(File.File(file_name, action, url, parent_urls, parent_ids, ""))
        return file_list


def filter_file(file):
    file_suffix = file.split('.')[-1]
    return ('.' + file_suffix) in File.file_type_list
