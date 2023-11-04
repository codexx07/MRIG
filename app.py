from flask import Flask, render_template, Response, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField
from flask_uploads import configure_uploads, IMAGES, UploadSet, UploadNotAllowed
import os
import json
import re
import mail

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'supersecretpasskey'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'

images = UploadSet('photos', ('jpg'))
configure_uploads(app, images)

class UploadForm(FlaskForm):
    name = StringField('name')
    gender = StringField('gender')
    email = StringField('email')
    age = IntegerField("age")
    image = FileField('image')

def validateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(regex,email)

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
        mail.sendMail(email)
        print("mail sent")
        op_file = open("static/input.json", "w")
        json.dump(op, op_file, indent=4)
        print("exported to json")
        return redirect(url_for('result'))
    
    return render_template("Page1.html", form=form)

@app.route('/result')
def result():
    file = open('static/output.json')
    op = json.load(file)
    return render_template("xray.html", content=op)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)