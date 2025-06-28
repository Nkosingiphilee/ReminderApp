from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TelField,DateField,FileField,SelectField
from wtforms.validators import DataRequired,Email,Length
from wtforms.validators import ValidationError

from .models import User



class AdminForm(FlaskForm):
	email=StringField('your email address',validators=[DataRequired(),Email()])
	password=PasswordField('your password',validators=[DataRequired()])
	button=SubmitField('Login')
	
	
class EmployeeForm(FlaskForm):
	full_name=StringField('employee full name',validators=[DataRequired(),Length(min=2, max=50)])
	email=StringField('your email address',validators=[DataRequired(),Email()])
	dob=DateField('date of birth',validators=[DataRequired()])
	email=StringField('employee email',validators=[DataRequired(),Email()])
	phone_number=TelField('cellphone number',validators=[DataRequired(),Length(min=10, max=20)])
	department=SelectField("Department", choices=[
    ('', 'Select Department'),  # Default option
    ('HR', 'Human Resources'),
    ('IT', 'Information Technology'),
    ('Finance', 'Finance'),
    ('Marketing', 'Marketing'),
    # Add more departments as needed
], validators=[DataRequired()])
	position=StringField("position",validators=[DataRequired(),Length(min=2, max=20)])
	submit=SubmitField('add employee')
	
	
	def validate_email(self, email):
	       user = User.query.filter_by(email=email.data).first()
	       if user:
	       	raise ValidationError('This email is taken')

	def validate_phone_number(self,phone_number):
	       user = User.query.filter_by(phone_no=phone_number.data).first()
	       if user:
	       	raise ValidationError('This phone number is taken')
	
	
class EmployeeDocumentForm(FlaskForm):
	document=FileField("upload your document",validators=[])
	document_type=StringField('document type',validators=[])
	issue_date=DateField('issued on ',validators=[])
	expiring_date=DateField('expire on ',validators=[])
	
	submit=SubmitField('upload document')