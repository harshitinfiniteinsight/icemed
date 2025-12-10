# How to Start the ICE Reconciliation Server

## Quick Start

```bash
cd "/Users/harshitagarwal/Desktop/upwork proposals/ice-reconciliation-mock"
python run.py
```

Then open your browser to: **http://localhost:5001**

---

## Server Status

✅ **Server is Running!**

- **URL:** http://localhost:5001
- **Port:** 5001 (changed from 5000 due to macOS AirPlay conflict)
- **Status:** Active

---

## What You Can Do

1. **Upload Page** (http://localhost:5001)
   - Upload your own Excel file
   - OR select from 6 sample files
   - Click "Process" to start

2. **Sample Files Available:**
   - `sample_complete.xlsx` - All complete (100% success)
   - `sample_missing_dx.xlsx` - 10 missing diagnosis codes
   - `sample_missing_cpt.xlsx` - 8 missing procedure codes
   - `sample_mixed.xlsx` - Various scenarios
   - `sample_multiple_dates.xlsx` - Multiple service dates
   - `sample_large.xlsx` - 150+ encounters

3. **Results Page**
   - View statistics
   - Download General Reconciliation file
   - Download Master Missing file

---

## If Server Stops

Restart with:
```bash
python run.py
```

---

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running
