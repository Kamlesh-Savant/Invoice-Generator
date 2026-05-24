# Invoice Generator — AI Agent Instructions

## Project Overview
Flask-based billing & ledger management app. Single-user. No tax system. SQLite by default.

## Tech Stack
- Python Flask + Jinja2 templates
- SQLAlchemy ORM (SQLite default, MySQL optional)
- ReportLab (PDF export), openpyxl (Excel export)
- Vanilla CSS/JS frontend

## Project Structure
```
app/models/       # SQLAlchemy models
app/routes/       # Flask blueprints
app/services/     # PDF & Excel generators
app/templates/    # Jinja2 HTML templates
app/static/       # CSS, JS
config.py         # DB URI, secret key
run.py            # Dev entry point
```

## How to Run Locally
```powershell
cd E:\python projects\Invoice-Generator
pip install -r requirements.txt
python run.py
# Opens at http://localhost:5000
```

## Default Login
- Username: `admin`
- Password: `1234`
- Auto-created on first run (see `app/__init__.py`)

## Database
- **Default:** SQLite file `invoice_generator.db` (auto-created)
- **MySQL:** Set env var `DATABASE_URL=mysql+pymysql://user:pass@host/dbname`

## Deployment (PythonAnywhere Free)
- Username: `daxbill`
- App URL: `https://daxbill.pythonanywhere.com`
- Repo: `https://github.com/Kamlesh-Savant/Invoice-Generator.git`

### Deployment Steps (already done, for reference):
1. Clone repo in PythonAnywhere bash
2. Create venv + `pip install -r requirements.txt`
3. Manual web app → Python 3.10
4. WSGI file at `/var/www/daxbill_pythonanywhere_com_wsgi.py`
5. Static files mapped `/static/` → `/home/daxbill/Invoice-Generator/app/static`
6. Reload

## Change Workflow
When user requests a change, follow this exact sequence:

### Step 1 — Edit code
Make changes in `E:\python projects\Invoice-Generator\`

### Step 2 — Commit & push
```powershell
cd E:\python projects\Invoice-Generator
git add -A
git commit -m "description of change"
git push
```

### Step 3 — Pull on PythonAnywhere
User opens PythonAnywhere Bash console and runs:
```bash
cd ~/Invoice-Generator
git pull
```

### Step 4 — Reload
User clicks **Reload** button on PythonAnywhere Web tab.

## Key Conventions
- No tax/GST fields anywhere
- Single user, no roles/permissions
- Blueprint-based routing (`app/routes/`)
- All templates extend `base.html`
- CSS in `style.css`, JS in `main.js`
- Auto-numbering for invoices (`INV-00001`) and payments (`PAY-00001`), configurable in Settings
