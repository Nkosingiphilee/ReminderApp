from Reminderapp import app,db,mail
from flask import render_template,flash,redirect,url_for
from Reminderapp.forms import AdminForm,EmployeeForm,EmployeeDocumentForm
from Reminderapp.models import Admin,Employee,EmployeeDocument
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from werkzeug.utils import secure_filename
import os
import schedule

'''
def send_email():
    msg = Message('Stat Of The Application',
                  sender='noreply@demo.com',
                  recipients='Phungulankosingiphile828@gmail.com')
    msg.body = f'''#the application reminds you about documents expirstion
'''
    mail.send(msg)
'''
 
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
		employee=Employee(employee_fname=form.full_name.data,
		dob=form.dob.data,
		employee_email=form.email.data,
		employee_no=form.phone_number.data,
		department=form.department.data,
		position=form.position.data
		)
		db.session.add(employee)	
		db.session.commit()
		flash('new employee added','success')
		return redirect(url_for('employee_list'))
	return render_template('add-employee.html',form=form)
	
	
@app.route('/employee-profile/<id>')
def employee_profile(id):
	employee=Employee.query.get(id)
	return render_template('employee-profile.html',employee=employee)

	
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']	
# im having an issue handling the document submission	
@app.route('/upload-document',methods=['POST','GET'])
def upload_document():
	form=EmployeeDocumentForm()
	if form.validate_on_submit():
	       document = form.document.data
	       if document and allowed_file(document.filename):
	           filename = secure_filename(document.filename)
	           document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	           flash('document uploaded','info')
	return render_template('upload-document.html', form=form)
	
@app.errorhandler(404)

def page_not_found(e):

	return render_template('404.html'), 404
	
	

@app.errorhandler(500)

def internal_server_error(e):

	return render_template('500.html'), 500
	

