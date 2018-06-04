# 接口文件
# 根路径
BASE_URL = 'http://localhost:12007/DiffMiner/main'

# API
# 访问github 并在miner生成cache
GENERATE_META = BASE_URL + '/genCache'
# 获取metaCache
FETCH_META = BASE_URL+ '/fetchMetaCache'
# 获取文件内容 link 和 diff
FETCH_FILE_CONTENT = BASE_URL+ '/fetchContent'
