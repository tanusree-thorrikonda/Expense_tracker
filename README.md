# Expense Tracker

A premium, modern Expenses Tracker application built with Python Flask and vanilla CSS/JS.

## Features

- **Dashboard**: High-level metrics showing total income, total expenses, net balance, and beautiful visual progress.
- **Transactions Management**: Complete CRUD operations for expenses and income.
- **Categories**: Organize your transactions.
- **Clean UI**: A sleek, dark-themed responsive user interface with rich aesthetics.

## Technology Stack

- **Backend**: Flask, Flask-SQLAlchemy (SQLite database), Python-dotenv
- **Frontend**: Vanilla HTML5, modern CSS3 (custom variables, glassmorphism), and Javascript

## Installation & Running

1. Clone or copy this repository to your workspace.
2. Initialize virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Run the development server:
   ```bash
   python backend/app.py
   ```
5. Open `http://127.0.0.1:5000` in your web browser.
