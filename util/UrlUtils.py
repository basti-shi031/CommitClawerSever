class UrlUtils(object):
    # 根据Url获取commitHash和projectName
    @staticmethod
    def genCommitHashAndProjectName(url):
        # 找不为空的最后一个字段是commit_id
        # 最后第三个不会空的id是project_name
        keys = url.split('/')
        keySize = len(keys)
        commit_hash = ''
        project_name = ''
        owner = ''
        # 不为空的字段数量
        validKey = 0
        for i in range(0, keySize)[::-1]:
            if keys[i] != '':
                validKey += 1
                if validKey == 1:
                    commit_hash = keys[i]
                elif validKey == 3:
                    project_name = keys[i]
                    break
        return commit_hash, project_name

    @staticmethod
    def getUrl(form):
        for field in form.keys():
            field_item = form[field]
            key = field_item.name
            value = field_item.value
            if key == 'url':
                url = value
                print(url)
        return url
