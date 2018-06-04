import requests

import CommitCache

# cache = CommitCache.CommitCache()
# cache.add_commit_hash("123")
# cache.add_commit_hash("234")
# cache.add_commit_hash("345")
#
# print(cache.find("12323412323"))
# print(cache.find("123"))
# cache.close()
url = 'a/b/c/d////'
keys = url.split('/')
keySize = len(keys)
commit_hash= ''
for i in range(0, keySize)[::-1]:
    commit_hash = keys[i]
    if commit_hash !='':
        break
print(commit_hash)
