import requests
from requests_toolbelt.multipart import encoder
from requests_toolbelt.multipart.encoder import MultipartEncoder

import requests

multiple_files = [
    ('https://github.com/.../qweqweqe/A.java', 'public void main....'),
    ('https://github.com/.../qweqweqe/A.java_parent_0', 'public int main...'),
    ('https://github.com/.../qweqweqe/A.java_parent_1', 'public static void...'),
    ('https://github.com/.../qweqweqe/B.java', 'aaaaa'),
    ('https://github.com/.../qweqweqe/B.java_parent_0', 'bbbb')]

multipart_encoder = encoder.MultipartEncoder(
    fields=multiple_files,
    boundary="xxx---------------xxx",
)

r = requests.post('http://httpbin.org/post', data=multipart_encoder,
                  headers={'Content-Type': multipart_encoder.content_type})
print(r.request.body)
print(r.status_code)
