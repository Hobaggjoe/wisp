from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, Email, Optional
from datetime import datetime
import json
import os
from pdf_generator import generate_comprehensive_wisp_pdf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wisp_generator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class WISP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    data = db.Column(db.Text)  # JSON storage for all form data
    
    def get_data(self):
        return json.loads(self.data) if self.data else {}
    
    def set_data(self, data_dict):
        self.data = json.dumps(data_dict)

# Form Classes for each step
class CompanyInfoForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_size = SelectField('Company Size', choices=[
        ('', 'Select company size'),
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-1000', '201-1000 employees'),
        ('1000+', '1000+ employees')
    ], validators=[DataRequired()])
    industry = SelectField('Industry', choices=[
        ('', 'Select industry'),
        ('accounting', 'Accounting/CPA'),
        ('legal', 'Legal Services'),
        ('healthcare', 'Healthcare'),
        ('financial', 'Financial Services'),
        ('consulting', 'Consulting'),
        ('technology', 'Technology'),
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Business Address', validators=[DataRequired()])

class DataCollectionForm(FlaskForm):
    personal_info_types = SelectField('Types of Personal Information Collected', choices=[
        ('basic', 'Basic contact information only'),
        ('financial', 'Financial information (SSN, banking, etc.)'),
        ('healthcare', 'Healthcare/medical information'),
        ('employment', 'Employment records and payroll'),
        ('comprehensive', 'Comprehensive personal data')
    ], validators=[DataRequired()])
    data_sources = TextAreaField('Data Collection Sources', 
        description='Describe how and where you collect personal information')
    data_retention = SelectField('Data Retention Period', choices=[
        ('1year', '1 year'),
        ('3years', '3 years'),
        ('7years', '7 years'),
        ('indefinite', 'Indefinite/As required by law')
    ], validators=[DataRequired()])
    data_destruction = BooleanField('Do you have a process to destroy data when no longer needed?')

class SystemsForm(FlaskForm):
    quickbooks = BooleanField('QuickBooks')
    adp = BooleanField('ADP Payroll')
    workday = BooleanField('Workday')
    salesforce = BooleanField('Salesforce')
    office365 = BooleanField('Microsoft 365')
    google_workspace = BooleanField('Google Workspace')
    custom_software = TextAreaField('Other Systems/Software', 
        description='List any other systems that handle sensitive data')

class SecurityControlsForm(FlaskForm):
    mfa_enabled = BooleanField('Multi-Factor Authentication (MFA) enabled')
    data_encryption = BooleanField('Data encryption at rest')
    transmission_encryption = BooleanField('Data encryption in transmission')
    regular_backups = BooleanField('Regular data backups')
    firewall_protection = BooleanField('Firewall protection')
    antivirus_software = BooleanField('Antivirus software')
    password_policy = BooleanField('Written password policy')
    security_updates = BooleanField('Regular security updates and patches')

class VendorsForm(FlaskForm):
    vendor_list = TextAreaField('Third-Party Vendors with Data Access', 
        description='List all vendors, contractors, or service providers who have access to sensitive data')
    vendor_agreements = BooleanField('Do you have written agreements with all vendors regarding data protection?')
    vendor_monitoring = BooleanField('Do you regularly monitor vendor compliance?')

class EmployeeAccessForm(FlaskForm):
    access_control = BooleanField('Do you have role-based access controls?')
    employee_training = BooleanField('Do you provide regular security awareness training?')
    training_frequency = SelectField('Training Frequency', choices=[
        ('', 'Select frequency'),
        ('quarterly', 'Quarterly'),
        ('biannual', 'Twice per year'),
        ('annual', 'Annual'),
        ('onboarding', 'New employee onboarding only')
    ])
    incident_response = BooleanField('Do you have a written incident response plan?')
    background_checks = BooleanField('Do you conduct background checks for employees with data access?')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    wisps = WISP.query.order_by(WISP.updated_at.desc()).all()
    return render_template('dashboard.html', wisps=wisps)

@app.route('/wizard/start')
def start_wizard():
    # Clear any existing session data
    session.clear()
    return redirect(url_for('wizard_step', step=1))

@app.route('/wizard/step/<int:step>', methods=['GET', 'POST'])
def wizard_step(step):
    if step < 1 or step > 6:
        return redirect(url_for('index'))
    
    # Form mapping
    forms = {
        1: CompanyInfoForm(),
        2: DataCollectionForm(),
        3: SystemsForm(),
        4: SecurityControlsForm(),
        5: VendorsForm(),
        6: EmployeeAccessForm()
    }
    
    form = forms[step]
    
    if request.method == 'POST' and form.validate_on_submit():
        # Store form data in session
        step_key = f'step_{step}'
        session[step_key] = {}
        
        for field in form:
            if field.name != 'csrf_token':
                session[step_key][field.name] = field.data
        
        # Move to next step or finish
        if step < 6:
            return redirect(url_for('wizard_step', step=step + 1))
        else:
            return redirect(url_for('wizard_complete'))
    
    # Pre-populate form with session data if available
    step_key = f'step_{step}'
    if step_key in session:
        for field_name, value in session[step_key].items():
            if hasattr(form, field_name):
                getattr(form, field_name).data = value
    
    return render_template(f'wizard/step_{step}.html', form=form, step=step)

@app.route('/wizard/complete')
def wizard_complete():
    # Collect all session data
    wisp_data = {}
    for i in range(1, 7):
        step_key = f'step_{i}'
        if step_key in session:
            wisp_data.update(session[step_key])
    
    if not wisp_data.get('company_name'):
        flash('Please complete all wizard steps', 'error')
        return redirect(url_for('wizard_step', step=1))
    
    # Save to database
    wisp = WISP(company_name=wisp_data['company_name'])
    wisp.set_data(wisp_data)
    db.session.add(wisp)
    db.session.commit()
    
    # Clear session
    session.clear()
    
    return render_template('wizard/complete.html', wisp=wisp, wisp_data=wisp_data)

@app.route('/wisp/<int:wisp_id>')
def view_wisp(wisp_id):
    wisp = WISP.query.get_or_404(wisp_id)
    wisp_data = wisp.get_data()
    return render_template('wisp/view.html', wisp=wisp, wisp_data=wisp_data)

@app.route('/wisp/<int:wisp_id>/pdf')
def download_wisp_pdf(wisp_id):
    wisp = WISP.query.get_or_404(wisp_id)
    wisp_data = wisp.get_data()
    
    # Generate comprehensive PDF using the external function
    buffer = generate_comprehensive_wisp_pdf(wisp, wisp_data)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{wisp_data.get('company_name', 'WISP')}_WISP.pdf",
        mimetype='application/pdf'
    )

@app.route('/wisp/<int:wisp_id>/delete', methods=['POST'])
def delete_wisp(wisp_id):
    wisp = WISP.query.get_or_404(wisp_id)
    db.session.delete(wisp)
    db.session.commit()
    flash('WISP deleted successfully', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)