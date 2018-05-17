class Meta(object):
    def __init__(self, author, date_time, committer, commit_hash, children, parents):
        self.author = author
        self.date_time = date_time
        self.committer = committer
        self.commit_hash = commit_hash
        self.children = children
        self.parents = parents
