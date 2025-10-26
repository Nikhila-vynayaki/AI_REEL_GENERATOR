from flask import Flask, render_template,request
import uuid
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET","POST"])
def create():
    myid=uuid.uuid1()
    if request.method == "POST":
        desc=request.form['text']
        id=request.form['uuid']
        input_files=[]
        for key,value in request.files.items():
            print(request.form['uuid'])
            print(f"{key}:{value}")
            file=request.files[key]
            if file:
                
                filename=secure_filename(file.filename)
                if(not(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],id)))):
                    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],id),exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],id, filename))
                input_files.append(filename)
        for fl in input_files:
            with open(os.path.join(app.config['UPLOAD_FOLDER'],id,"input.txt"),'a') as f:
                f.write(f"file '{fl}'\nduration 1\n")
        with open(os.path.join(app.config['UPLOAD_FOLDER'],id,"desc.txt"),'w') as f:
                    f.write(desc)

    return render_template("create.html",myid=myid)

@app.route("/gallery")
def gallery():
    reels=os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html",reels=reels)

app.run(debug=True)