from flask import Flask, render_template, Response, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField
from flask_uploads import configure_uploads, IMAGES, UploadSet, UploadNotAllowed
from flask_executor import Executor

import os
import json
import re

import pdfgenerator
import mail

import ml_gen
import speedometer_gen
import heat_map_gen
import bar_graphs

import tcl

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'supersecretpasskey'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'

images = UploadSet('photos', ('jpg', 'png'))
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
        
        ext = os.path.splitext(filename)[1]
        try:
            os.rename("static/uploads/"+filename, "static/uploads/input"+ext)
        except FileExistsError:
            if ext == ".png":
                os.remove("static/uploads/input.png")
            else:
                os.remove("static/uploads/input.jpg")
            
            os.rename("static/uploads/"+filename, "static/uploads/input"+ext)
        
        op = {}
        op['name'] = name
        op['age'] = age
        op['gender'] = gender
        op['email'] = email
        op['filename'] = "/static/uploads/input"+ext
        print(op)
        op_file = open("static/input.json", "w+")
        json.dump(op, op_file, indent=4)
        ml_gen.predict(op['filename'][1:])
        return redirect(url_for('result'))
    
    return render_template("Page1.html", form=form)

@app.route('/result')
def result():
    file_op = open('static/output.json')
    op = json.load(file_op)
    file_op.close()
    file_ip = open("static/input.json")
    ip = json.load(file_ip)
    if os.path.exists("static/uploads/input.png"):
        bar_graphs.generate("static/uploads/input.png")
        heat_map_gen.generate("static/uploads/input.png")
        speedometer_gen.generate("static/uploads/input.png")
        pdfgenerator.generate_pdf("static/input.json", "static/output.json", "static/uploads/input.jpg", "static/outputs/heatmap.png","static/outputs/bar_graph.png","static/outputs/speedometers.png","static/media/logoXray.png")
    else:
        bar_graphs.generate("static/uploads/input.jpg")
        heat_map_gen.generate("static/uploads/input.jpg")
        speedometer_gen.generate("static/uploads/input.jpg")
        pdfgenerator.generate_pdf("static/input.json", "static/output.json", "static/uploads/input.jpg", "static/outputs/heatmap.png","static/outputs/bar_graph.png","static/outputs/speedometers.png","static/media/logoXray.png")
    executor.submit(mail.sendMail, ip['email'])
    return render_template("xray.html", content={'input': ip, 'output': op})

@app.route('/get', methods=['GET'])
def get_response():
    userTxt = request.args.get('usrMsg')
    print(userTxt)
    if not os.path.exists(tcl.vectordb_file_path):  # Only create vector db if it doesn't exist
        tcl.create_vector_db()

    vectordb = tcl.FAISS.load_local(tcl.vectordb_file_path, tcl.instructor_embeddings)  # Load the vector database once
    chain_instance = tcl.get_qa_chain(vectordb)  # Create the chain instance once using the loaded vector database
    output = tcl.ask_question(chain_instance, userTxt)
    print(output)
    return output

if __name__ == "__main__":
    app.run(debug=True, threaded=True)