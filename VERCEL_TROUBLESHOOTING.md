# Vercel Troubleshooting Guide

## Current Status

✅ **Build:** Successful  
❓ **Runtime:** May have issues (check logs)

---

## How to Check Vercel Logs

### Option 1: Vercel Dashboard
1. Go to: https://vercel.com/dashboard
2. Select your `icemed` project
3. Click on the latest deployment
4. Click "Functions" tab
5. Click on `api/index.py`
6. View "Logs" tab

### Option 2: Vercel CLI
```bash
vercel logs icemed
```

---

## Common Issues & Fixes

### Issue 1: Function Crashes on Startup

**Symptoms:**
- 500 error immediately
- "FUNCTION_INVOCATION_FAILED"

**Possible Causes:**
1. Flask app not exporting correctly
2. Import errors
3. File path issues

**Fix:**
Check `api/index.py` exports `handler` correctly:
```python
handler = app
```

---

### Issue 2: Templates Not Found

**Symptoms:**
- 500 error on `/` route
- TemplateNotFound error in logs

**Fix:**
Already fixed - Flask now has explicit `template_folder`:
```python
template_dir = os.path.join(PROJECT_ROOT, 'web', 'templates')
app = Flask(__name__, template_folder=template_dir)
```

---

### Issue 3: Static Files Not Loading

**Symptoms:**
- CSS/JS files return 404
- Page loads but no styling

**Fix:**
Already fixed - Flask now has explicit `static_folder`:
```python
static_dir = os.path.join(PROJECT_ROOT, 'web', 'static')
app = Flask(__name__, static_folder=static_dir, static_url_path='/static')
```

---

### Issue 4: Sample Files Not Found

**Symptoms:**
- `/api/sample-files` returns 404
- "Sample directory not found" error

**Possible Causes:**
1. Files not committed to Git
2. Path resolution issue

**Fix:**
Verify files exist in Git:
```bash
git ls-files | grep "data/input"
```

Should show:
- `data/input/sample_complete.xlsx`
- `data/input/sample_mixed.xlsx`
- etc.

---

### Issue 5: Orchestrator Initialization Fails

**Symptoms:**
- "Orchestrator not initialized" error
- Config file not found

**Fix:**
Check `config.json` exists and is committed:
```bash
git ls-files | grep config.json
```

---

## Debug Steps

### Step 1: Check Function Logs
```bash
vercel logs icemed --follow
```

### Step 2: Test Locally First
```bash
cd "/Users/harshitagarwal/Desktop/upwork proposals/ice-reconciliation-mock"
python run.py
# Open http://localhost:5001
```

### Step 3: Verify All Files Committed
```bash
git ls-files | wc -l  # Should be ~37 files
```

### Step 4: Check Vercel Build Output
Look for any warnings or errors in build logs

---

## Quick Fixes

### If Flask App Crashes:

1. **Add debug logging:**
```python
# In api/index.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Check imports:**
```python
# Test imports work
try:
    from web.app import app
    print("✅ Flask app imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
```

### If Routes Don't Work:

Check `vercel.json` routes:
```json
{
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

---

## Testing Checklist

- [ ] Build completes successfully ✅
- [ ] Function deploys without errors
- [ ] `/` route loads (index.html)
- [ ] Static files load (CSS, JS)
- [ ] `/api/sample-files` returns list
- [ ] `/api/preview-sample` works
- [ ] `/api/process-sample` works
- [ ] Downloads work

---

## Next Steps

1. **Check Vercel logs** for specific error
2. **Share error message** if still failing
3. **Test each endpoint** individually
4. **Verify file paths** are correct

---

## Alternative: Use Vercel's Python Runtime Directly

If Flask continues to have issues, we can switch to a simpler approach:

```python
# api/index.py
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Hello"}).encode())
```

But Flask should work - let's debug the current setup first.

---

**Last Updated:** December 10, 2025  
**Status:** Debugging in progress
