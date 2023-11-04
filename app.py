from flask import Flask, render_template, Response, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField
from flask_uploads import configure_uploads, IMAGES, UploadSet, UploadNotAllowed
from flask_executor import Executor

import os
import json
import re

import jsonpdfgen
import mail

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'supersecretpasskey'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'

images = UploadSet('photos', ('jpg'))
configure_uploads(app, images)

executor = Executor(app)

class UploadForm(FlaskForm):
    name = StringField('name')
    gender = StringField('gender')
    email = StringField('email')
    age = IntegerField("age")
    image = FileField('image')

def validateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(regex,email)

def validateAge(age):
    return age not in range(1,101)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        name = form.name.data
        gender = form.gender.data
        age = form.age.data
        email = form.email.data

        if validateEmail(email) == None:
            flash("Wrong E-Mail Format!")
            return redirect(url_for('index'))
        
        if validateAge(age):
            flash("Please enter your correct age!")
            return redirect(url_for("index"))
        try:
            filename = images.save(form.image.data)
        except UploadNotAllowed:
            flash("Filetype not supported! Upload JPEGS!")
            return redirect(url_for('index'))
        
        try:
            os.rename("static/uploads/"+filename, "static/uploads/input.jpg")
        except FileExistsError:
            os.remove("static/uploads/input.jpg")
            os.rename("static/uploads/"+filename, "static/uploads/input.jpg")
        
        op = {}
        op['name'] = name
        op['age'] = age
        op['gender'] = gender
        op['email'] = email
        print(op)
        op_file = open("static/input.json", "w+")
        json.dump(op, op_file, indent=4)
        print("exported to json:", op_file.read())
    

        return redirect(url_for('result'))
    
    return render_template("Page1.html", form=form)

@app.route('/result')
def result():
    file_op = open('static/output.json')
    op = json.load(file_op)
    file_op.close()
    file_ip = open("static/input.json")
    ip = json.load(file_ip)
    executor.submit(mail.sendMail, ip['email'])
    jsonpdfgen.generate_pdf("static/input.json", "static/output.json", "static/uploads/input.jpg", "static/media/logoXray.png")
    return render_template("xray.html", content={'input': ip, 'output': op})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)