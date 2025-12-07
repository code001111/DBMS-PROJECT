from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_PATH = 'shopping_store.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==================== PRODUCTS ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if product:
        return jsonify(dict(product))
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/products', methods=['POST'])
def add_product():
    """Add a new product"""
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO Products (product_name, description, price, quantity_available)
            VALUES (?, ?, ?, ?)
        ''', (data['product_name'], data.get('description', ''), data['price'], data['quantity_available']))
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'product_id': product_id}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# ==================== CUSTOMERS ====================

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get all customers"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    conn.close()
    return jsonify([dict(c) for c in customers])

@app.route('/api/customers', methods=['POST'])
def add_customer():
    """Add a new customer"""
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO Customers (customer_name, email, phone, address, city)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['customer_name'], data['email'], data.get('phone', ''), 
              data.get('address', ''), data.get('city', '')))
        conn.commit()
        customer_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'customer_id': customer_id}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Email already exists'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# ==================== ORDERS ====================

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.json
    customer_id = data.get('customer_id')
    items = data.get('items', [])
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Calculate total amount
        total_amount = 0
        for item in items:
            cursor.execute('SELECT price FROM Products WHERE product_id = ?', (item['product_id'],))
            product = cursor.fetchone()
            if not product:
                conn.close()
                return jsonify({'error': f"Product {item['product_id']} not found"}), 404
            total_amount += product['price'] * item['quantity']
        
        # Create order
        cursor.execute('''
            INSERT INTO Orders (customer_id, total_amount, status)
            VALUES (?, ?, 'pending')
        ''', (customer_id, total_amount))
        
        order_id = cursor.lastrowid
        
        # Add order items
        for item in items:
            cursor.execute('SELECT price FROM Products WHERE product_id = ?', (item['product_id'],))
            product = cursor.fetchone()
            unit_price = product['price']
            subtotal = unit_price * item['quantity']
            
            cursor.execute('''
                INSERT INTO Order_Items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            ''', (order_id, item['product_id'], item['quantity'], unit_price, subtotal))
            
            # Update product quantity
            cursor.execute('''
                UPDATE Products SET quantity_available = quantity_available - ?
                WHERE product_id = ?
            ''', (item['quantity'], item['product_id']))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'order_id': order_id, 'total_amount': total_amount}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/orders/<int:customer_id>', methods=['GET'])
def get_customer_orders(customer_id):
    """Get all orders for a customer"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Orders WHERE customer_id = ?', (customer_id,))
    orders = cursor.fetchall()
    conn.close()
    return jsonify([dict(o) for o in orders])

@app.route('/api/orders/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    """Get items for an order"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT oi.*, p.product_name 
        FROM Order_Items oi
        JOIN Products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
    ''', (order_id,))
    items = cursor.fetchall()
    conn.close()
    return jsonify([dict(i) for i in items])

@app.route('/api/orders/<int:order_id>/bill', methods=['GET'])
def get_bill(order_id):
    """Generate bill for an order"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get order details
    cursor.execute('''
        SELECT o.*, c.customer_name, c.email, c.phone, c.address, c.city
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        WHERE o.order_id = ?
    ''', (order_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return jsonify({'error': 'Order not found'}), 404
    
    # Get order items
    cursor.execute('''
        SELECT oi.*, p.product_name 
        FROM Order_Items oi
        JOIN Products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
    ''', (order_id,))
    items = cursor.fetchall()
    conn.close()
    
    bill = {
        'order_id': order['order_id'],
        'order_date': order['order_date'],
        'customer_name': order['customer_name'],
        'email': order['email'],
        'phone': order['phone'],
        'address': order['address'],
        'city': order['city'],
        'items': [dict(i) for i in items],
        'total_amount': order['total_amount']
    }
    
    return jsonify(bill)

# ==================== PAGES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/shop')
def shop():
    """Shop page"""
    return render_template('shop.html')

@app.route('/cart')
def cart():
    """Shopping cart page"""
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    """Checkout page"""
    return render_template('checkout.html')

@app.route('/orders')
def orders():
    """Orders page"""
    return render_template('orders.html')

@app.route('/bill/<int:order_id>')
def bill(order_id):
    """Bill page"""
    return render_template('bill.html', order_id=order_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
