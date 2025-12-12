"""
Test MySQL Connection Script

This script tests if your Flask app can connect to the MySQL database.

Run this from the house-app directory:
    python test_connection.py
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

def test_connection():
    """Test the MySQL database connection"""
    
    print("=" * 50)
    print("Testing MySQL Connection")
    print("=" * 50)
    print(f"\nHost: {DB_HOST}")
    print(f"Port: {DB_PORT}")
    print(f"User: {DB_USER}")
    print(f"Database: {DB_NAME}")
    print("-" * 50)
    
    try:
        # Attempt connection
        print("\nAttempting to connect...")
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        print("✓ Connection successful!\n")
        
        # Test query
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DATABASE() as current_db, VERSION() as version")
        result = cursor.fetchone()
        
        print(f"Current Database: {result['current_db']}")
        print(f"MySQL Version: {result['version']}")
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"\nTables in database:")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"  - {table_name}")
                
                # Count records
                cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                count = cursor.fetchone()['count']
                print(f"    Records: {count}")
        else:
            print("\nNo tables found in database.")
            print("Run 'python init_db.py' to create tables.")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
        
        return True
        
    except mysql.connector.Error as err:
        print(f"\n✗ Connection failed!")
        print(f"Error: {err}\n")
        
        if err.errno == 1049:  # Unknown database
            print("The database doesn't exist yet.")
            print("Solution: Run 'python init_db.py' to create it.")
        elif err.errno == 1045:  # Access denied
            print("Access denied - check your username/password.")
            print("Solution: Verify credentials in .env file.")
        elif err.errno == 2003:  # Can't connect
            print("Can't connect to MySQL server.")
            print("Solution: Make sure MySQL is running.")
        else:
            print("Possible solutions:")
            print("1. Make sure MySQL server is running")
            print("2. Check your .env file for correct credentials")
            print("3. Run 'python init_db.py' to set up the database")
        
        print("\n" + "=" * 50)
        return False

if __name__ == "__main__":
    test_connection()

