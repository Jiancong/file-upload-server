import requests
import json

#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

url = "http://localhost:5000/uploader"
fin = open('ml2.jpg', 'rb')
filedic = {'file': fin}
clientinfos = {'client_ver': '2.0',"client_type":"android"}

try:
  r = requests.post(url, files=filedic, data=(clientinfos))
  print(r.text)

finally:
  fin.close()
