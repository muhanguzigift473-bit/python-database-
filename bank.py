import sqlite3

# 1. Connect to the database
conn = sqlite3.connect("iron_horizon_bank.db")
cursor = conn.cursor()

# 2. Enable Foreign Key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# 3. Create Tables
# --- Employees Table ---
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        role TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
''')

# --- Customers Table ---
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        assigned_employee_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (assigned_employee_id) REFERENCES employees(employee_id) ON DELETE SET NULL
    )
''')

# --- Accounts Table ---
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT UNIQUE NOT NULL,
        customer_id INTEGER NOT NULL,
        account_type TEXT NOT NULL,
        balance REAL DEFAULT 0.0 CHECK(balance >= 0.0),
        status TEXT DEFAULT 'Active',
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
    )
''')

# --- Transactions Table ---
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        transaction_type TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount > 0.0),
        transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
        description TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
    )
''')

# 4. Insert Custom Sample Data
try:
    # Insert Bank Staff
    employees_data = [
        ("Alistair", "Vane", "Senior Wealth Manager", "a.vane@ironhorizon.com"),
        ("Elena", "Rostova", "Private Banker", "e.rostova@ironhorizon.com")
    ]
    cursor.executemany("INSERT OR IGNORE INTO employees (first_name, last_name, role, email) VALUES (?, ?, ?, ?)", employees_data)

    # Insert Bank Clients
    customers_data = [
        ("Cassian", "Drake", "cassian.drake@vanguard.io", "+1-555-8932", 1),
        ("Lyra", "Sterling", "lyra.s@meridian.design", "+1-555-4711", 2)
    ]
    cursor.executemany("INSERT OR IGNORE INTO customers (first_name, last_name, email, phone, assigned_employee_id) VALUES (?, ?, ?, ?, ?)", customers_data)

    # Insert Client Accounts
    accounts_data = [
        ("IHB-99821", 1, "Corporate Checking", 1450000.00),
        ("IHB-99822", 1, "High-Yield Savings", 4200000.00),
        ("IHB-44109", 2, "Personal Checking", 85400.75)
    ]
    cursor.executemany("INSERT OR IGNORE INTO accounts (account_number, customer_id, account_type, balance) VALUES (?, ?, ?, ?)", accounts_data)

    # Insert Ledger Ledger Entries
    transactions_data = [
        (1, "Deposit", 250000.00, "Inbound Wire Transfer - Venture Funding"),
        (3, "Withdrawal", 1250.00, "Online Brokerage Settlement")
    ]
    cursor.executemany("INSERT OR IGNORE INTO transactions (account_id, transaction_type, amount, description) VALUES (?, ?, ?, ?)", transactions_data)

    conn.commit()
    print("Iron Horizon Bank internal systems initialized successfully.\n")

except sqlite3.Error as e:
    print(f"Database error occurred: {e}")


# 5. Query Example: View Wealth Management Portfolios
def display_bank_summary():
    print(f"{'Client Account Holder':<20} | {'Account No.':<12} | {'Account Type':<20} | {'Balance':<14} | {'Assigned Banker':<18}")
    print("-" * 95)
    
    query = """
        SELECT 
            c.first_name || ' ' || c.last_name AS customer_name,
            a.account_number,
            a.account_type,
            a.balance,
            e.first_name || ' ' || e.last_name AS employee_name
        FROM accounts a
        JOIN customers c ON a.customer_id = c.customer_id
        LEFT JOIN employees e ON c.assigned_employee_id = e.employee_id
        ORDER BY a.balance DESC
    """
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"{row:<20} | {row:<12} | {row:<20} | ${row:<13,.2f} | {row:<18}")
    print("-" * 95)

# Execute portfolio overview
display_bank_summary()

# Close backend ledger connection
conn.close()
