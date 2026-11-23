# Personal Expense & Budget Tracker

A full-CRUD Python and SQLite3 web application built with Streamlit and Pandas to track daily expenses, monitor monthly category budgets, edit/delete records, and export reports as CSV. 

## Features
- **Relational SQLite3 Databases:** Normalized 'categories' and 'expenses' tables with 'FOREIGN KEY' and 'CHECK' constraints, plus paramaterized queries ('?') to prevent SQL injection.
- **Full CRUD Operations:** Add, view, edit('UPDATE'), and delete ('DELETE') expenses with immediate recalculation of monthly category budgets.
- **Monthly Budget Analytics:** 'LEFT JOIN', 'GROUP BY', and 'COALESCE' to track spending against monthly imits and flag over-budget categories.
- **CSV Report Export:** One-click download of expense history using pandas.


## Setup & Run Locally
'''bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py