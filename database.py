import sqlite3

DB_NAME = (
    "expenses.db"
)

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS categories(
                           category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT UNIQUE NOT NULL,
                           monthly_limit REAL NOT NULL CHECK(monthly_limit > 0)
                       );                       
                       """)
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS expenses(
                           expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           amount REAL NOT NULL CHECK(amount>0),
                           category_id INTEGER NOT NULL,
                           expense_date TEXT NOT NULL,
                           note TEXT,
                           FOREIGN KEY(category_id) REFERENCES categories(category_id)
                           );                       
                       """)
        
        default_categories=[
            ("Food", 5000.0),
            ("Travel", 5000.0),
            ("Utilities", 5000.0),
            ("Study & Books", 5000.0),
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO categories (name, monthly_limit) VALUES(?,?);",
            default_categories,
                           )
        conn.commit()
        
def add_expense(amount, category_id, expense_date, note):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO expenses(amount, category_id, expense_date, note) VALUES"
            "(?,?,?,?);",
            (amount, category_id, expense_date, (note or "").strip()),
            )
        conn.commit()
        
def get_categories():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT category_id, name, monthly_limit FROM categories;"
        ).fetchall()
        return{row[1]: {"id":row[0], "lmit":row[2]} for row in rows}

def get_all_expenses():
    with get_connection() as conn:
        query = """ 
                SELECT e.expense_id, e.expense_date, c.name AS category, e.amount, e.note
                FROM expenses e
                INNER JOIN categories c ON e.category_id = c.category_id
                ORDER BY e.expense_date DESC, e.expense_id DESC;  
                """
        return conn.execute(query).fetchall()
    
def get_monthly_summary(month_prefix):
    with get_connection() as conn:
        
        query="""
               SELECT c.name, c.monthly_limit, COALESCE(SUM(e.amount), 0) AS total_spent
               FROM categories c
               LEFT JOIN expenses e
               ON c.category_id = e.category_id
               AND e.expense_date LIKE ? 
               GROUP BY c.category_id, c.name, c.monthly_limit
               ORDER BY c.name ASC; 
              """
        return conn.execute(query, (f"{month_prefix}%",)).fetchall()

def update_expense(expense_id, amount, category_id, expense_date, note):
    with get_connection() as conn:
        conn.execute(
            """ UPDATE expenses
                SET amount = ?, category_id = ?, expense_date = ?, note = ?
                WHERE expense_id = ?;
            """,
            (amount, category_id, expense_date, (note or "").strip(), expense_id),
            )
        conn.commit()
        
def delete_expense(expense_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM expenses WHERE expense_id = ?;",
            (expense_id,),
        )
        conn.commit()