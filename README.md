# Invoice Generator - Billing & Ledger Management System

A production-ready, single-user billing and ledger management web application built with Flask and MySQL.

## Features

### Party Management
- Add, Edit, Delete, Search parties/customers
- Opening balance tracking
- Outstanding amount calculation
- Full transaction history

### Invoice / Billing System
- Create, Edit, Delete invoices
- Dynamic item rows with auto-calculation
- Auto invoice numbering (configurable prefix)
- Item-wise billing (no tax system)
- Print and PDF export

### Payment Entry
- Record payments with multiple modes (Cash, Cheque, Bank Transfer, UPI, Card)
- Partial and advance payment support
- Auto payment numbering
- PDF receipt generation

### Ledger & Statements
- Accounting-style running ledger with Debit/Credit/Balance
- Party-wise ledger with date filtering
- Combined ledger showing all parties
- Opening and closing balance
- PDF and Excel export
- Print support

### Dashboard
- Summary cards (Total parties, invoices, payments, outstanding)
- Recent transactions
- Top outstanding parties

### Settings
- Business information
- Invoice/Payment prefix configuration
- Password change

## Tech Stack

| Component   | Technology          |
|-------------|---------------------|
| Backend     | Python Flask        |
| Database    | MySQL               |
| ORM         | SQLAlchemy          |
| Frontend    | HTML5, CSS3, JS     |
| Templates   | Jinja2              |
| PDF Export  | ReportLab           |
| Excel Export| openpyxl            |

## Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Invoice-Generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MySQL database**
   ```sql
   CREATE DATABASE invoice_generator CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Configure database connection**

   Edit `config.py` or set environment variable:
   ```bash
   set DATABASE_URL=mysql://username:password@localhost/invoice_generator
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Initial Setup**
   - Open `http://localhost:5000/auth/setup`
   - Create admin user
   - Login and start using

## Architecture

### Ledger Calculation Flow
```
Opening Balance
+ Total Invoice Amounts (Debit)
- Total Payment Amounts (Credit)
= Outstanding Balance
```

### Outstanding Calculation
```
Outstanding = Opening Balance + Total Invoices - Total Payments
```

### Database Schema
- **parties** - Customer/Party master data
- **invoices** - Invoice headers
- **invoice_items** - Invoice line items
- **payments** - Payment records
- **settings** - Application configuration
- **users** - Admin user accounts

### Key Design Decisions
- **Single user** - No multi-user complexity
- **No tax system** - Clean billing without GST/VAT
- **Running balance ledger** - Accounting-style for accuracy
- **Auto numbering** - Configurable prefixes for invoices and payments
- **Cascade delete** - Deleting a party removes all related transactions

## API Endpoints

| Module    | Endpoints                                      |
|-----------|-----------------------------------------------|
| Auth      | `/auth/login`, `/auth/logout`, `/auth/setup`  |
| Dashboard | `/`, `/dashboard`                             |
| Parties   | `/parties/` CRUD, `/parties/search`           |
| Invoices  | `/invoices/` CRUD, `/invoices/view/<id>`      |
| Payments  | `/payments/` CRUD, `/payments/view/<id>`      |
| Ledger    | `/ledger/`, `/ledger/party/<id>`, `/ledger/combined` |
| Exports   | PDF & Excel downloads                         |
| Settings  | `/settings/`                                  |

## Usage

1. **Setup**: Create admin account at `/auth/setup`
2. **Add Parties**: Navigate to Parties → Add Party
3. **Create Invoices**: Invoices → New Invoice → Select party → Add items
4. **Record Payments**: Payments → Record Payment
5. **View Ledger**: Ledger → Select party → View running balance
6. **Export**: Use PDF/Excel buttons on ledger and invoice pages

## Performance Optimizations
- SQLAlchemy query optimization with joins
- Pagination on all list views
- Indexed foreign keys for faster joins
- Lazy loading for related data where appropriate

## Security
- Password hashing with Werkzeug
- CSRF protection via Flask-Login
- SQL injection prevention via SQLAlchemy ORM
- Input validation on all forms
- Session management with secure cookies
