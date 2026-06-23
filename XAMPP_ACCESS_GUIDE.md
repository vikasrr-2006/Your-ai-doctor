# XAMPP Access Guide - Your AI Doctor

## Overview

This guide explains how to access the **Your AI Doctor** application through XAMPP. The application uses a PHP proxy to bridge requests between XAMPP's Apache server and the Flask backend.

## Architecture

```
Browser → Apache (XAMPP, port 80) → PHP Proxy → Flask (port 5000)
```

- **Apache (XAMPP)**: Serves the PHP entry points (`index.php`, `proxy.php`)
- **PHP Proxy** (`proxy.php`): Forwards requests to the Flask application
- **Flask App** (`app.py`): Handles all application logic and ML predictions

## Prerequisites

1. **XAMPP** installed and running (Apache module must be active)
2. **Python 3.8+** installed
3. **Flask** and dependencies installed (`pip install flask numpy scikit-learn`)

## Step-by-Step Setup

### 1. Start XAMPP

1. Open the **XAMPP Control Panel**
2. Click **Start** next to **Apache**
3. Ensure Apache status shows green/running

### 2. Start the Flask Application

**Option A - Using the batch file (recommended):**
```
Double-click start_flask.bat
```

**Option B - Manual start:**
```bash
cd "c:\xampp\htdocs\new help\Your AI Doctor"
python app.py
```

Wait for the message: `Running on http://127.0.0.1:5000`

### 3. Access the Application

| Method | URL | Notes |
|--------|-----|-------|
| **Via XAMPP (recommended)** | `http://localhost/new%20help/Your%20AI%20Doctor/` | Uses PHP proxy |
| **Direct Flask** | `http://localhost:5000` | Bypasses XAMPP |

## How It Works

### index.php
- First point of contact when accessing via XAMPP
- Checks if Flask is running by making a test request
- If Flask is NOT running: displays setup instructions
- If Flask IS running: proxies requests to Flask

### proxy.php
- Receives all HTTP requests from Apache
- Strips the XAMPP path prefix (`/new%20help/Your%20AI%20Doctor`)
- Forwards clean paths to Flask at `127.0.0.1:5000`
- Returns Flask's response back to the browser
- Supports GET, POST, and other HTTP methods

## Troubleshooting

### "Flask Application Not Running" message

**Cause**: Flask backend is not started.

**Solution**:
1. Open a terminal/command prompt
2. Run: `cd "c:\xampp\htdocs\new help\Your AI Doctor"`
3. Run: `python app.py`
4. Refresh the page

### Port 5000 already in use

**Cause**: Another process is using port 5000.

**Solution**:
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Apache not starting (port 80 conflict)

**Cause**: Another service is using port 80 (e.g., IIS, Skype).

**Solution**:
1. In XAMPP Control Panel, click **Config** → **Apache (httpd.conf)**
2. Change `Listen 80` to `Listen 8080`
3. Access via: `http://localhost:8080/new%20help/Your%20AI%20Doctor/`

### PHP cURL extension not enabled

**Cause**: The proxy requires PHP cURL extension.

**Solution**:
1. Open `C:\xampp\php\php.ini`
2. Find `;extension=curl`
3. Remove the semicolon: `extension=curl`
4. Restart Apache in XAMPP

### Blank page or 500 error

**Cause**: Missing Python dependencies.

**Solution**:
```bash
pip install flask numpy scikit-learn geopy
```

### 404 errors for static files (CSS/JS not loading)

**Cause**: The `.htaccess` file may not be processed by Apache.

**Solution**:
1. Ensure `mod_rewrite` is enabled in Apache
2. In `C:\xampp\apache\conf\httpd.conf`, ensure:
   - `LoadModule rewrite_module modules/mod_rewrite.so` is uncommented
   - `AllowOverride All` is set for the htdocs directory

## File Permissions

Ensure the following directories are writable:
- `models/` - for ML model files
- `data/` - for JSON data files
- `__pycache__/` - Python cache (auto-created)

## Network Access (LAN)

To access from other devices on the network:

1. Find your local IP: `ipconfig` (look for IPv4 Address)
2. Ensure Windows Firewall allows connections on port 80 and 5000
3. Access via: `http://<your-ip>/new%20help/Your%20AI%20Doctor/`
4. Update Flask to listen on all interfaces in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```

## Quick Reference

| Component | Location | Default Port |
|-----------|----------|-------------|
| XAMPP Apache | `C:\xampp\apache\` | 80 |
| Flask App | `app.py` | 5000 |
| Entry Point | `index.php` | via Apache |
| Proxy | `proxy.php` | via Apache |
