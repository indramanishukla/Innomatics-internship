
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import string
import random


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
# ...

class Urls(db.Model):
    # __tablename__ = 'url_table'
    id = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.String(100), nullable=False)
    short = db.Column(db.String(5), nullable=False)
    
    def __init__(self, long, short):
        self.long = long
        self.short= short

    



@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method=='GET':
        return render_template('home.html')

@app.route('/generate', methods = ['POST']) 
def generate_url():

    
    original_url = request.form['in_1']
    if not original_url:
        return 'Please enter url'
            
    found_url =  Urls.query.filter_by(long = original_url).first()
    if found_url:
        return render_template('generate.html', short = found_url.short)
        
    else:
        gen_short = [''.join(random.choice(string.ascii_letters+string.digits) for i in range(3))][0]
            
        entry = Urls(original_url, gen_short)
        db.session.add(entry)
        db.session.commit()

        return render_template('generate.html', short = gen_short )

@app.route('/<short_url>')
def redirect_url(short_url):
    matched_url = Urls.query.filter_by(short=short_url).first()
    if matched_url:
        return redirect(matched_url.long)
    else:
        return 'Invalid Short Url'

@app.route('/history')
def history():
    get_url = Urls.query.all()
    return render_template('display.html',get_url= get_url) 



if __name__== '__main__':
    app.run(debug=True)