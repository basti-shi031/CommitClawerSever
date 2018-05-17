class File(object):
    def __init__(self, name, action, url, parent_urls, parent_ids, id):
        self.name = name
        self.action = action
        self.url = url
        self.parent_urls = parent_urls
        self.parent_ids = parent_ids
        self.id = id

    def get_parent_raw_urls(self):
        return self.parent_raw_urls;

    def set_raw_url(self, raw_url):
        self.raw_url = raw_url

    def set_parent_raw_urls(self, parent_raw_urls):
        self.parent_raw_urls = parent_raw_urls

    def set_raw(self, raw):
        self.raw = raw

    def set_parent_raws(self, raws):
        self.parent_raws = raws


file_type_list = ['.java', '.Java', '.JAVA']
