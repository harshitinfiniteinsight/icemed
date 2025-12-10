# ICE Charge Import & Reconciliation System

A fully functional web-based system for automating the reconciliation of ICE medical billing encounters with mock EBS (Electronic Billing System) integration.

## 🌟 Features

### Core Functionality
- **File Upload**: Upload Excel files or select from sample files
- **Instant Preview**: See raw data immediately when selecting a sample file
- **Mock EBS Processing**: Simulates billing evaluation with business rules
- **Automated Reconciliation**: Generates two output Excel files:
  - **General Reconciliation**: Complete billing status for all encounters (Data + Summary sheets)
  - **Master Missing**: Historical ledger of unbillable encounters (cumulative tracking)

### User Experience
- ✅ Modern, responsive web interface
- ✅ Instant data preview before processing
- ✅ Real-time processing status
- ✅ Color-coded results (green = billed, pink = not billed)
- ✅ Inline results display (no page redirects)
- ✅ Summary statistics and insights
- ✅ One-click Excel file downloads

### Technical Features
- ✅ SHA-256 encounter key generation for unique identification
- ✅ Persistent Master Missing file across multiple runs
- ✅ Business rules simulation (missing DX, CPT, provider validation)
- ✅ Support for multiple service dates in single file
- ✅ Handles large files (150+ encounters)

---

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Application**
```bash
python run.py
```

3. **Open Browser**
```
http://localhost:5001
```

### Vercel Deployment

1. **Install Vercel CLI** (if not already installed)
```bash
npm install -g vercel
```

2. **Deploy**
```bash
vercel
```

3. **Follow Prompts**
- Link to existing project or create new
- Configure as needed
- Deploy!

---

## 📁 Project Structure

```
ice-reconciliation-mock/
├── api/
│   └── index.py                 # Vercel serverless entry point
├── web/
│   ├── app.py                   # Flask application
│   ├── templates/
│   │   ├── index.html          # Main upload page
│   │   └── results.html        # Results display (legacy)
│   └── static/
│       ├── css/
│       │   └── style.css       # Styling
│       └── js/
│           └── app.js          # Frontend logic
├── src/
│   ├── models.py               # Data models
│   ├── file_parser.py          # Excel file parsing
│   ├── mock_ebs.py             # Mock billing system
│   ├── encounter_key.py        # Key generation
│   ├── reconciliation_generator.py  # Output file generation
│   ├── master_missing_manager.py    # Historical tracking
│   └── orchestrator.py         # Workflow coordinator
├── data/
│   ├── input/                  # Sample Excel files
│   └── output/                 # Generated files
├── config.json                 # Configuration
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel configuration
└── run.py                      # Local development entry point
```

---

## 🎯 How to Use

### Option 1: Upload Your File
1. Click "Choose File"
2. Select an Excel file (`.xlsx`)
3. Click "Process File"
4. View results and download files

### Option 2: Select Sample File (Recommended for Testing)
1. **Select a sample file from dropdown**
   - sample_complete.xlsx (20 encounters, all valid)
   - sample_missing_dx.xlsx (15 encounters, 10 missing DX)
   - sample_missing_cpt.xlsx (15 encounters, 8 missing CPT)
   - sample_mixed.xlsx (25 encounters, various scenarios)
   - sample_multiple_dates.xlsx (30 encounters, 3 dates)
   - sample_large.xlsx (150 encounters)
2. **Preview appears instantly** showing first 20 rows
3. Review the raw data
4. Click "Process Sample"
5. View processed results with:
   - Summary statistics
   - Master Missing updates
   - Color-coded data table
   - Download buttons

---

## 📊 Output Files

### General Reconciliation (MM-dd-yyyy).xlsx

**Sheet 1: Data**
- All original input columns
- `Billed` column: "Yes" or "No"
- `Reason for not billed` column: Error description (if applicable)

**Sheet 2: Summary**
- Aggregated by Date of Service, Facility, Provider, Type of Care
- `PRM Billing`: Count of billed encounters
- `CPTs`: Count of CPT codes billed

### Master Missing to (MM-dd-yyyy).xlsx

**Sheet: Data**
- Historical ledger of all unbillable encounters
- Cumulative across multiple runs
- Updates when encounters become billable
- Tracks last attempt to process

---

## 🧪 Sample Files Included

1. **sample_complete.xlsx**: All complete encounters (100% success rate)
2. **sample_missing_dx.xlsx**: Missing diagnosis codes
3. **sample_missing_cpt.xlsx**: Missing CPT codes
4. **sample_mixed.xlsx**: Various scenarios (48% success rate)
5. **sample_multiple_dates.xlsx**: Encounters from multiple dates
6. **sample_large.xlsx**: Large file with 150 encounters

---

## 🔧 Configuration

Edit `config.json` to customize:

```json
{
  "input": {
    "folderPath": "data/input",
    "sheetName": "Sheet1"
  },
  "output": {
    "folderPath": "data/output",
    "dateFormat": "MM-dd-yyyy"
  },
  "masterMissing": {
    "folderPath": "data/output",
    "fileNamePattern": "Master Missing to {date}.xlsx"
  },
  "logging": {
    "level": "INFO",
    "filePath": "logs"
  }
}
```

---

## 🏗️ Architecture

### Backend (Python/Flask)
- **Flask**: Web framework
- **openpyxl**: Excel file manipulation
- **python-dateutil**: Date parsing
- **werkzeug**: File uploads

### Frontend
- **HTML5**: Structure
- **CSS3**: Modern gradient design
- **Vanilla JavaScript**: Dynamic interactions
- **Fetch API**: AJAX requests

### Processing Pipeline
1. File Upload/Selection
2. Excel Parsing (openpyxl)
3. Mock EBS Evaluation (business rules)
4. General Reconciliation Generation
5. Master Missing Update
6. Results Display with Preview Data

---

## 🔐 Security Notes

- Files may contain PHI (Protected Health Information)
- Store in secure, approved locations
- Apply appropriate access controls
- Use HTTPS in production
- Implement authentication before production deployment

---

## 🚀 Production Deployment

### Environment Variables (Vercel)

Set these in your Vercel dashboard:

```bash
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key-here
```

### Before Production:

1. ✅ Replace Mock EBS with real EBS integration
2. ✅ Add user authentication (Flask-Login, OAuth)
3. ✅ Implement database (PostgreSQL, MongoDB)
4. ✅ Add email notifications
5. ✅ Setup monitoring (Sentry, LogDNA)
6. ✅ Configure automated backups
7. ✅ Add rate limiting
8. ✅ Implement audit logging

---

## 📝 API Endpoints

### GET /
Main upload page

### GET /api/sample-files
List available sample files

### POST /api/preview-sample
Preview raw data from sample file
```json
{
  "sample_name": "sample_mixed.xlsx"
}
```

### POST /api/upload
Upload and process user file

### POST /api/process-sample
Process selected sample file
```json
{
  "sample_name": "sample_mixed.xlsx"
}
```

### GET /api/results/:job_id
Get processing results

### GET /api/download/:file_type
Download generated file (reconciliation or master_missing)

### GET /api/download-by-job/:job_id/:file_type
Download file by specific job ID

---

## 🎨 UI Features

- **Gradient Design**: Modern blue-purple gradient header
- **Responsive Layout**: Works on desktop, tablet, mobile
- **Color-Coded Tables**: 
  - Green rows: Successfully billed
  - Pink rows: Not billed (with reason)
- **Badge Indicators**: Visual status (✓ Success / ✗ Failed)
- **Progress Bars**: Real-time processing status
- **Statistics Cards**: Key metrics at a glance
- **Smooth Animations**: Professional transitions

---

## 🧪 Testing

### Backend Test
```bash
python test_backend.py
```

### Manual Testing
1. Select each sample file
2. Verify preview appears
3. Process each file
4. Download both output files
5. Verify Excel file contents
6. Run multiple times to test Master Missing accumulation

---

## 📚 Documentation

- `IMPLEMENTATION_COMPLETE.md`: Full implementation details
- `WORKING_STATUS.md`: Current working status
- `PREVIEW_FEATURE_COMPLETE.md`: Preview feature documentation
- `FINAL_COMPLETE_STATUS.md`: Complete feature checklist

---

## 🤝 Contributing

This is a prototype/mock system. For production use:
1. Fork the repository
2. Implement real EBS integration
3. Add authentication
4. Add tests
5. Submit pull request

---

## 📄 License

Proprietary - PRM Healthcare Billing

---

## 👥 Authors

- **Development Team**: PRM Development
- **Client**: Intensive Care Experts (ICE)
- **Project**: ICE Charge Import & Reconciliation Automation

---

## 🆘 Support

For issues or questions:
1. Check documentation files
2. Review sample files for examples
3. Contact development team

---

## ✅ Status

**Current Version**: 1.0.0 (Prototype)  
**Status**: ✅ Fully Functional  
**Last Updated**: December 10, 2025

### Working Features:
- ✅ File upload and processing
- ✅ Sample file selection
- ✅ Instant data preview
- ✅ Mock EBS simulation
- ✅ Output file generation
- ✅ Master Missing tracking
- ✅ Results display
- ✅ File downloads
- ✅ Color-coded interface
- ✅ Responsive design

---

## 🎉 Demo

Visit the live demo: [Your Vercel URL here after deployment]

Or run locally:
```bash
python run.py
# Open http://localhost:5001
```

---

**Built with ❤️ for healthcare billing automation**
