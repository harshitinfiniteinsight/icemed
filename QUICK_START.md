# ICE Reconciliation - Quick Start Guide

## ✅ Server is Running!

**URL:** http://localhost:5001

---

## 🎯 What You'll See

### 1. Upload Page (http://localhost:5001)

Two options to process files:

**Option A: Upload Your Own File**
- Click "Choose Excel file (.xlsx)"
- Select your ICE export file
- Click "Process File"

**Option B: Use Sample Files**
- Select from dropdown:
  - `sample_complete.xlsx` - 100% success rate
  - `sample_missing_dx.xlsx` - Missing diagnosis codes
  - `sample_missing_cpt.xlsx` - Missing procedure codes
  - `sample_mixed.xlsx` - Various scenarios ⭐ **TRY THIS FIRST**
  - `sample_multiple_dates.xlsx` - Multiple service dates
  - `sample_large.xlsx` - 150 encounters
- Click "Process Sample"

---

## 📊 Results Page

After processing, you'll see:

### 1. **Summary Statistics Cards**
- Total Encounters
- Billed Successfully (green)
- Not Billed (red)
- Success Rate

### 2. **Master Missing Updates**
- Added: New incomplete encounters
- Updated: Existing encounters updated
- Removed: Encounters that became billable

### 3. **📋 DATA TABLE** ⭐ NEW!
Shows first 20 rows with:
- Patient Name
- Date of Service
- Facility
- Type of Care
- CPT Code
- **Billed Status** (Green badge = Yes, Red badge = No)
- **Reason for not billed** (shows error if failed)

**Color Coding:**
- 🟢 Green rows = Successfully billed
- 🔴 Pink rows = Not billed (with reason)

### 4. **Download Buttons**
- Download General Reconciliation (full data + summary)
- Download Master Missing (historical ledger)

---

## 🚀 Try It Now!

1. **Open:** http://localhost:5001
2. **Select:** "Mixed scenarios (25 encounters)" from dropdown
3. **Click:** "Process Sample"
4. **View:** Data table showing which encounters were billed and which weren't

---

## 📋 What the Data Table Shows

Example from `sample_mixed.xlsx`:

| Patient | Date | Facility | CPT | Billed | Reason |
|---------|------|----------|-----|--------|--------|
| Patient001 | 12-09-2025 | Hospital A | 99213 | ✅ Yes | - |
| Patient011 | 12-09-2025 | Hospital A | (empty) | ❌ No | Missing DX |
| Patient016 | 12-09-2025 | Hospital A | 99213 | ❌ No | Missing CPT |

---

## 💡 Understanding the Results

**Green Badge (Yes):** Encounter was successfully billed
- All required fields present
- Passed all business rules
- Claim created

**Red Badge (No):** Encounter could not be billed
- Missing required data
- Shows specific reason:
  - "Missing DX" - No diagnosis code
  - "Missing CPT" - No procedure code
  - "Invalid Facility" - Facility field empty
  - "Provider Mismatch" - Provider issues

---

## 🔄 Test the Master Missing Tracking

1. Process `sample_missing_dx.xlsx` - Creates Master Missing with 10 records
2. Process `sample_mixed.xlsx` - Updates Master Missing (adds more records)
3. Process `sample_complete.xlsx` - No Master Missing records (all billed)

The Master Missing file accumulates incomplete encounters across all runs!

---

## 📥 What You Can Download

### General Reconciliation File
- **Sheet 1 (Data):** All encounters with billing status
- **Sheet 2 (Summary):** Aggregated statistics by date/facility/provider

### Master Missing File
- Historical ledger of all incomplete encounters
- Updates across multiple runs
- Tracks "Last Attempt to Process" date

---

## 🎨 Features

- ✅ Modern, responsive UI
- ✅ Real-time processing status
- ✅ Color-coded data table
- ✅ Badge indicators for billing status
- ✅ Hover effects on table rows
- ✅ Professional styling
- ✅ Mobile-friendly design

---

**Ready to see it in action?** 

👉 **http://localhost:5001** 👈

Select "Mixed scenarios" and watch the data table populate with color-coded results!
