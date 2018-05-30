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
        return file_list, meta


def filter_file(file):
    file_suffix = file.split('.')[-1]
    return ('.' + file_suffix) in File.file_type_list
