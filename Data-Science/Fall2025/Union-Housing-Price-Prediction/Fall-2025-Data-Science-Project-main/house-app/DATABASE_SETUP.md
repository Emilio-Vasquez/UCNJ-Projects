# MySQL Database Setup Guide

## Prerequisites
- MySQL Server installed on your computer
- MySQL running on localhost (port 3306)

## Step 1: Verify MySQL is Running

Open Command Prompt or PowerShell and check if MySQL is running:

```bash
mysql --version
```

## Step 2: Connect to MySQL

Connect to MySQL as root user:

```bash
mysql -u root -p
```

Enter your password: `Katdawg2a#`

## Step 3: Create Database and Tables

Once connected to MySQL, run these commands:

```sql
-- Create the database
CREATE DATABASE IF NOT EXISTS flaskproject;

-- Use the database
USE flaskproject;

-- Create the users table
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Verify the table was created
SHOW TABLES;

-- Check the table structure
DESCRIBE users;
```

## Step 4: Test the Connection

After creating the database, test your Flask connection:

```bash
# Make sure you're in the project root directory
cd house-app

# Activate your virtual environment (if you have one)
# On Windows:
.\venv\Scripts\activate

# Run the Flask app
python run.py
```

## Step 5: Verify Connection in Flask

You can test the database connection by adding a test route in your Flask app or checking the console for any connection errors when the app starts.

## Common Issues

### Issue 1: "Access denied for user"
- Check your `.env` file has the correct password
- Verify the MySQL user exists and has proper privileges

### Issue 2: "Unknown database 'flaskproject'"
- Make sure you ran the CREATE DATABASE command
- Check the database name in your `.env` file matches

### Issue 3: Connection timeout
- Verify MySQL service is running
- Check the port number (default: 3306)
- Ensure DB_HOST is set to "localhost" in `.env`

## Granting Privileges (if needed)

If you need to grant privileges to the root user:

```sql
GRANT ALL PRIVILEGES ON flaskproject.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

## Alternative: Run SQL File Directly

You can also run the schema.sql file directly from the command line:

```bash
mysql -u root -p < database/schema.sql
```

Then enter your password when prompted.

