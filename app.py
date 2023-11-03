from flask import Flask, render_template, Response, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField
from flask_uploads import configure_uploads, IMAGES, UploadSet, UploadNotAllowed
import os
import json

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'supersecretpasskey'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'

images = UploadSet('photos', ('jpg'))
configure_uploads(app, images)

class UploadForm(FlaskForm):
    name = StringField('name')
    age = IntegerField("age")
    image = FileField('image')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        
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
        
        
        return redirect(url_for('result'))
    return render_template("index.html", form=form)

@app.route('/result')
def result():
    file = open('static/output.json')
    op = json.load(file)
    return render_template("interactive_result.html", content=op)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)