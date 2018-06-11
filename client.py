import requests

#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

url = "http://localhost:80/uploader"
fin = open('ml2.jpg', 'rb')
files = {'file': fin}

try:
  r = requests.post(url, files=files)
  print r.text

finally:
  fin.close()
