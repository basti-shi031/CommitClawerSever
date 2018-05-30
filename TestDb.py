import requests

import CommitCache

cache = CommitCache.CommitCache()
cache.add_commit_hash("123")
cache.add_commit_hash("234")
cache.add_commit_hash("345")

print(cache.find("12323412323"))
print(cache.find("123"))
cache.close()
