import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from plug_app import app , db ,bcrypt
from plug_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, SkilltagForm, ProjectsForm
from plug_app.models import User, Post, Skilltag, Projects
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import MetaData, Column

@app.route('/', methods=['GET' , 'POST' ])
@app.route('/register', methods=['GET' , 'POST' ])

def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()
	if form.validate_on_submit():

		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(Firstname=form.First_name.data, Secondname=form.Second_name.data, username=form.username.data, email=form.email.data, password=hashed_password)

		db.session.add(user)
		db.session.commit()
		flash('account made')
		return redirect(url_for('login'))

	return render_template('register.html', title='Register', form=form)
#////////////// PROJECT UPLOADER ///////////////////////////////
# renaming pic to a random hex str with original extension and then saving 
#it into static folder  FOR PROJECT PICTURES
#/////////////////// ADD USER ID AT THE FRONT OF HEX/////////////////////



@app.route('/projects', methods=['GET' , 'POST' ])
@login_required
def projects():
	form = ProjectsForm()
	image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
	random_hex = secrets.token_hex(5)
	random_hex_two = secrets.token_hex(5)

	Project_id = "P_ID"+"_"+ str(current_user.id)+"_"+random_hex
	uid = current_user.id

	Img_id = Project_id+"Img_ID"+"_"+random_hex_two
	Vid_id  = Project_id+"Vid_id"+"_"+random_hex_two
	Doc_id  = Project_id+"Doc_id "+"_"+random_hex_two

	def save_prjct_img(project_form_picture):
		_name, f_ext = os.path.splitext(project_form_picture.filename)
		picture_fn = Img_id + f_ext
		picture_path = os.path.join(app.root_path, 'static/project_upload', picture_fn)
		project_form_picture.save(picture_path)
		
		return picture_fn

	d_picture_fn = save_prjct_img(form.cover_img.data)

	if form.cover_img.data:
		picture_file = save_prjct_img(form.cover_img.data)
		#current_user.image_file = picture_file	

	if form.validate_on_submit():
		project = Projects( user_id=uid, Title=form.Title.data, TxtContent=form.TxtContent.data, Project_id=Project_id, Img_id=d_picture_fn, Vid_id=Vid_id, Doc_id=Doc_id, Requests=form.Requests.data )

		db.session.add(project)
		db.session.commit()
		flash('project uploaded')	
		return redirect(url_for('search'))


	return render_template('project.html', title='projects upload', form=form, image_file=image_file)	


@app.route('/Skilltag', methods =['GET', 'POST'])
def Skilltag():
	form = SkilltagForm()
	if form.validate_on_submit():
		#result = User.query.filter(User.email == "test@gmail.com")
		#fresult = result[0].id
		skilltag = Skilltag(web_developer=form.Skilltag.data)
		db.session.add(skilltag)
		db.session.commit()

		flash('Skilltag added')
		return redirect(url_for('search'))

	return render_template('skilltags.html', title='Home', form=form)





@app.route('/home',methods =['GET' , 'POST'])
@login_required
def home():
    return render_template('home.html', title='home')

@app.route('/newsfeed',methods =['GET' , 'POST'])
@login_required
def newsfeed():
	result = User.query.all()
	return render_template('newsFeed.html', title='home', result=result )

@app.route('/newsfeed2',methods =['GET' , 'POST'])
@login_required
def newsfeed2():
	result = Projects.query.all()
	user_id = result[0]

	post_user = User.query.filter(User.id == "1")
	#fresult = result[0].id


	image_file = url_for('static', filename='project_upload/')
	return render_template('newsFeed2.html', title='home', result=result, image_file=image_file, user_id=user_id, post_user=post_user)





@app.route('/search',methods =['GET' , 'POST'])
#@login_required
def search():
    return render_template('search.html', title='search')

@app.route('/layout',methods =['GET' , 'POST'])
def layout():
    return render_template('layout.html', title='layout')


@app.route('/area',methods =['GET' , 'POST'])
def peopleInArea():
    return render_template('peopleInArea.html', title='peopleInArea')	



@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('register'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	
	if current_user.is_authenticated:
		return  redirect(url_for('search'))
	form = LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else: 
				return redirect(url_for('search'))	
	return render_template('login.html', title='login', form=form)

#////////////// PROFILE PIC UPLOADER ///////////////////////////////
# renaming profile pic to a random hex str with original extension and then saving 
#it into static folder  FOR PROFILE PICTURES
#/////////////////// ADD USER ID AT THE FRONT OF HEX/////////////////////
def save_img(form_picture):
	random_hex = secrets.token_hex(8)
	_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
# Resizing uploaded image using pillow packad
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn



@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	image_file = url_for('static', filename='profile_pics/'+current_user.image_file)

	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_img(form.picture.data)
			current_user.image_file = picture_file

		current_user.Firstname = form.First_name.data
		current_user.Secondname = form.Second_name.data
		current_user.email = form.email.data
		current_user.username = form.username.data
		db.session.commit()

		flash('account updated')
		return redirect(url_for('account'))

	elif request.method == 'GET':
		form.First_name.data = current_user.Firstname
		form.Second_name.data = current_user.Secondname
		form.email.data = current_user.email
		form.username.data = current_user.username
	return render_template('account.html', title='Account', form=form, image_file=image_file)









  