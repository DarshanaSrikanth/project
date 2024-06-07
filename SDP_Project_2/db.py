import sqlite3

# Connect to the database (create if not exists)
conn = sqlite3.connect('laundry_service.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                cloth_type TEXT NOT NULL,
                laundry_type TEXT NOT NULL,
                cost REAL NOT NULL,
                delivery_date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (id))''')

c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL)''')

c.execute("INSERT OR IGNORE INTO users (name, email, password, role) VALUES ('admin', 'admin', 'password', 'admin')")

conn.commit()
conn.close()
# Function to get a new database connection
def get_db_connection():
    return sqlite3.connect('laundry_service.db')