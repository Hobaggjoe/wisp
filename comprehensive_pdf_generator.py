from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import io
from datetime import datetime

def draw_footer(canvas_obj, doc):
    """Draw footer on each page"""
    canvas_obj.saveState()
    # Footer text
    footer_text = "Alpharetta, GA | Bloomington, IN | Nashua, NH | rightworks.com | 866.923.6874"
    # Position footer at bottom of page
    canvas_obj.setFont('Helvetica', 9)
    canvas_obj.setFillColor(colors.Color(0.165, 0.255, 0.349))  # Rightworks dark blue
    # Center the footer text
    page_width = letter[0]
    text_width = canvas_obj.stringWidth(footer_text, 'Helvetica', 9)
    x_position = (page_width - text_width) / 2
    y_position = 0.5 * inch  # 0.5 inch from bottom
    canvas_obj.drawString(x_position, y_position, footer_text)
    canvas_obj.restoreState()

def generate_complete_rightworks_wisp_pdf(wisp):
    """Generate a complete Rightworks-style WISP PDF document"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        topMargin=0.75*inch, 
        bottomMargin=1.0*inch,  # More space for footer
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    # Get the data
    data = wisp.get_data()
    
    # Helper function to safely get string values
    def safe_get(key, default='Not specified'):
        """Safely get a value from data, ensuring it's a string"""
        value = data.get(key, default)
        return str(value) if value is not None else default
    
    company_name = safe_get('company_name', 'Company Name')
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles matching Rightworks template
    main_title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.Color(0.133, 0.380, 0.682),  # Rightworks blue
        fontName='Helvetica-Bold'
    )
    
    wisp_accent_style = ParagraphStyle(
        'WISPAccent',
        parent=styles['Normal'],
        fontSize=14,
        spaceBefore=5,
        spaceAfter=15,
        alignment=TA_CENTER,
        textColor=colors.Color(0.133, 0.380, 0.682),
        fontName='Helvetica-Bold'
    )
    
    prepared_for_style = ParagraphStyle(
        'PreparedFor',
        parent=styles['Normal'],
        fontSize=12,
        spaceBefore=20,
        spaceAfter=5,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    company_info_style = ParagraphStyle(
        'CompanyInfo',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=2,
        spaceAfter=2,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=15,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.Color(0.133, 0.380, 0.682),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=6,
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )
    
    footer_bar_style = ParagraphStyle(
        'FooterBar',
        parent=styles['Normal'],
        fontSize=8,
        spaceBefore=20,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.white,
        backColor=colors.Color(0.133, 0.380, 0.682),
        fontName='Helvetica'
    )
    
    story = []
    
    # Title Page
    story.append(Paragraph("Written<br/>Information<br/>Security Plan<br/>(WISP)", main_title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("PREPARED FOR", prepared_for_style))
    story.append(Paragraph(company_name, company_info_style))
    
    # Company address and contact info
    address_parts = []
    if data.get('street_address'):
        address_parts.append(data.get('street_address'))
    if data.get('city') and data.get('state'):
        city_state = f"{data.get('city')}, {data.get('state')}"
        if data.get('zip_code'):
            city_state += f" {data.get('zip_code')}"
        address_parts.append(city_state)
    if data.get('contact_email'):
        address_parts.append(data.get('contact_email'))
    
    for part in address_parts:
        story.append(Paragraph(part, company_info_style))
    
    story.append(Spacer(1, 10))
    
    # Prepared by and dates
    if data.get('prepared_by'):
        story.append(Paragraph(f"Prepared by: {data.get('prepared_by')}", date_style))
    
    story.append(Paragraph(f"Created on: {datetime.now().strftime('%B %d, %Y')}", date_style))
    
    if data.get('annual_review_date'):
        review_date = data.get('annual_review_date')
        if hasattr(review_date, 'strftime'):
            review_date_str = review_date.strftime('%B %d, %Y')
        else:
            review_date_str = str(review_date)
        story.append(Paragraph(f"Annual Review Date: {review_date_str}", date_style))
    
    # Footer will be automatically added to every page
    
    story.append(PageBreak())
    
    # I. OBJECTIVE
    story.append(Paragraph("I. OBJECTIVE", section_title_style))
    objective_text = f"""The objective of {company_name}'s (the "Company") WISP is to support and document the implementation 
    and maintenance of necessary protective measures the Company has selected to protect the personally 
    identifiable information (PII) and other sensitive customer data it collects, creates, uses and maintains. This 
    WISP has been prepared in line with the requirements and guidelines of the IRS, the Gramm-Leach-Bliley Act 
    (GLBA), and the FTC Safeguards Rule. This document will also act as the comprehensive record of all internal 
    policies and processes designed to secure information of Company's customers."""
    story.append(Paragraph(objective_text, body_style))
    story.append(Spacer(1, 15))
    
    # II. PURPOSE
    story.append(Paragraph("II. PURPOSE", section_title_style))
    purpose_items = [
        "Ensure the proper security and confidentiality of PII and other sensitive customer information collected, created and maintained.",
        "Comply with applicable data security laws; including IRS Publication 4557, 5708 and the FTC Safeguards Rule.",
        "Document and show auditors/ data safeguards and policies.",
        f"Define an information security program that is appropriate to the Company's size, business and resources, and the amount of PII and other sensitive information maintained by the Company.",
        "Protect clients from unauthorized access."
    ]
    
    for item in purpose_items:
        story.append(Paragraph(f"• {item}", body_style))
    story.append(Spacer(1, 15))
    
    # III. SCOPE
    story.append(Paragraph("III. SCOPE", section_title_style))
    scope_items = [
        "Applies to all employees, contractors, officers and directors of the Company.",
        "Applies to any PII storage locations or records.",
        "Applies to security of PII and sensitive information of both the company and its clients.",
        "Cataloging existing preventive strategies against data breaches.",
        "Ongoing evaluation and review of the efficacy of the established protective measures.",
        "For the purposes of this WISP, PII includes any of the following items to the extent it could be used, alone or in combination with other information, to identify a specific natural person or individual household:"
    ]
    
    for item in scope_items:
        story.append(Paragraph(f"• {item}", body_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("PII includes", section_title_style))
    
    # PII list
    pii_items = [
        "First and last name combination",
        "Personal phone number", 
        "Purchase history",
        "Bank account information",
        "Credit card numbers",
        "CRM data",
        "Tax prep software data",
        "Driver's license information",
        "Social security number",
        "Date of birth",
        "Employment history",
        "Previous tax returns",
        "Financial statements",
        "Private email addresses"
    ]
    
    for item in pii_items:
        story.append(Paragraph(f"• {item}", body_style))
    
    story.append(PageBreak())
    
    # FTC Checklist Table
    story.append(Paragraph("Checklist: Required FTC Software and Policies", section_title_style))
    
    # Create FTC checklist data
    ftc_data = [
        ['Description', 'Citation', 'In place', 'Not in place', 'Vendor/Date']
    ]
    
    # Add FTC checklist items based on form data
    ftc_items = [
        ['Designate a qualified individual', '16 CFR 314.4 (a)', data.get('qualified_individual_designated', False), data.get('qualified_individual_vendor', '')],
        ['Conduct risk assessment', '16 CFR 314.4 (a)', data.get('risk_assessment_conducted', False), data.get('risk_assessment_vendor', '')],
        ['Encryption at rest', '16 CFR 314.4 (c) (3)', data.get('encryption_at_rest', False), data.get('encryption_at_rest_vendor', '')],
        ['Encryption in transit', '16 CFR 314.4 (c) (3)', data.get('encryption_in_transit', False), data.get('encryption_in_transit_vendor', '')],
        ['Multifactor authentication', '16 CFR 314.4 (c) (5)', data.get('mfa_enabled', False), data.get('mfa_vendor', '')],
        ['Continuous monitoring with IDS/RMM or network scan and penetration testing', '16 CFR 314.4 (d) (2)', data.get('continuous_monitoring', False), data.get('continuous_monitoring_vendor', '')],
        ['Security awareness training', '16 CFR 314.4 (e)', data.get('security_awareness_training', False), data.get('security_awareness_vendor', '')],
        ['Assess providers', '16 CFR 314.4 (f)', data.get('assess_providers', False), data.get('assess_providers_vendor', '')],
        ['Annual WISP review', '16 CFR 314.4 (g)', data.get('annual_wisp_review', False), data.get('annual_wisp_review_vendor', '')],
        ['Develop a Written Information Security Plan', '16 CFR 314.4 (h)', data.get('wisp_developed', False), data.get('wisp_developed_vendor', '')],
        ['Annual director reports', '16 CFR 314.4 (h)', data.get('annual_director_reports', False), data.get('annual_director_reports_vendor', '')],
        ['Annual disposal of records', 'FTC SWS (1)', data.get('annual_disposal_records', False), data.get('annual_disposal_vendor', '')],
        ['Restricted access to data', 'FTC SWS (2)', data.get('restricted_access_data', False), data.get('restricted_access_vendor', '')],
        ['Require complex passwords', 'FTC SWS (3)', data.get('complex_passwords_required', False), data.get('complex_passwords_vendor', '')],
        ['Firewall', 'FTC SWS (5)', data.get('firewall_protection', False), data.get('firewall_vendor', '')],
        ['Intrusion detection systems (IDS)', 'FTC SWS (5)', data.get('ids_enabled', False), data.get('ids_vendor', '')],
        ['Segmented / IOT / Guest network', 'FTC SWS (5)', data.get('segmented_network', False), data.get('segmented_network_vendor', '')],
        ['Endpoint security', 'FTC SWS (6)', data.get('endpoint_security', False), data.get('endpoint_security_vendor', '')],
        ['Third-party patch management', 'FTC SWS (6)', data.get('third_party_patch_mgmt', False), data.get('third_party_patch_vendor', '')],
        ['Windows patch management', 'FTC SWS (6)', data.get('windows_patch_mgmt', False), data.get('windows_patch_vendor', '')]
    ]
    
    for item in ftc_items:
        description = item[0]
        citation = item[1]
        in_place = "✓" if item[2] else ""
        not_in_place = "" if item[2] else "✓"
        vendor_date = item[3]
        
        # Wrap description text for table cell
        desc_para = Paragraph(description, ParagraphStyle('CellText', parent=body_style, fontSize=8, leading=10))
        
        ftc_data.append([desc_para, citation, in_place, not_in_place, vendor_date])
    
    # Create table with proper column widths
    col_widths = [2.2*inch, 1.2*inch, 0.8*inch, 0.8*inch, 1.4*inch]
    ftc_table = Table(ftc_data, colWidths=col_widths, repeatRows=1)
    
    # Table styling
    ftc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.133, 0.380, 0.682)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (3, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),
    ]))
    
    story.append(ftc_table)
    story.append(PageBreak())
    
    # IRS Security Six
    story.append(Paragraph("Checklist: IRS \"Security Six\"", section_title_style))
    
    # Create Security Six section
    security_six_items = [
        ["Use an antivirus", "Antivirus installed:", data.get('antivirus_solution', '')],
        ["Use backup software/services", "Backup:", data.get('backup_solution', '')],
        ["", "Is it encrypted?", "Yes" if data.get('backup_encrypted') else "No"],
        ["Use a firewall", "Firewall:", data.get('firewall_solution', '')],
        ["Use drive encryption", "Encryption through:", data.get('encryption_solution', '')],
        ["Multifactor authentication", "Accessing customer data:", data.get('mfa_solution', '')],
        ["Create and secure virtual private networks", "VPN:", data.get('vpn_solution', '')]
    ]
    
    for item in security_six_items:
        if item[0]:  # Only show the main category if it exists
            story.append(Paragraph(f"<b>{item[0]}</b>", body_style))
        story.append(Paragraph(f"{item[1]} {item[2]}", body_style))
        story.append(Spacer(1, 5))
    
    # Additional IRS items
    story.append(Paragraph("Endpoint detection and response: " + safe_get('endpoint_detection_solution', 'Solution name/provider'), body_style))
    story.append(Paragraph("Intrusion detection systems: " + safe_get('intrusion_detection_solution', 'Solution name/provider'), body_style))
    
    story.append(PageBreak())
    
    # Password Policy Section
    story.append(Paragraph("IRS Publication 4557: Safeguarding Taxpayer Data", section_title_style))
    story.append(Paragraph("Create strong passwords", ParagraphStyle('SubSection', parent=section_title_style, fontSize=12)))
    
    password_items = [
        f"Minimum of {data.get('password_min_length', '8')} characters",
        f"Password must meet complexity requirements: {'Enabled' if data.get('password_complexity') else 'Disabled'}",
        f"Enforce password history: 24 (max) passwords remembered - {'Enabled' if data.get('password_history_enabled') else 'Disabled'}",
        "Avoid personal information use phrases instead",
        f"Change default/temporary passwords that come with accounts including printers - {'Yes' if data.get('default_passwords_changed') else 'No'}",
        f"Store passwords in a secure location like a safe or locked file cabinet - {'Yes' if data.get('password_secure_storage') else 'No'}",
        f"Use MFA for password manager - {'Yes' if data.get('password_manager_mfa') else 'No'}"
    ]
    
    for item in password_items:
        story.append(Paragraph(item, body_style))
    
    story.append(Spacer(1, 15))
    
    # Wireless Security Section
    story.append(Paragraph("Secure wireless networks", ParagraphStyle('SubSection', parent=section_title_style, fontSize=12)))
    
    wireless_items = [
        f"Default login on router? {'Changed' if data.get('wireless_admin_password_changed') else 'Not changed'}",
        f"Turn off public SSID - {'Yes' if data.get('wireless_ssid_hidden') else 'No'}",
        f"Change guest wireless network to unidentifiable name - {'Yes' if data.get('wireless_guest_network') else 'No'}",
        f"Reduce WLAN Transmit power (TX) range to not work outside of office if needed - {'Yes' if data.get('wireless_tx_power_reduced') else 'No'}",
        f"WPA2 and AES Encryption enabled - {'Yes' if data.get('wireless_wpa2_enabled') else 'No'}",
        f"Do not use WEP - {'WEP Disabled' if data.get('wireless_wep_disabled') else 'Check WEP status'}"
    ]
    
    for item in wireless_items:
        story.append(Paragraph(item, body_style))
    
    story.append(PageBreak())
    
    # Continue with more sections...
    # PII Inventory List
    story.append(Paragraph("PII inventory list", section_title_style))
    story.append(Paragraph("List anywhere that contains PII. Examples include but are not limited to:", body_style))
    story.append(Spacer(1, 10))
    
    # Third-party apps
    story.append(Paragraph("1. Third-party apps", body_style))
    apps = [data.get('third_party_apps_1', ''), data.get('third_party_apps_2', '')]
    for i, app in enumerate(apps, 1):
        if app:
            story.append(Paragraph(f"   {chr(96+i)}. {app}", body_style))
        else:
            story.append(Paragraph(f"   {chr(96+i)}. __________________________________________________", body_style))
    
    # Cloud providers
    story.append(Paragraph("2. Cloud provider(s)", body_style))
    clouds = [data.get('cloud_providers_1', ''), data.get('cloud_providers_2', '')]
    for i, cloud in enumerate(clouds, 1):
        if cloud:
            story.append(Paragraph(f"   {chr(96+i)}. {cloud}", body_style))
        else:
            story.append(Paragraph(f"   {chr(96+i)}. __________________________________________________", body_style))
    
    # Data storage
    story.append(Paragraph("3. Data storage(s)", body_style))
    storages = [data.get('data_storage_1', ''), data.get('data_storage_2', '')]
    for i, storage in enumerate(storages, 1):
        if storage:
            story.append(Paragraph(f"   {chr(96+i)}. {storage}", body_style))
        else:
            story.append(Paragraph(f"   {chr(96+i)}. __________________________________________________", body_style))
    
    # Email providers
    story.append(Paragraph("4. Email provider(s)", body_style))
    emails = [data.get('email_providers_1', ''), data.get('email_providers_2', '')]
    for i, email in enumerate(emails, 1):
        if email:
            story.append(Paragraph(f"   {chr(96+i)}. {email}", body_style))
        else:
            story.append(Paragraph(f"   {chr(96+i)}. __________________________________________________", body_style))
    
    # CRM systems
    story.append(Paragraph("5. CRM(s)", body_style))
    crms = [data.get('crm_systems_1', ''), data.get('crm_systems_2', '')]
    for i, crm in enumerate(crms, 1):
        if crm:
            story.append(Paragraph(f"   {chr(96+i)}. {crm}", body_style))
        else:
            story.append(Paragraph(f"   {chr(96+i)}. __________________________________________________", body_style))
    
    # Social media contractors
    story.append(Paragraph("6. Social media contractor(s)", body_style))
    socials = [data.get('social_media_contractors_1', ''), data.get('social_media_contractors_2', '')]
    for i, social in enumerate(socials, 1):
        if social:
            story.append(Paragraph(f"   {chr(96+i)}. {social}", body_style))
        else:
            story.append(Paragraph(f"   {chr(96+i)}. __________________________________________________", body_style))
    
    story.append(PageBreak())
    
    # Qualified Individual Section
    story.append(Paragraph("Qualified Individual implementing and supervising the information security program", section_title_style))
    
    qi_name = data.get('qualified_individual_name', '__________________________________________')
    qi_qualifications = data.get('qualified_individual_qualifications', '__________________________________________')
    qi_supervisor = data.get('qualified_individual_supervisor', '__________________________________________')
    
    story.append(Paragraph(f"Qualified Individual: {qi_name}", body_style))
    story.append(Paragraph(f"Qualifications/experience: {qi_qualifications}", body_style))
    story.append(Paragraph(f"Supervisor: {qi_supervisor}", body_style))
    story.append(Spacer(1, 10))
    
    qi_text = f"""Company's Qualified Individual shall report in writing to the Company's [Board of Directors] [senior management] 
    and such report shall include an overall assessment of Company's compliance with the information 
    security program and provide specific reporting on the elements provided in this Written Information Security 
    Plan, as well as security events and how management responded, and recommendations for changes in the 
    information security program."""
    
    story.append(Paragraph(qi_text, body_style))
    story.append(Spacer(1, 15))
    
    # Additional comprehensive sections would continue here...
    # Risk assessment, Security program safeguards, Incident response, etc.
    
    # Footer will be automatically added to every page
    
    # Build the PDF with footer on every page
    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    buffer.seek(0)
    return buffer