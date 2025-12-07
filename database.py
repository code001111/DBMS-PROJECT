import sqlite3
import os
from datetime import datetime

DB_PATH = 'shopping_store.db'

def init_database():
    """Initialize the database with tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            quantity_available INTEGER NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            city TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Orders table (One-to-many: Customer -> Orders)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL DEFAULT 0,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        )
    ''')
    
    # Create Order_Items table (One-to-many: Order -> Order_Items)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Order_Items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def add_sample_products():
    """Add sample products to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    sample_products = [
        ('Laptop', 'High-performance laptop for gaming and work', 999.99, 10, 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop'),
        ('Mouse', 'Wireless optical mouse', 29.99, 50, 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop'),
        ('Keyboard', 'Mechanical gaming keyboard', 149.99, 30, 'https://images.unsplash.com/photo-1587829191301-46f5d47e5e33?w=400&h=400&fit=crop'),
        ('Monitor', '27-inch 4K monitor', 399.99, 15, 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop'),
        ('Headphones', 'Noise-canceling headphones', 199.99, 25, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop'),
        ('USB-C Cable', 'Fast charging USB-C cable', 19.99, 100, 'https://images.unsplash.com/photo-1609034227505-5876f6aa4e90?w=400&h=400&fit=crop'),
        ('Webcam', '1080p HD webcam', 89.99, 20, 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400&h=400&fit=crop'),
        ('Phone Stand', 'Adjustable phone stand', 24.99, 40, 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop'),
    ]
    
    for product in sample_products:
        cursor.execute('''
            INSERT OR IGNORE INTO Products (product_name, description, price, quantity_available, image_url)
            VALUES (?, ?, ?, ?, ?)
        ''', product)
    
    conn.commit()
    conn.close()
    print("Sample products added!")

if __name__ == '__main__':
    init_database()
    add_sample_products()
