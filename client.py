#coding=utf-8  
import requests  
import os
url = "http://127.0.0.1:8080"
# url = "http://10.222.147.212:8080"
# path = os.getcwd()+"/handle_pom.py"
# print(path)
# files = {'file': open(path, 'rb')}
# //org.apache.tomcat/tomcat-jdbc/
# m_data = {"groupId":"org.apache.tomcat","artifactId":"tomcat-jdbc","version":"9.0.8","id":260}

# files = {'file':open(path,'rb')}
# r = requests.post(url, files=files)

while True:
    url = "https://github.com/basti-shi031/BaseActivity/commit/6a1fd220d362c232178b4cda1d7f2ad9893abe66"
    m_data = {"groupId": "ai.h2o", "artifactId": "h2o-classic-parent", "version": "2.5", "id": 285,"url":url};
    r = requests.post(url, data=m_data)
    print(r.url)
    print(r.text)