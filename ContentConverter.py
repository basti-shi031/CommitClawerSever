import NetUtil
import U
import re
import File

# 如果没有parent branch，返回空
# 否则返回改变的文件列表
from Meta import Meta


def convert_commit_info(soup, url):
    # 获取parentBranch Id,list形式
    parent_branch_id_html = soup.findAll('a', attrs={'class': 'sha'})
    if parent_branch_id_html is None or len(parent_branch_id_html) == 0:
        # 没有parent branch
        U.p("No Parent Branch")
        return None, None
    else:
        author = None
        date = None
        committer = None
        commit_hash = None
        children = None
        commit_log = None
        parents = []
        # <a data-pjax="#js-repo-pjax-container" href="/basti-shi031/LoopViewPager">LoopViewPager</a>
        project_name = soup.find('a', attrs={'data-pjax': '#js-repo-pjax-container'}).text
        # <a class="url fn" rel="author" href="/basti-shi031">basti-shi031</a>
        # 作者
        author = soup.find('a', attrs={'class': 'url fn', 'rel': 'author'}).text
        # <relative-time datetime="2016-01-11T03:09:39Z" title="2016年1月11日 GMT+8 上午11:09">on 11 Jan 2016</relative-time>
        # 时间
        date = soup.find('relative-time').get('datetime')
        # <a href="/basti-shi031/RichTextView/commits?author=basti-shi031"
        # class="commit-author tooltipped tooltipped-s user-mention"
        # aria-label="View all commits by basti-shi031">basti-shi031</a>
        # committer
        committer = soup.find('a', attrs={'class': 'commit-author tooltipped tooltipped-s user-mention'}).text
        # <span class="sha user-select-contain">1a2219ebb73464497f5efa8dba8823781a4e887e</span>
        # commit_hash
        commit_hash = soup.find('span', attrs={'class': 'sha user-select-contain'}).text
        # <p class="commit-title">
        #       Merge branch 'master' of <a href="https://git
        # hub.com/basti-shi031/RichTextView">https://github.com/basti-shi031/RichTextView</a>
        #     </p>
        # commit_log
        commit_log = soup.find('p', attrs={'class': 'commit-title'}).text
        U.p(author)
        U.p(date)
        U.p(committer)
        U.p(commit_hash)
        U.p(commit_log)
        parent_ids = []
        parent_urls = []
        for html in parent_branch_id_html:
            parent_branch_id = html.string
            parent_branch_url = html.get('href')
            parents.append(parent_branch_url.split('/')[-1])
            parent_ids.append(parent_branch_id)
            parent_urls.append('https://github.com' + parent_branch_url)
        meta = Meta(author, date, committer, commit_hash, commit_log, children, parents, project_name)
        # 查找改变的文件列表v3
        # 拼接url
        # https://github.com/spring-projects/spring-framework/
        # diffs?commit=3c1adf7f6af0dff9bda74f40dabe8cf428a62003
        # &sha1=9d63f805b3b3ad07f102f6df779b852b2d1f306c
        # &sha2=3c1adf7f6af0dff9bda74f40dabe8cf428a62003&start_entry=0
        # sha1是parent_commit_id
        # sha2是自己的commit_id
        # start_entry取0
        # 传进来的url https://github.com/spring-projects/spring-framework/commit/3c1adf7f6af0dff9bda74f40dabe8cf428a62003
        # 首先拼接成diff_url
        diff_url = url.split('/commit/')[0]
        diff_url = diff_url + '/diffs?commit=' + commit_hash + '&sha1=' + parents[
            0] + "&sha2=" + commit_hash + "&start_entry=0"
        diffResponse, code = NetUtil.fetch_info(diff_url)
        file_list = []
        file_list_htmls = diffResponse.findAll(name='a', attrs={'class': 'link-gray-dark'})
        print(len(file_list_htmls))
        for html in file_list_htmls:
            file_name = html.get("title")
            print(file_name)
            if filter_file(file_name):
                file_list.append(File.File(file_name, "", url, parent_urls, parent_ids, ""))
        return file_list, meta
        # ===============================================================================
        # /basti-shi031/LeetCode_Python/commit/d6e5d51963b237b0df4534aad0ffea9780390052
        # 查找改变的文件列表v2
        # 修改查找文件的方式
        # file_list_htmls = soup.findAll(name='a',attrs={'class':'link-gray-dark'})
        # file_list = []
        # for html in file_list_htmls:
        #     file_name = html.get("title")
        #     if filter_file(file_name):
        #         file_list.append(File.File(file_name, "", url, parent_urls, parent_ids, ""))
        # return file_list, meta
        # =================================================================================
        # 查找改变的文件列表v1
        # 先找span标签 class 为diffstat float-right
        # span_list = soup.findAll(name='span', attrs={"class": "diffstat float-right"})
        # file_list = []
        # for span in span_list:
        #     # 遍历列表，获得span的父元素li，通过li获得a标签内容
        #     li = span.parent
        #     file_name = li.findAll('a', attrs={'href': re.compile('^#diff')})[1].string
        #     action = li.find('svg').get("title")
        #     if filter_file(file_name):
        #         diff = li.find('a').get("href")
        #         # print(diff)
        #         diffResponse, code = NetUtil.fetch_info(url + diff)
        #         # print(diffResponse)
        #         real_file_name_html = diffResponse.find('a',attrs={'href':diff,'class':'link-gray-dark'})
        #         real_file_name = real_file_name_html.get('title')
        #         print(real_file_name)
        #         file_list.append(File.File(real_file_name, action, url, parent_urls, parent_ids, ""))
        # return file_list, meta


def filter_file(file):
    file_suffix = file.split('.')[-1]
    return ('.' + file_suffix) in File.file_type_list
