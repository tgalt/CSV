# SQLite Reference

A quick reference guide for using SQLite databases.

## Python sqlite3 Module

### Connection

```python
import sqlite3

# Connect to database (creates if doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Always close when done
conn.close()

# Context manager (auto-closes)
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    # ... operations
```

### Creating Tables

```python
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
```

### Common Data Types

- `INTEGER` - Signed integer
- `TEXT` - Text string
- `REAL` - Floating point number
- `BLOB` - Binary data
- `NULL` - NULL value

### Inserting Data

```python
# Single insert
cursor.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', 
               ('John Doe', 'john@example.com', 30))

# Multiple inserts
users = [
    ('Jane Doe', 'jane@example.com', 25),
    ('Bob Smith', 'bob@example.com', 35)
]
cursor.executemany('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', users)

conn.commit()  # Don't forget to commit!
```

### Querying Data

```python
# Fetch one row
cursor.execute('SELECT * FROM users WHERE id = ?', (1,))
row = cursor.fetchone()

# Fetch all rows
cursor.execute('SELECT * FROM users WHERE age > ?', (25,))
rows = cursor.fetchall()

# Fetch as dictionary
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT * FROM users')
for row in cursor:
    print(row['name'], row['email'])
```

### Updating Data

```python
cursor.execute('UPDATE users SET age = ? WHERE id = ?', (31, 1))
conn.commit()
```

### Deleting Data

```python
cursor.execute('DELETE FROM users WHERE id = ?', (1,))
conn.commit()
```

### Common SQL Operations

```python
# Count rows
cursor.execute('SELECT COUNT(*) FROM users')
count = cursor.fetchone()[0]

# Drop table
cursor.execute('DROP TABLE IF EXISTS users')

# Get table info
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
```

## Command Line Tool

### Basic Commands

```bash
# Open database
sqlite3 database.db

# Execute SQL
sqlite3 database.db "SELECT * FROM users;"

# Export to CSV
sqlite3 database.db ".mode csv" ".output users.csv" "SELECT * FROM users;"

# Import from CSV
sqlite3 database.db ".mode csv" ".import users.csv users"

# Show schema
sqlite3 database.db ".schema"

# Show tables
sqlite3 database.db ".tables"
```

## Best Practices

1. **Always use parameterized queries** (`?` placeholders) to prevent SQL injection
2. **Commit transactions** after modifications
3. **Use context managers** or `try/finally` to ensure connections close
4. **Create indexes** on frequently queried columns: `CREATE INDEX idx_email ON users(email)`
5. **Use transactions** for multiple operations: `BEGIN; ... COMMIT;`

## Example Workflow

```python
import sqlite3

def setup_database():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                amount REAL,
                date TEXT
            )
        ''')
        conn.commit()

def add_invoice(invoice_number, amount, date):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO invoices (invoice_number, amount, date) VALUES (?, ?, ?)',
            (invoice_number, amount, date)
        )
        conn.commit()

def get_invoices():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM invoices')
        return cursor.fetchall()
```
