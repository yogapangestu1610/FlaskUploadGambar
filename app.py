
from flask import Flask, json, request, jsonify
import os
import urllib.request
from werkzeug.utils import secure_filename
import sqlite3
from datetime import datetime 
 
app = Flask(__name__)

con=sqlite3.connect("myimage.db")
con.execute("create table if not exists image(id integer primary key,img TEXT)")
con.close()

app.secret_key = "caircocoders-ednalan"
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def main():
    return 'Hallo, Mohammad Prayoga Pangestu'
 
@app.route('/upload', methods=['POST'])
def upload_file():
    con = sqlite3.connect("myimage.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from image")
    data = cur.fetchall()
    con.close()
    
   # periksa apakah request post memiliki bagian file
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'Tidak ada bagian file dalam request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(fullpath)
            con=sqlite3.connect("myimage.db")
            cur=con.cursor()
            cur.execute("insert into image(img)values(?)",(filename,))
            con.commit()
    
            success = True
            
            print(filename)
        else:
            errors[file.filename] = 'Jenis file tidak diperbolehkan'
 

    if success:
        resp = jsonify({'message' : 'Files berhasil di upload'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
 
if __name__ == '__main__':
    app.run(debug=True)