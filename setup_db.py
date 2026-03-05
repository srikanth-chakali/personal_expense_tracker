import mysql.connector

# Connect to MySQL server
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="srikanth"
    )
    cursor = conn.cursor()
    
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS users_expense_tracker_cred")
    print("✓ Database 'users_expense_tracker_cred' created/verified")
    
    # Select database
    cursor.execute("USE users_expense_tracker_cred")
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        password VARCHAR(255)
    )
    """)
    print("✓ Users table created/verified")
    
    # Create expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        date TEXT,
        category VARCHAR(100),
        payment VARCHAR(100),
        amount DECIMAL(10, 2),
        description TEXT
    )
    """)
    print("✓ Expenses table created/verified")
    
    # Create income table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        amount DECIMAL(10, 2),
        date TEXT
    )
    """)
    print("✓ Income table created/verified")
    
    conn.commit()
    print("\n✓ Database setup completed successfully!")
    
except mysql.connector.Error as err:
    print(f"✗ Error: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
