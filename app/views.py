"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import os
import time
from app import app
from flask import render_template, request, redirect, url_for
from app import db
from app.models import User

from .forms import ProfileForm
from flask import jsonify
import models
from app.models import ProfileSchema
from werkzeug import secure_filename
from flask_wtf.file import FileField
###
# Routing for your application.
###

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/person')
def person():
  first_user = db.session.query(User).first()
  return jsonify() #"firstname: {},lastname: {},age: {},sex: {},image: {}".format(first_user.firstname,first_user.lastname, first_user.age,first_user.sex,first_user.image)  

@app.route( '/profile' , methods =[ "GET" , "POST" ])
def profile():
    form = ProfileForm ()
    if request.method == "POST":
      file = request.files['image']
      image = secure_filename(file.filename)
      
file.save(os.path.join(app.config['UPLOAD_FOLDER'], image))
      
      first_name = form.first_name.data
      last_name = form.last_name.data
      age = form.age.data
      sex = form.sex.data
      addinfo = User(first_name, last_name, age, sex, image)
      #f = request.form["firstname"]
      #l = request.form["lastname"]
      #a = request.form["age"]
      #s = request.form["sex"]
      #m = request.form["image"]
      #u = User(f,l,a,s,m)
      db.session.add(addinfo)
      db.session.commit()
      return render_template("profile.html", form = form)
    return render_template ( 'profile.html' , form = form)
  
@app.route('/profiles', methods = ["GET", "POST"])
def profiles():
  #user = db.session.query(User).all()
  user = models.User.query.all()
  if request.method == "POST":
    myData = ProfileSchema(many = True)
    data = myData.dump(user)
    return jsonify({"User": data.data})
  return render_template('profile.html', user = user)
  
@app.route('/profile/<int:userid>', methods = ["GET", "POST"])
def profileid(userid):
  #user = db.session.query(User).first()
  # show the user profile for that user
  user = User.query.filter_by(userid = userid).first()
  if request.method == "POST":
    date = str(user.profile_add_on)
    return jsonify(user = user.userid, profile_add_on = date, first_name = user.first_name, last_name = user.last_name, age = user.age, sex = user.sex)
  return render_template('user.html', user = user)
    
@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

#@app.route("/profile")
#def profile():
 #  """Render home page for profile.html."""
  # return render_template("profile.html") 
  
def timeinfo():
  now = time.strftime("%Y-%m-%d")
  return now

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
