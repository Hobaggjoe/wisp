from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

def generate_comprehensive_wisp_pdf(wisp, wisp_data):
    """Generate a comprehensive WISP PDF document"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=20,
        alignment=1,  # Center alignment
        textColor='#2261AE'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=15,
        alignment=1,
        textColor='#2A4159'
    )
    
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor='#2261AE',
        borderWidth=1,
        borderColor='#2261AE',
        borderPadding=5
    )
    
    subsection_style = ParagraphStyle(
        'SubsectionHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor='#2A4159'
    )
    
    # Document Header
    story.append(Paragraph("Written Information Security Plan", title_style))
    story.append(Paragraph(f"{wisp_data.get('company_name', 'Company Name')}", subtitle_style))
    story.append(Paragraph(f"Created: {wisp.created_at.strftime('%B %d, %Y')} | Last Updated: {wisp.updated_at.strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 30))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", section_style))
    exec_summary = f"""
    This Written Information Security Plan (WISP) has been developed by {wisp_data.get('company_name', 'the Company')} 
    to comply with the requirements set forth in IRS Publication 4557 and the Gramm-Leach-Bliley Act (GLBA). 
    This plan outlines our commitment to protecting customer information and the specific measures we have 
    implemented to safeguard sensitive data.<br/><br/>
    
    As a {wisp_data.get('industry', 'business').lower()} organization with {wisp_data.get('company_size', 'multiple')} employees, 
    we handle {wisp_data.get('personal_info_types', 'personal information').lower()} and are committed to maintaining 
    the highest standards of data protection and privacy.
    """
    story.append(Paragraph(exec_summary, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Company Information
    story.append(Paragraph("Company Information", section_style))
    story.append(Paragraph("Business Details", subsection_style))
    company_info = f"""
    <b>Company Name:</b> {wisp_data.get('company_name', 'N/A')}<br/>
    <b>Industry:</b> {wisp_data.get('industry', 'N/A').title()}<br/>
    <b>Company Size:</b> {wisp_data.get('company_size', 'N/A')}<br/>
    <b>Contact Email:</b> {wisp_data.get('contact_email', 'N/A')}<br/>
    <b>Business Address:</b><br/>
    {wisp_data.get('address', 'Address not provided').replace(chr(10), '<br/>')}
    """
    story.append(Paragraph(company_info, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Administrative Safeguards
    story.append(Paragraph("Administrative Safeguards", section_style))
    
    story.append(Paragraph("Access Control and User Management", subsection_style))
    access_info = f"""
    <b>Role-Based Access Controls:</b> {'Implemented' if wisp_data.get('access_control') else 'Not Implemented'}<br/>
    <b>Background Checks:</b> {'Conducted for data access roles' if wisp_data.get('background_checks') else 'Not conducted'}<br/><br/>
    {'Employees are granted access to sensitive information only on a need-to-know basis according to their job responsibilities. Access rights are reviewed regularly and updated when roles change.' if wisp_data.get('access_control') else 'Access controls should be implemented to restrict data access based on job responsibilities.'}
    """
    story.append(Paragraph(access_info, styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Employee Training Program", subsection_style))
    training_info = f"""
    <b>Security Awareness Training:</b> {'Provided regularly' if wisp_data.get('employee_training') else 'Not provided'}<br/>
    <b>Training Frequency:</b> {wisp_data.get('training_frequency', 'Not specified').title()}<br/><br/>
    {'All employees receive regular training on information security best practices, including password security, phishing awareness, and proper data handling procedures.' if wisp_data.get('employee_training') else 'Security awareness training should be implemented for all employees handling sensitive data.'}
    """
    story.append(Paragraph(training_info, styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Incident Response", subsection_style))
    incident_info = f"""
    <b>Written Incident Response Plan:</b> {'Documented and maintained' if wisp_data.get('incident_response') else 'Not documented'}<br/><br/>
    {'Our incident response plan defines procedures for identifying, containing, and recovering from security incidents, including notification requirements and recovery steps.' if wisp_data.get('incident_response') else 'An incident response plan should be developed to handle security breaches and data incidents.'}
    """
    story.append(Paragraph(incident_info, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Technical Safeguards
    story.append(Paragraph("Technical Safeguards", section_style))
    
    story.append(Paragraph("Authentication and Access Security", subsection_style))
    auth_info = f"""
    <b>Multi-Factor Authentication:</b> {'Enabled' if wisp_data.get('mfa_enabled') else 'Not Enabled'}<br/>
    <b>Password Policy:</b> {'Written policy in place' if wisp_data.get('password_policy') else 'No written policy'}<br/>
    """
    story.append(Paragraph(auth_info, styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Data Encryption", subsection_style))
    encryption_info = f"""
    <b>Encryption at Rest:</b> {'Implemented' if wisp_data.get('data_encryption') else 'Not Implemented'}<br/>
    <b>Encryption in Transit:</b> {'Implemented' if wisp_data.get('transmission_encryption') else 'Not Implemented'}<br/>
    """
    story.append(Paragraph(encryption_info, styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Network and System Protection", subsection_style))
    network_info = f"""
    <b>Firewall Protection:</b> {'Active' if wisp_data.get('firewall_protection') else 'Not Active'}<br/>
    <b>Antivirus Software:</b> {'Installed and updated' if wisp_data.get('antivirus_software') else 'Not installed'}<br/>
    <b>Security Updates:</b> {'Regular updates applied' if wisp_data.get('security_updates') else 'Not regularly applied'}<br/>
    """
    story.append(Paragraph(network_info, styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Data Backup and Recovery", subsection_style))
    backup_info = f"""
    <b>Regular Data Backups:</b> {'Implemented' if wisp_data.get('regular_backups') else 'Not Implemented'}<br/>
    {'Regular backups ensure business continuity and data availability in the event of system failures or security incidents.' if wisp_data.get('regular_backups') else 'Data backup procedures should be implemented for business continuity.'}
    """
    story.append(Paragraph(backup_info, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Physical Safeguards
    story.append(Paragraph("Physical Safeguards", section_style))
    physical_info = """
    Physical access to areas containing sensitive information is restricted to authorized personnel only. 
    This includes computer workstations, file cabinets, and any physical storage containing customer data.<br/><br/>
    
    <b>Physical Security Measures:</b><br/>
    • Office doors are locked when unattended<br/>
    • Computer screens are locked when away from desk<br/>
    • Sensitive documents are stored in locked cabinets<br/>
    • Clean desk policy is enforced<br/>
    • Visitor access is monitored and logged
    """
    story.append(Paragraph(physical_info, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Information Collected and Stored
    story.append(Paragraph("Information Collected and Stored", section_style))
    
    story.append(Paragraph("Data Types", subsection_style))
    data_info = f"""
    <b>Personal Information Types:</b> {wisp_data.get('personal_info_types', 'Not specified').title()}<br/>
    <b>Data Retention Period:</b> {wisp_data.get('data_retention', 'Not specified').title()}<br/>
    """
    if wisp_data.get('data_sources'):
        data_info += f"<br/><b>Data Collection Sources:</b><br/>{wisp_data.get('data_sources').replace(chr(10), '<br/>')}<br/>"
    story.append(Paragraph(data_info, styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Data Destruction", subsection_style))
    destruction_info = f"""
    <b>Data Destruction Process:</b> {'Documented process in place' if wisp_data.get('data_destruction') else 'No formal process documented'}<br/>
    {'When personal information is no longer needed for business purposes or legal requirements, it is securely destroyed using methods appropriate to the storage medium.' if wisp_data.get('data_destruction') else 'A data destruction policy should be implemented for secure disposal of sensitive information.'}
    """
    story.append(Paragraph(destruction_info, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Systems and Software
    story.append(Paragraph("Systems and Software", section_style))
    story.append(Paragraph("Business Systems in Use", subsection_style))
    
    systems_used = []
    system_checks = [
        ('QuickBooks', wisp_data.get('quickbooks')),
        ('ADP Payroll', wisp_data.get('adp')),
        ('Workday', wisp_data.get('workday')),
        ('Salesforce', wisp_data.get('salesforce')),
        ('Microsoft 365', wisp_data.get('office365')),
        ('Google Workspace', wisp_data.get('google_workspace'))
    ]
    
    for system, enabled in system_checks:
        if enabled:
            systems_used.append(f"• {system}")
    
    systems_text = "<br/>".join(systems_used) if systems_used else "No standard business systems specified"
    
    if wisp_data.get('custom_software'):
        systems_text += f"<br/><br/><b>Additional Systems:</b><br/>{wisp_data.get('custom_software').replace(chr(10), '<br/>')}"
    
    story.append(Paragraph(systems_text, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Third-Party Vendors
    story.append(Paragraph("Third-Party Vendors and Service Providers", section_style))
    
    if wisp_data.get('vendor_list'):
        story.append(Paragraph("Vendors with Data Access", subsection_style))
        vendor_text = wisp_data.get('vendor_list').replace(chr(10), '<br/>')
        story.append(Paragraph(vendor_text, styles['Normal']))
        story.append(Spacer(1, 10))
    
    story.append(Paragraph("Vendor Management", subsection_style))
    vendor_mgmt = f"""
    <b>Written Vendor Agreements:</b> {'In place for all vendors' if wisp_data.get('vendor_agreements') else 'Not in place'}<br/>
    <b>Vendor Compliance Monitoring:</b> {'Regular monitoring conducted' if wisp_data.get('vendor_monitoring') else 'Not regularly monitored'}
    """
    story.append(Paragraph(vendor_mgmt, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Risk Assessment and Review
    story.append(Paragraph("Risk Assessment and Annual Review", section_style))
    story.append(Paragraph("Ongoing Risk Management", subsection_style))
    
    risk_text = f"""
    This WISP is reviewed annually to ensure continued effectiveness and compliance with applicable regulations. 
    The review process includes:<br/><br/>
    
    • Assessment of current security controls and their effectiveness<br/>
    • Identification of new threats and vulnerabilities<br/>
    • Review of any security incidents that occurred during the year<br/>
    • Evaluation of changes in business operations or technology<br/>
    • Updates to policies and procedures as needed<br/>
    • Employee training program effectiveness review<br/><br/>
    
    <b>Next Review Date:</b> {(wisp.created_at.replace(year=wisp.created_at.year + 1)).strftime('%B %d, %Y')}
    """
    story.append(Paragraph(risk_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Document Footer
    story.append(PageBreak())
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        alignment=1,
        fontSize=10,
        textColor='#666666'
    )
    story.append(Paragraph(f"This Written Information Security Plan was created on {wisp.created_at.strftime('%B %d, %Y')}", footer_style))
    story.append(Paragraph("Generated using WISP Generator - Ensuring IRS Publication 4557 and GLBA Compliance", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    
    return buffer