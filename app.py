from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, IntegerField, FieldList, FormField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, Optional
from datetime import datetime
import json
import os
from comprehensive_pdf_generator import generate_complete_rightworks_wisp_pdf

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
    # Basic Company Information
    company_name = StringField('Company Name', validators=[DataRequired()])
    street_address = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number')
    website = StringField('Website')
    
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
    
    # WISP preparation details
    prepared_by = StringField('WISP Prepared By (Name)', validators=[DataRequired()],
        description='Name of person preparing this WISP')
    annual_review_date = DateField('Annual Review Date', validators=[DataRequired()],
        description='Date for annual WISP review (typically one year from creation)')
    
    # EIN/EFIN Information
    ein_number = StringField('Employer Identification Number (EIN)')
    efin_number = StringField('Electronic Filing Identification Number (EFIN)',
        description='Required for tax preparers who file electronically')

class DataCollectionForm(FlaskForm):
    # Basic PII Types (for scope section)
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
    
    # PII Inventory Lists (detailed for template)
    third_party_apps_1 = StringField('Third-party App #1', 
        description='Name of third-party application that contains PII')
    third_party_apps_2 = StringField('Third-party App #2')
    
    cloud_providers_1 = StringField('Cloud Provider #1', 
        description='Name of cloud service provider (e.g., Google Drive, Dropbox)')
    cloud_providers_2 = StringField('Cloud Provider #2')
    
    data_storage_1 = StringField('Data Storage Solution #1', 
        description='Primary data storage location/method')
    data_storage_2 = StringField('Data Storage Solution #2')
    
    email_providers_1 = StringField('Email Provider #1', 
        description='Primary email service provider')
    email_providers_2 = StringField('Email Provider #2')
    
    crm_systems_1 = StringField('CRM System #1', 
        description='Customer Relationship Management systems')
    crm_systems_2 = StringField('CRM System #2')
    
    social_media_contractors_1 = StringField('Social Media Contractor #1', 
        description='Third-party managing social media accounts')
    social_media_contractors_2 = StringField('Social Media Contractor #2')

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
    # FTC Checklist Items
    qualified_individual_designated = BooleanField('Qualified individual designated')
    qualified_individual_vendor = StringField('Qualified Individual Vendor/Date')
    
    risk_assessment_conducted = BooleanField('Risk assessment conducted')
    risk_assessment_vendor = StringField('Risk Assessment Vendor/Date')
    
    encryption_at_rest = BooleanField('Encryption at rest')
    encryption_at_rest_vendor = StringField('Encryption at Rest Vendor/Date')
    
    encryption_in_transit = BooleanField('Encryption in transit')
    encryption_in_transit_vendor = StringField('Encryption in Transit Vendor/Date')
    
    mfa_enabled = BooleanField('Multi-Factor Authentication (MFA) enabled')
    mfa_vendor = StringField('MFA Vendor/Date')
    
    continuous_monitoring = BooleanField('Continuous monitoring with IDS/RMM or network scan and penetration testing')
    continuous_monitoring_vendor = StringField('Continuous Monitoring Vendor/Date')
    
    security_awareness_training = BooleanField('Security awareness training')
    security_awareness_vendor = StringField('Security Awareness Training Vendor/Date')
    
    assess_providers = BooleanField('Assess providers')
    assess_providers_vendor = StringField('Assess Providers Vendor/Date')
    
    annual_wisp_review = BooleanField('Annual WISP review')
    annual_wisp_review_vendor = StringField('Annual WISP Review Vendor/Date')
    
    wisp_developed = BooleanField('Written Information Security Plan developed')
    wisp_developed_vendor = StringField('WISP Development Vendor/Date')
    
    annual_director_reports = BooleanField('Annual director reports')
    annual_director_reports_vendor = StringField('Annual Director Reports Vendor/Date')
    
    annual_disposal_records = BooleanField('Annual disposal of records')
    annual_disposal_vendor = StringField('Annual Disposal Vendor/Date')
    
    restricted_access_data = BooleanField('Restricted access to data')
    restricted_access_vendor = StringField('Restricted Access Vendor/Date')
    
    complex_passwords_required = BooleanField('Require complex passwords')
    complex_passwords_vendor = StringField('Complex Passwords Vendor/Date')
    
    firewall_protection = BooleanField('Firewall')
    firewall_vendor = StringField('Firewall Vendor/Date')
    
    ids_enabled = BooleanField('Intrusion detection systems (IDS)')
    ids_vendor = StringField('IDS Vendor/Date')
    
    segmented_network = BooleanField('Segmented / IOT / Guest network')
    segmented_network_vendor = StringField('Segmented Network Vendor/Date')
    
    endpoint_security = BooleanField('Endpoint security')
    endpoint_security_vendor = StringField('Endpoint Security Vendor/Date')
    
    third_party_patch_mgmt = BooleanField('Third-party patch management')
    third_party_patch_vendor = StringField('Third-party Patch Management Vendor/Date')
    
    windows_patch_mgmt = BooleanField('Windows patch management')
    windows_patch_vendor = StringField('Windows Patch Management Vendor/Date')
    
    # IRS Security Six
    antivirus_solution = StringField('Antivirus solution name/provider')
    endpoint_detection_solution = StringField('Endpoint detection and response solution name/provider')
    intrusion_detection_solution = StringField('Intrusion detection systems solution name/provider')
    backup_solution = StringField('Backup solution name/provider')
    backup_encrypted = BooleanField('Is backup encrypted?')
    firewall_solution = StringField('Firewall solution name/provider')
    encryption_solution = StringField('Drive encryption solution name/provider')
    mfa_solution = StringField('Multifactor authentication solution name/provider')
    vpn_solution = StringField('VPN solution name/provider')
    
    # Password Policy Details
    password_min_length = SelectField('Minimum Password Length', choices=[
        ('8', '8 characters'),
        ('10', '10 characters'),
        ('12', '12 characters'),
        ('16', '16 characters')
    ], default='8')
    password_complexity = BooleanField('Password complexity requirements enabled')
    password_history_enabled = BooleanField('Password history enforced (24 max remembered)')
    password_manager_required = BooleanField('Password manager required for all accounts')
    default_passwords_changed = BooleanField('Default/temporary passwords changed')
    password_secure_storage = BooleanField('Passwords stored in secure location')
    password_manager_mfa = BooleanField('MFA enabled for password manager')
    
    # Wireless Security
    wireless_wpa2_enabled = BooleanField('WPA2/WPA3 encryption enabled')
    wireless_ssid_hidden = BooleanField('Wireless SSID hidden from public view')
    wireless_guest_network = BooleanField('Separate guest wireless network available')
    wireless_admin_password_changed = BooleanField('Default router admin passwords changed')
    wireless_tx_power_reduced = BooleanField('WLAN transmit power reduced to office area only')
    wireless_wep_disabled = BooleanField('WEP encryption disabled (not used)')
    
    # Additional Security Controls
    rmm_solution = StringField('Remote Monitoring and Management (RMM) solution')
    browser_patch_mgmt = BooleanField('Patch management on browsers')
    stored_passwords_disabled = BooleanField('Stored password feature disabled')
    incident_response_printed = BooleanField('Incident response plan printed and readily available')
    security_training_method = StringField('Security awareness training method')
    unnecessary_software_blocked = BooleanField('Installing unnecessary software disallowed')
    device_inventory_performed = BooleanField('Inventory of devices containing client data performed')
    client_data_access_limited = BooleanField('Access to stored client data limited/disabled')
    client_data_protection_solution = StringField('Client data protection solution name/provider')

class VendorsForm(FlaskForm):
    vendor_list = TextAreaField('Third-Party Vendors with Data Access', 
        description='List all vendors, contractors, or service providers who have access to sensitive data')
    vendor_agreements = BooleanField('Do you have written agreements with all vendors regarding data protection?')
    vendor_monitoring = BooleanField('Do you regularly monitor vendor compliance?')

class EmployeeAccessForm(FlaskForm):
    # Basic Employee Access Controls
    access_control = BooleanField('Do you have role-based access controls?')
    employee_training = BooleanField('Do you provide regular security awareness training?')
    training_frequency = SelectField('Training Frequency', choices=[
        ('', 'Select frequency'),
        ('quarterly', 'Quarterly'),
        ('biannual', 'Twice per year'),
        ('annual', 'Annual'),
        ('onboarding', 'New employee onboarding only')
    ])
    security_awareness_method = StringField('Security Awareness Training Method', 
        description='How do you conduct security awareness training?')
    incident_response = BooleanField('Do you have a written incident response plan?')
    background_checks = BooleanField('Do you conduct background checks for employees with data access?')
    
    # Employee Management
    confidentiality_agreements = BooleanField('All employees sign confidentiality agreements')
    employee_access_review = BooleanField('Regular review of employee access rights')
    employee_termination_process = BooleanField('Formal process for revoking access when employees leave')
    remote_work_policy = BooleanField('Written remote work security policy')
    
    # Qualified Individual Information
    qualified_individual_name = StringField('Qualified Individual Name', validators=[DataRequired()],
        description='Person responsible for implementing and supervising the information security program')
    qualified_individual_qualifications = TextAreaField('Qualifications/Experience',
        description='Describe their cybersecurity qualifications and experience')
    qualified_individual_supervisor = StringField('Supervisor',
        description='Who does the Qualified Individual report to?')
    
    # Incident Response Team
    incident_coordinator_name = StringField('Incident Coordinator Name',
        description='Primary person responsible for coordinating incident response')
    incident_coordinator_phone = StringField('Incident Coordinator Phone')
    incident_team_member_1 = StringField('Incident Team Member #1')
    incident_team_member_1_phone = StringField('Team Member #1 Phone')
    incident_team_member_2 = StringField('Incident Team Member #2')
    incident_team_member_2_phone = StringField('Team Member #2 Phone')
    
    # Incident Response Contacts
    tech_company = StringField('IT Support Company Name',
        description='Primary technology support company')
    tech_company_phone = StringField('IT Support Phone Number')
    legal_counsel_name = StringField('Legal Counsel Name')
    legal_counsel_phone = StringField('Legal Counsel Phone')
    insurance_broker = StringField('Insurance Broker/Company')
    insurance_policy = StringField('Insurance Policy Information')
    
    # Testing and Monitoring
    annual_penetration_test = BooleanField('Annual penetration testing conducted')
    vulnerability_assessments = BooleanField('Regular vulnerability assessments')
    system_scans = BooleanField('System-wide security scans every six months')
    security_awareness_testing = BooleanField('Phishing simulation testing for employees')
    
    # EFIN Monitoring (for tax preparers)
    efin_monitoring_process = BooleanField('EFIN monitoring process implemented')
    efin_status_check_frequency = SelectField('EFIN Status Check Frequency', choices=[
        ('', 'Not applicable'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly')
    ])

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
    
    # Generate comprehensive PDF using the Rightworks template
    buffer = generate_complete_rightworks_wisp_pdf(wisp)
    
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