from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, HiddenField, EmailField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    form_loaded_at = HiddenField()
    company_code = StringField('Company Code')

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    company = StringField('Company Name', validators=[DataRequired()])
    business_type = StringField('Business Type / Area', validators=[DataRequired()])
    
    service = SelectField('Service Interested In', choices=[
        ('', 'Select a service'),
        ('Website Design', 'Website Design'),
        ('Website Development', 'Website Development'),
        ('Website Hosting', 'Website Hosting'),
        ('Website Migration', 'Website Migration'),
        ('Website Maintenance', 'Website Maintenance'),
        ('Other', 'Other'),
    ], validators=[DataRequired()])

    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])