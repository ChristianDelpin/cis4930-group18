# Project 3: Django API Integration

## Overview

This project implements **Section 2.5: API Integration** and **Section 2.6: Security & Deployment** for a Django web application that integrates countries and currencies data from the REST Countries API.

### What It Does
-  Fetches ~250 countries + ~165 currencies from a live REST API
-  Stores data in Django database using ORM
-  Provides web interface to fetch and delete data
-  Manages secrets safely with environment variables

---

## Quick Start

### 1. Create Virtual Environment
```bash
# From the project3 directory
python3 -m venv .venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 2. Install Dependencies
```bash
# Make sure you're inside project3 directory
cd project3
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Setup Database
```bash
cd ..  # Go back to the root directory where manage.py is
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### 5. Start Server
```bash
python manage.py runserver
```

### 6. Access Application
- Dashboard: `http://localhost:8000/data-management/`
- Admin Panel: `http://localhost:8000/admin/`

---

## How to Use

### Via Web Interface (Easiest)

1. Go to: `http://localhost:8000/data-management/`
2. Click **" Fetch Data"** button
3. Wait 2-5 seconds
4. Stats update: "250 Countries, 165 Currencies"
5. Click **" Delete All"** to reset (for next demo)

### Via Terminal Command

```bash
# Fetch data from API
python manage.py fetch_data --verbose
```

---

## CRUD Operations (Create, Read, Update, Delete)

You can manage currencies directly from the web interface:

### View All Currencies
Go to: `http://localhost:8000/records/`
- Shows list with pagination (20 per page)
- Has Edit and Delete links for each currency

### View One Currency
Go to: `http://localhost:8000/records/USD/`
- Replace `USD` with any currency code
- Shows: Code, Name, Symbol

### Add New Currency
1. Go to: `http://localhost:8000/records/add/`
2. Fill in form: Code (like `ZZZ`), Name, Symbol
3. Click Save

### Edit Currency
1. Go to: `http://localhost:8000/records/USD/edit/`
2. Change values in form
3. Click Save

### Delete Currency
1. Go to: `http://localhost:8000/records/USD/delete/`
2. Page shows confirmation
3. Click "Yes, Delete"

---

## Section 2.5: API Integration

**What it implements:**

**Management Command** - `project3/management/commands/fetch_data.py`
- Calls REST Countries API (`https://restcountries.com/v3.1/all`)
- Uses `requests` library with error handling
- Implements timeout protection (10 seconds)
- Uses `raise_for_status()` for error detection
- Handles pagination with batch size (default 50)

 **Django ORM** - Saves data safely
- Uses `get_or_create()` to prevent duplicates
- Atomic transactions for data consistency
- Models: `Country` and `Currency`

 **Web Endpoint** - `/fetch/` and `/delete/` (POST, staff-only)
- Calls management command in-process
- Protected with `@user_passes_test()` decorator
- Uses Django messages for user feedback
- CSRF protected

 **Error Handling**
- Network timeouts caught with try/except
- Invalid JSON responses handled
- Missing data fields skipped with warnings
- Database errors rolled back automatically

---

## Section 2.6: Security & Deployment

**What it implements:**

 **Environment Variables** - `python-decouple`
- File: `project3/settings.py`
- Loads `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` from `.env`
- Example: `SECRET_KEY = config('SECRET_KEY', default='...')`

 **Environment File Protection**
- File: `.env.example` - Template (in GitHub)
- File: `.env` - Your secrets (Git-ignored, not in GitHub)
- Listed in `.gitignore` - Prevents accidental commits

 **Secure Configuration**
- No hardcoded secrets in code
- Different settings for development vs production
- `ALLOWED_HOSTS` restricted to localhost
- Security middleware enabled

---

## Setup Environment Variables

### 1. Create .env File
```bash
cp .env.example .env
```

### 2. Edit .env (Your Secrets)
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Django Loads Automatically
No additional setup needed! Django reads from `.env` on startup.

---

## Project Structure

```
project3/
├── manage.py                          ← Run commands here
├── settings.py                        ← Configuration (uses decouple)
├── urls.py                            ← Website routes
├── views.py                           ← Page handlers
├── models.py                          ← Database models
├── forms.py                           ← Currency form for CRUD
├── requirements.txt                   ← Python packages
├── .env.example                       ← Template (copy to .env)
│
├── management/commands/
│   └── fetch_data.py                 ← API fetching command
│
├── templates/core/
│   ├── base.html                     ← Navigation
│   ├── data_management.html          ← Fetch/Delete interface
│   ├── records_list.html             ← List all currencies
│   ├── record_detail.html            ← View one currency
│   ├── record_form.html              ← Add/Edit form
│   ├── record_confirm_delete.html    ← Delete confirmation
│   ├── currency_list.html            ← Display currencies
│   └── home.html                     ← Homepage
│
└── static/css/
    └── style.css                     ← Styling
```

---





```
```

---

## Common Commands

```bash
# Fetch data from API
python manage.py fetch_data --verbose

# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Check deployment readiness
python manage.py check
```

---


---

## Data Fetched

| Model | Count | Source |
|-------|-------|--------|
| Countries | ~250 | REST Countries API v3.1 |
| Currencies | ~165 | REST Countries API v3.1 |

**API Endpoint**: `https://restcountries.com/v3.1/all`

---

## Why This Design?

**API Integration (Section 2.5)**
- Shows how to fetch live data from external APIs
- Demonstrates error handling for real-world scenarios
- Uses industry-standard patterns (Django ORM, transactions)

**Security & Deployment (Section 2.6)**
- Teaches why secrets should never be hardcoded
- Shows environment-based configuration
- Prepares code for production deployment

---



---


