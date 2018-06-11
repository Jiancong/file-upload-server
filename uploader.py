import os
from flask import Flask, render_template, request, send_from_directory, Response
from werkzeug import secure_filename
import hashlib
from datetime import datetime
from shutil import copyfile

app = Flask(__name__)

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg',  'bmp' ])

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def allowed_file(filename):
    file_ext=filename.rsplit('.', 1)[-1]
    status = '.' in filename and file_ext in ALLOWED_EXTENSIONS
    return file_ext, status

#    return '.' in filename and \
#           filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return "Hello world!"

@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      ver = request.form["client_ver"]
      clienttype = request.form['client_type']
	
      print("ver=>", ver )
      print("clienttype=>", clienttype)

      if ver != "1.0" or clienttype != "android":
          print('[upload] secret info not matched!')
          return Response('Error uploading', status=500)

      if f.filename == '':
          print('[upload] Upload attempt with no filename')
          return Response('No filename uploaded', status=500)

      if f: 
          fext, status = allowed_file(f.filename)
          if status:
              filename = secure_filename(f.filename)
              f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
              
              tmppath = md5(os.path.join(app.config['UPLOAD_FOLDER'], filename)) + "." + fext

              os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], tmppath))
              return Response('Uploaded file successfully', status=200)
   return

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
		
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=int('5000'), debug=True)
