import urllib.request
import urllib.parse
import urllib.error
response = urllib.request.urlopen("http://www.baidu.com")
print(response.read())

#模仿登录
values = {"username": "100..", "password":"xxxx"}
data = urllib.parse.urlencode(values)
url = "...."
#post
req = urllib.request.Request(url, data)
#get
req = urllib.request.Request("%s?%s"%(url,data))
res = urllib.request.urlopen(req)
print(res.read())

req = urllib.request.Request('http://blog.csdn.net/cqcre1')
try:
    urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.reason)
