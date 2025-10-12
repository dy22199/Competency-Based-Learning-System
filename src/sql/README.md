# SQL Database Creation Guide

This project demonstrates how to create a SQL database and tables using Python and SQLite.

## Files Overview

- `create_database.py` - Creates a complete database with sample data
- `database_schema.sql` - Pure SQL commands for creating tables
- `database_manager.py` - Python class for database operations
- `requirements.txt` - Dependencies (none required for SQLite)

## Quick Start

### 1. Create Database and Tables

Run the main script to create a database with sample data:

```bash
python create_database.py
```

This will create:
- `sample_database.db` - SQLite database file
- 5 tables: users, products, categories, orders, order_items
- Sample data in all tables

### 2. Interact with Database

Use the database manager for common operations:

```bash
python database_manager.py
```

## Database Schema

### Tables Created:

1. **categories** - Product categories
2. **users** - User accounts
3. **products** - Product catalog
4. **orders** - Customer orders
5. **order_items** - Order details (many-to-many)

### Key Relationships:
- Products belong to Categories (foreign key)
- Orders belong to Users (foreign key)
- Order Items link Orders and Products (many-to-many)

## SQL Commands

You can also run the SQL commands directly from `database_schema.sql` in any SQLite client.

## Database Operations

The `DatabaseManager` class provides methods for:

- Adding users and products
- Searching products
- Getting products by category
- Updating stock levels
- Finding low stock items

## Alternative Database Options

### SQLite (Current)
- ✅ No installation required
- ✅ File-based, portable
- ✅ Perfect for learning and small projects
- ❌ Limited concurrent users

### MySQL
```bash
# Install MySQL server
# Create database: CREATE DATABASE mydb;
# Use mysql-connector-python for Python integration
```

### PostgreSQL
```bash
# Install PostgreSQL server
# Create database: CREATE DATABASE mydb;
# Use psycopg2 for Python integration
```

## Next Steps

1. **Run the scripts** to see the database in action
2. **Modify the schema** in `database_schema.sql` for your needs
3. **Extend the DatabaseManager** class with more operations
4. **Add a web interface** using Flask/Django
5. **Migrate to MySQL/PostgreSQL** for production use

## Useful SQLite Tools

- **DB Browser for SQLite** - GUI tool for database management
- **sqlite-web** - Web-based database browser: `pip install sqlite-web`
- **Command line**: `sqlite3 sample_database.db`