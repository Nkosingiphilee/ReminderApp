from Reminderapp import db,app,login_manager
from wtforms import ValidationError
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

class Role(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	role=db.Column(db.String(15) ,unique=True)
	users=db.relationship('User', backref='role',lazy='dynamic')

class User(db.Model,UserMixin):
	id=db.Column(db.Integer, primary_key=True)
	full_name=db.Column(db.String(100) ,nullable=False)
	email=db.Column(db.String(60),nullable=False,unique=True)
	phone_no=db.Column(db.String(15),nullable=False,unique=True)
	hash_password=db.Column(db.String(100),nullable=False ,default='password')
	role_id=db.Column(db.Integer ,db.ForeignKey('role.id'),nullable=False ,default=3)
	employee=db.relationship('Employee', backref='user')
	


class Employee(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	dob=db.Column(db.DateTime , default=datetime.utcnow)
	department=db.Column(db.String(25), nullable=True)
	position=db.Column(db.String(25))
	documents = db.relationship('EmployeeDocument', backref='employee' ,lazy=True)
	user_id=db.Column(db.Integer ,db.ForeignKey('user.id'))
	

class EmployeeDocument(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	document=db.Column(db.String(25),nullable=True)
	document_type=db.Column(db.String(25),nullable=True)
	status=db.Column(db.String(25),nullable=False,default="valid/not expired")
	issue_date=db.Column(db.DateTime())
	expiring_date=db.Column(db.DateTime())
	upload_date=db.Column(db.DateTime() ,nullable=False,default=datetime.utcnow)
	employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)



	
	
with app.app_context():
	db.create_all()
	
	
	roles=[
	Role(role='Admin'),
	Role(role='Employer'),
	Role(role='Employee')
	]
	
	users=[
	User(full_name='Admin Administrator',
	email='administrator@admin.com',phone_no='+27 657246328',
	hash_password='Administrator',
	role_id=1),
	User(full_name='Empl Employer',
	email='employer@empl.com',
	phone_no='+27 657246329',
	hash_password='Employer',
	role_id=2),
	User(full_name='Nkosingiphile phungula',
	email='phungula@admin.com',
	phone_no='+27 657246320',
	hash_password='password',
	role_id=3),
	User(full_name='kwandiso phungula',
	email='phungula2@admin.com',
	phone_no='+27 657246321',
	hash_password='password',
	role_id=3),
	User(full_name='Nkosingiphile mnguni',
	email='mnguni@admin.com',
	phone_no='+27 657246310',
	hash_password='password',
	role_id=3),User(full_name='Nkosingiphile khumalo',
	email='khumalo@admin.com',
	phone_no='+27 657246324',
	hash_password='password',
	role_id=3),User(full_name='mzwandile thango',
	email='thango@admin.com',
	phone_no='+27 657246325',
	hash_password='password',
	role_id=3)
	]
	
	
	employees=[
	Employee(
	dob=datetime(1990, 1, 1),
	department='HR',
	position='Manager', user_id=3),
	Employee(
	dob=datetime(1991, 2, 2),
	department='Marketing',
	position='Executive', user_id=4),
	Employee(
	dob=datetime(1992, 3, 3),
	department='Sales',
	position='Representative', user_id=5),
	Employee(
	dob=datetime(1993, 4, 4),
	department='IT',
	 position='Developer'
	 , user_id=6),
	 Employee(
	 dob=datetime(1994, 5, 5),
	 department='Finance',
	 position='Accountant', user_id=7)
	 ]
	 
	employeesDocument=[
	
  EmployeeDocument(document='Resume', document_type='resume', issue_date=datetime(1994, 5, 5), expiring_date=datetime(1994, 5, 5), employee_id=1),
    EmployeeDocument(document='Contract', document_type='employment contract', issue_date=datetime(1994, 5, 5), expiring_date=datetime(1994, 5, 5), employee_id=1),
    EmployeeDocument(document='cv.pdf', document_type='curriculum vitae', issue_date=datetime(1994, 5, 5), expiring_date=datetime(1994, 5, 5), employee_id=2),
    EmployeeDocument(document='Contract', document_type='employment contract', issue_date=datetime(1994, 5, 5), expiring_date=datetime(1994, 5, 5), employee_id=2),
    EmployeeDocument(document='resume.pdf', document_type='resume', issue_date=datetime(1994, 5, 5), expiring_date=datetime(1994, 5, 5), employee_id=3),
    EmployeeDocument(document='Contract', document_type='employment contract', issue_date=datetime(1994, 5, 5), expiring_date=datetime(1994, 5, 5), employee_id=3),
    EmployeeDocument(document='myresume.pdf', document_type='resume', issue_date=datetime(1994, 5, 5), expiring_date=datetime(1994, 5, 5), employee_id=4),
    EmployeeDocument(document='Contract', document_type='employment contract', issue_date=datetime(1994, 5, 5), expiring_date=datetime(1994, 5, 5), employee_id=4),
    EmployeeDocument(document='resume2024.pdf', document_type='resume', issue_date=datetime(1994, 5, 5), expiring_date=datetime(1994, 5, 5), employee_id=5),
    EmployeeDocument(document='Contract', issue_date=datetime(1994, 5, 5), expiring_date=datetime(1994, 5, 5), document_type='employment contract', employee_id=5),
    EmployeeDocument(document='Resume', document_type='resume', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=1),
    EmployeeDocument(document='Contract', document_type='employment contract', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=2),
    EmployeeDocument(document='ID Card', document_type='ID card', status='expired', issue_date=datetime(2015, 1, 1), expiring_date=datetime(2020, 1, 1), employee_id=3),
    EmployeeDocument(document='Certification', document_type='certification', status='valid', issue_date=datetime(2018, 1, 1), expiring_date=datetime(2023, 1, 1), employee_id=4),
    EmployeeDocument(document='Transcript', document_type='academic transcript', status='valid', issue_date=datetime(2019, 1, 1), expiring_date=datetime(2024, 1, 1), employee_id=5),
    EmployeeDocument(document='Document 0', document_type='identification document', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=1),
    EmployeeDocument(document='Document 1', document_type='employment contract', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=2),
    EmployeeDocument(document='ID Card', document_type='ID card', status='expired', issue_date=datetime(2015, 1, 1), expiring_date=datetime(2020, 1, 1), employee_id=3),
    EmployeeDocument(document='Certification', document_type='certification', status='valid', issue_date=datetime(2018, 1, 1), expiring_date=datetime(2023, 1, 1), employee_id=4),
    EmployeeDocument(document='Transcript', document_type='academic transcript', status='valid', issue_date=datetime(2019, 1, 1), expiring_date=datetime(2024, 1, 1), employee_id=5),
    EmployeeDocument(document='License', document_type='professional license', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1,1),employee_id=6),
EmployeeDocument(document='Certificate', document_type='professional certificate', status='expired', issue_date=datetime(2015, 1, 1), expiring_date=datetime(2020, 1, 1), employee_id=7),
    EmployeeDocument(document='Agreement', document_type='employment agreement', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=8),
    EmployeeDocument(document='Permit', document_type='work permit', status='valid', issue_date=datetime(2018, 1, 1), expiring_date=datetime(2023, 1, 1), employee_id=9),
    EmployeeDocument(document='Registration', document_type='professional registration', status='valid', issue_date=datetime(2019, 1, 1), expiring_date=datetime(2024, 1, 1), employee_id=10),
    EmployeeDocument(document='Document 11', document_type='identification document', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=1),
    EmployeeDocument(document='Document 12', document_type='employment contract', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=2),
    EmployeeDocument(document='Document 13', document_type='ID card', status='expired', issue_date=datetime(2015, 1, 1), expiring_date=datetime(2020, 1, 1), employee_id=3),
    EmployeeDocument(document='Document 14', document_type='certification', status='valid', issue_date=datetime(2018, 1, 1), expiring_date=datetime(2023, 1, 1), employee_id=4),
    EmployeeDocument(document='Document 15', document_type='academic transcript', status='valid', issue_date=datetime(2019, 1, 1), expiring_date=datetime(2024, 1, 1), employee_id=5),
    EmployeeDocument(document='Document 16', document_type='professional license', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=6),
    EmployeeDocument(document='Document 17', document_type='ID card', status='expired', issue_date=datetime(2015, 1, 1), expiring_date=datetime(2020, 1, 1), employee_id=7),
    EmployeeDocument(document='Document 18', document_type='employment agreement', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=8),
    EmployeeDocument(document='Document 19', document_type='certification', status='valid', issue_date=datetime(2018, 1, 1), expiring_date=datetime(2023, 1, 1), employee_id=9),
    EmployeeDocument(document='Document 20', document_type='academic transcript', status='valid', issue_date=datetime(2019, 1, 1), expiring_date=datetime(2024, 1, 1), employee_id=10),
    EmployeeDocument(document='Document 22', document_type='identification document', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=2),
    EmployeeDocument(document='Document 23', document_type='employment contract', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=3),
    EmployeeDocument(document='Document 24', document_type='ID card', status='expired', issue_date=datetime(2015, 1, 1), expiring_date=datetime(2020, 1, 1), employee_id=4),
    EmployeeDocument(document='Document 25', document_type='certification', status='valid', issue_date=datetime(2018, 1, 1), expiring_date=datetime(2023, 1, 1), employee_id=5),
    EmployeeDocument(document='Document 26', document_type='academic transcript', status='valid', issue_date=datetime(2019, 1, 1), expiring_date=datetime(2024, 1, 1), employee_id=6),
    EmployeeDocument(document='Document 27', document_type='professional license', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1),employee_id=7),

    EmployeeDocument(document='Document 28', document_type='ID card', status='expired', issue_date=datetime(2015, 1, 1), expiring_date=datetime(2020, 1, 1), employee_id=8),
    EmployeeDocument(document='Document 29', document_type='employment agreement', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=9),
    EmployeeDocument(document='Document 30', document_type='certification', status='valid', issue_date=datetime(2018, 1, 1), expiring_date=datetime(2023, 1, 1), employee_id=10),
    EmployeeDocument(document='Document 31', document_type='identification document', status='valid', issue_date=datetime(2019, 1, 1), expiring_date=datetime(2024, 1, 1), employee_id=1),
    EmployeeDocument(document='Document 32', document_type='employment contract', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=2),
    EmployeeDocument(document='Document 33', document_type='ID card', status='expired', issue_date=datetime(2015, 1, 1), expiring_date=datetime(2020, 1, 1), employee_id=3),
    EmployeeDocument(document='Document 34', document_type='employment agreement', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=4),
    EmployeeDocument(document='Document 35', document_type='certification', status='valid', issue_date=datetime(2018, 1, 1), expiring_date=datetime(2023, 1, 1), employee_id=5),
    EmployeeDocument(document='Document 36', document_type='academic transcript', status='valid', issue_date=datetime(2019, 1, 1), expiring_date=datetime(2024, 1, 1), employee_id=6),
    EmployeeDocument(document='Document 37', document_type='professional license', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=7),
    EmployeeDocument(document='Document 38', document_type='ID card', status='expired', issue_date=datetime(2015, 1, 1), expiring_date=datetime(2020, 1, 1), employee_id=8),
    EmployeeDocument(document='Document 39', document_type='employment agreement', status='valid', issue_date=datetime(2020, 1, 1), expiring_date=datetime(2025, 1, 1), employee_id=9),
    EmployeeDocument(document='Document 40', document_type='certification', status='valid', issue_date=datetime(2018, 1, 1), expiring_date=datetime(2023, 1, 1), employee_id=10),
    EmployeeDocument(document='Document 41', document_type='identification document', status='valid', issue_date=datetime(2019, 1, 1), expiring_date=datetime(2024, 1, 1), employee_id=1),

	]


	try:
		db.session.add_all(roles)
		db.session.add_all(users)
		db.session.add_all(employees)
		db.session.add_all(employeesDocument)
		db.session.commit()
	except:
		db.session.rollback()
		
		
		
