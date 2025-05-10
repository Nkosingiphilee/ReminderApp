from Reminderapp import app,db
from flask import render_template,flash,redirect,url_for
from Reminderapp.forms import AdminForm,EmployeeForm
from Reminderapp.models import Admin,Employee
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/')
@app.route('/home')
def index():
	test=Admin.query.all()
	return render_template('landing.html',admin=test)
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	form=AdminForm()
	if form.validate_on_submit():
		user=Admin.query.filter_by(email=form.email.data).first()
		if user and user.hash_password==form.password.data:
			login_user(user, remember=False)
			#flash('loggedIn successful!', 'success')
			return redirect(url_for('dashboard'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html' ,form=form)
	
@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You logged out!', 'info')
	return redirect(url_for('login'))	
				
								
@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')	

@app.route('/employee-list')
def employee_list():
	employees=Employee.query.all()
	return render_template('employee-list.html',employees=employees)
	
@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
	form=EmployeeForm()
	if form.validate_on_submit():
		flash('sent','success')
	return render_template('add-employee.html',form=form)
	
	
@app.route('/employee-profile/<id>')
def employee_profile(id):
	employee=Employee.query.get(id)
	return render_template('employee-profile.html',employee=employee)
	
	
@app.errorhandler(404)

def page_not_found(e):

	return render_template('404.html'), 404
	
	

@app.errorhandler(500)

def internal_server_error(e):

	return render_template('500.html'), 500