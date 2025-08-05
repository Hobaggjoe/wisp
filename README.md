# WISP IRS Generator

A TurboTax-style web application that guides users through generating an IRS-compliant Written Information Security Plan (WISP). Built with Python Flask and designed with inspiration from Rightworks.com.

## 🎯 What is This App?

The WISP IRS Generator is a comprehensive web application that helps businesses create professional, IRS-compliant Written Information Security Plans (WISPs) through an intuitive, multi-step wizard interface. The app generates professionally formatted PDF documents that comply with IRS Publication 4557 and GLBA requirements.

## ✨ Features

### 📋 Multi-Step Onboarding Wizard
- **Step 1: Company Information** - Company details, contact info, EIN/EFIN numbers
- **Step 2: Data Collection Practices** - PII inventory and data sources
- **Step 3: Systems Used** - QuickBooks, ADP, Workday, and other business systems
- **Step 4: Security Controls** - FTC checklist, IRS Security Six, password policies
- **Step 5: Vendors & Access** - Third-party vendors with data access
- **Step 6: Employee Access & Training** - Roles, policies, incident response team

### 📄 Professional WISP Output
- **Real-time Preview** - View your WISP as you build it
- **PDF Export** - Generate professional, branded PDF documents
- **IRS Compliance** - Meets IRS Pub 4557 and GLBA requirements
- **Rightworks Branding** - Professional footer on every page

### 🎛️ Dashboard Management
- **WISP Library** - List and manage all saved WISPs
- **Edit/Update** - Modify existing WISPs
- **Download/Share** - Export and distribute completed WISPs
- **Annual Review Reminders** - Track when WISPs need updating

### 🎨 Professional Design
- **Rightworks Color Scheme** - Primary blue (#2261AE), slate gray (#2A4159), teal accent (#00B2A9)
- **Modern UI** - Soft drop shadows, rounded corners, card-based layout
- **Responsive Design** - Works on desktop and mobile devices

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, Tailwind CSS
- **Database**: SQLite with Flask-SQLAlchemy
- **Forms**: Flask-WTF and WTForms
- **PDF Generation**: ReportLab
- **Session Management**: Flask sessions

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hobaggjoe/wisp.git
   cd wisp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the app**
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

### Dependencies

The application requires the following Python packages (automatically installed with `requirements.txt`):

```
Flask==2.3.3
Flask-WTF==1.2.1
WTForms==3.1.0
Flask-SQLAlchemy==3.1.1
reportlab==4.0.4
Jinja2==3.1.2
python-dotenv==1.0.0
email_validator==2.2.0
```

## 🚀 Usage

### Creating Your First WISP

1. **Start the Wizard** - Click "Start Creating Your WISP" on the homepage
2. **Complete All Steps** - Fill out the 6-step wizard with your company information
3. **Review & Generate** - Preview your WISP and generate the PDF
4. **Download** - Save your professional WISP document

### Key Sections Included in Generated WISPs

- **Administrative Safeguards** - Company policies and procedures
- **Physical Safeguards** - Physical security measures
- **Technical Safeguards** - IT security controls and systems
- **Risk Assessment Summary** - Security risk evaluation
- **Incident Response Plan** - Data breach response procedures
- **Data Retention Policy** - Information lifecycle management
- **Annual Review Process** - Ongoing compliance maintenance

### Compliance Standards

The generated WISPs comply with:
- **IRS Publication 4557** - Safeguarding Taxpayer Data
- **Gramm-Leach-Bliley Act (GLBA)** - Financial privacy requirements
- **FTC Safeguards Rule** - Enhanced data security standards

## 🏗️ Project Structure

```
wisp/
├── app.py                          # Main Flask application
├── comprehensive_pdf_generator.py   # PDF generation logic
├── requirements.txt                # Python dependencies
├── wisp.db                        # SQLite database (auto-created)
├── templates/                     # Jinja2 HTML templates
│   ├── base.html                 # Base template
│   ├── index.html                # Homepage
│   ├── dashboard.html            # WISP management dashboard
│   ├── wizard/                   # Multi-step wizard templates
│   │   ├── step_1.html          # Company information
│   │   ├── step_2.html          # Data collection
│   │   ├── step_3.html          # Systems
│   │   ├── step_4.html          # Security controls
│   │   ├── step_5.html          # Vendors
│   │   ├── step_6.html          # Employee access
│   │   └── complete.html        # Completion page
│   └── wisp/
│       └── view.html            # WISP preview page
```

## 🔧 Configuration

The app uses Flask's development server by default. For production deployment:

1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Configure environment variables for security keys
4. Use a production database (PostgreSQL, MySQL)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Hobaggjoe/wisp/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🎉 Acknowledgments

- Built for IRS compliance and professional tax preparation firms
- Tailwind CSS for responsive design
- ReportLab for professional PDF generation

---

**Start creating professional, IRS-compliant WISPs today!** 🚀
