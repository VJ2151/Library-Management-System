# 📚 Library Management System

A web-based library system built using **Django** for librarians to manage books, members, transactions, and import books from Frappe API.

## 🚀 Features

✅ Manage books with stock  
✅ Add/edit/delete members  
✅ Issue and return books  
✅ Enforce ₹500 outstanding limit per member  
✅ Automatically calculate late return fees  
✅ Import books using the Frappe Books API  
✅ Mobile-responsive & Bootstrap 5 UI  
✅ Django Admin interface  
✅ Hosted on PythonAnywhere

## 🖥️ Screenshots

> 💡 Add these as real images in your repo or use relative links to `screenshots/` folder.

| Dashboard | Issue Book | Return Book | Import Page | Admin Panel |
|----------|------------|-------------|-------------|-------------|
| ![](screenshots/dashboard.png) | ![](screenshots/issue.png) | ![](screenshots/return.png) | ![](screenshots/import.png) | ![](screenshots/admin.png) |

## 🔧 Tech Stack

- **Backend:** Django 5.2
- **Frontend:** Bootstrap 5
- **Database:** SQLite3
- **Deployment:** PythonAnywhere
- **API Integration:** Frappe Book API

## 📦 Setup Instructions

```bash
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
python -m venv env
source env/bin/activate   # or env\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
