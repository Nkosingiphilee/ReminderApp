from Reminderapp import app,db,mail
from flask import render_template,flash,redirect,url_for,session
from Reminderapp.forms import AdminForm,EmployeeForm,EmployeeDocumentForm
from Reminderapp.models import User,Employee,EmployeeDocument,Role
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from werkzeug.utils import secure_filename
import os
import schedule
from datetime import datetime,timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from zoneinfo import ZoneInfo


@app.route('/')
@app.route('/home')
def index():
	test=User.query.all()	
	return render_template('landing.html',user=test)
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	form=AdminForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and user.hash_password==form.password.data:
			login_user(user, remember=False)
			#flash('loggedIn successful!','success')
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
	employees=User.query.filter_by(role_id=3).all()
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
	employee=User.query.get(id)
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

	

@app.route('/report')
def report():
	documents=EmployeeDocument.query.all()
	return render_template('report.html')
	
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
	
	

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500
	


scheduler = BackgroundScheduler(timezone=ZoneInfo("Africa/Johannesburg"))

def update_status(expiration_date):
    if expiration_date < datetime.now():
        status = "Expired"
    else:
        status = "Valid"
    return status


def doc_status():
        with app.app_context():
        	docs=EmployeeDocument.query.all()
        	for doc in docs:
        		doc.status=update_status(doc.expiring_date+timedelta(weeks=100))
        	db.session.commit()
        

sched =BackgroundScheduler(daemon=True)
sched.add_job(doc_status,'interval',seconds=10)
sched.start()
