"""
Database Initialization Script

This script will:
1. Connect to MySQL server
2. Create the flaskproject database (if it doesn't exist)
3. Create the users table
4. Verify the setup

Run this script from the house-app directory:
    python init_db.py
"""

import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def init_database():
    """Initialize the database and create tables"""
    
    print("=" * 50)
    print("MySQL Database Initialization")
    print("=" * 50)
    
    try:
        # Step 1: Connect to MySQL server (without specifying database)
        print(f"\n1. Connecting to MySQL server at {DB_HOST}:{DB_PORT}...")
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        print("✓ Connected successfully!")
        
        # Step 2: Create database if it doesn't exist
        print(f"\n2. Creating database '{DB_NAME}' (if not exists)...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✓ Database '{DB_NAME}' is ready!")
        
        # Step 3: Use the database
        cursor.execute(f"USE {DB_NAME}")
        
        # Step 4: Create users table
        print("\n3. Creating 'users' table...")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        print("✓ Users table created successfully!")
        
        # Step 5: Verify the table
        print("\n4. Verifying tables...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✓ Tables in database: {[table[0] for table in tables]}")
        
        # Step 6: Show table structure
        print("\n5. Table structure:")
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        print("\nUsers table columns:")
        print("-" * 80)
        print(f"{'Field':<20} {'Type':<20} {'Null':<10} {'Key':<10} {'Default':<15}")
        print("-" * 80)
        for col in columns:
            field, type_, null, key, default, extra = col
            print(f"{field:<20} {type_:<20} {null:<10} {key:<10} {str(default):<15}")
        
        # Commit and close
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 50)
        print("✓ Database initialization complete!")
        print("=" * 50)
        print("\nYou can now run your Flask app with: python run.py")
        
    except mysql.connector.Error as err:
        print(f"\n✗ Error: {err}")
        print("\nPossible solutions:")
        print("1. Make sure MySQL server is running")
        print("2. Check your credentials in the .env file")
        print("3. Verify the MySQL service is started")
        print("4. Try connecting manually: mysql -u root -p")
        return False
    
    return True

if __name__ == "__main__":
    init_database()

