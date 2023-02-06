from flask import Flask,render_template,request,url_for,request,Response
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pickle
from werkzeug.utils import secure_filename
import json
import os
from datetime import datetime


# for Indivisual-Prediction:-
app = Flask(__name__)
model = pickle.load(open('rfmodel.pkl', 'rb'))

@app.route('/Individual-Test')
def Individual_Test():
    return render_template('Individual-Test.html',params=params)
@app.route('/predict', methods=['POST','GET'])
def predict():
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output =  prediction[0]
    if output==1:
        return render_template('Individual-Test.html',params=params, prediction_text="Prediction result:- Congratulations you have heart disease")
    else:
        return render_template('Individual-Test.html',params=params, prediction_text="Prediction result:- sorry to say that you dont have chances of heart disease")


with open('config.json', 'r') as c:
    params = json.load(c)["params"]


local_server = True


app.config['UPLOAD_FOLDER'] = params['upload_location']
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']

db = SQLAlchemy(app)


class Contact(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_no= db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

@app.route("/")
def home():
    return render_template("index.html",params=params)

@app.route("/about")
def about():
    return render_template("about.html",params=params)

@app.route("/Dataset_test")
def Dataset_test():
    return render_template("Dataset_test.html",params=params)

@app.route("/index.html")
def index():
    return render_template("index.html",params=params)

@app.route("/uploader", methods = ['GET', 'POST'])
def uploader():
        if request.method=='POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded successfully!"

@app.route("/contact", methods = ['GET', 'POST'])

def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name=name, phone_no = phone, message = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html',params=params)
if __name__ == '__main__':
    app.run(debug=True)