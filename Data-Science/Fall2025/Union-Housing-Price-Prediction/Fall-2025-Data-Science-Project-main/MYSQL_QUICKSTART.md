# MySQL Quick Start Guide

## Your Current Setup ✓

Your Flask app is already configured to connect to MySQL with these settings:

- **Host:** localhost
- **Port:** 3306
- **User:** root
- **Password:** Katdawg2a# (stored in `.env`)
- **Database:** flaskproject

## Quick Setup (3 Steps)

### Option 1: Automated Setup (Recommended)

1. **Navigate to the house-app directory:**
   ```bash
   cd house-app
   ```

2. **Run the initialization script:**
   ```bash
   python init_db.py
   ```

3. **Test the connection:**
   ```bash
   python test_connection.py
   ```

4. **Start your Flask app:**
   ```bash
   python run.py
   ```

### Option 2: Manual Setup

1. **Open MySQL:**
   ```bash
   mysql -u root -p
   ```
   Enter password: `Katdawg2a#`

2. **Run these SQL commands:**
   ```sql
   CREATE DATABASE IF NOT EXISTS flaskproject;
   USE flaskproject;
   
   CREATE TABLE IF NOT EXISTS users(
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) UNIQUE NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
       phone VARCHAR(20),
       is_verified BOOLEAN DEFAULT FALSE,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

3. **Exit MySQL and test:**
   ```bash
   exit
   cd house-app
   python test_connection.py
   ```

## What's Already Set Up

✅ **Database Configuration** (`config.py`)
- Loads MySQL credentials from `.env` file
- Configures connection parameters

✅ **Database Connection Handler** (`app/db.py`)
- `get_db()` - Opens MySQL connection
- `close_db()` - Closes connection after request
- `query_test()` - Test query function

✅ **Flask Integration** (`app/__init__.py`)
- Database automatically initialized with Flask app
- Connections cleaned up after each request

✅ **Dependencies** (`requirements.txt`)
- `mysql-connector-python` already installed

## How to Use the Database in Your App

Here's an example of how to query the database in your routes:

```python
from .db import get_db

@bp.route("/users")
def get_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    cursor.close()
    return render_template("users.html", users=users)
```

## Troubleshooting

**Problem:** "Can't connect to MySQL server"
- **Solution:** Make sure MySQL is running on your computer

**Problem:** "Access denied"
- **Solution:** Check the password in `.env` matches your MySQL root password

**Problem:** "Unknown database 'flaskproject'"
- **Solution:** Run `python init_db.py` to create the database

## Next Steps

After setting up the database, you can:
1. Add more tables to `database/schema.sql`
2. Create database query functions in `app/db.py`
3. Build routes that read/write to the database
4. Implement user registration and login with database storage

## Useful Commands

**Check if MySQL is running:**
```bash
mysql --version
```

**Connect to MySQL:**
```bash
mysql -u root -p
```

**Show databases:**
```sql
SHOW DATABASES;
```

**Show tables:**
```sql
USE flaskproject;
SHOW TABLES;
```

**View table structure:**
```sql
DESCRIBE users;
```

**View table data:**
```sql
SELECT * FROM users;
```

