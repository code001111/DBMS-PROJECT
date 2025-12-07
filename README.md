# TechStore - Online Shopping Store

A simple online shopping store website built with Flask and SQLite, demonstrating one-to-many database relationships.

## Features

✅ **Product Management** - Browse and manage products
✅ **Customer Management** - Register and manage customer information  
✅ **Shopping Cart** - Add/remove products, update quantities
✅ **Order Placement** - Place orders with customer details
✅ **Bill Generation** - View and print order bills
✅ **Order History** - Track customer orders
✅ **Database Relationships** - One-to-many relationships (Customers → Orders → Order_Items)

## Database Schema

### Tables:
1. **Products**
   - product_id (PK)
   - product_name
   - description
   - price
   - quantity_available

2. **Customers**
   - customer_id (PK)
   - customer_name
   - email
   - phone
   - address
   - city

3. **Orders** (One-to-Many: Customers → Orders)
   - order_id (PK)
   - customer_id (FK)
   - order_date
   - total_amount
   - status

4. **Order_Items** (One-to-Many: Orders → Order_Items)
   - item_id (PK)
   - order_id (FK)
   - product_id (FK)
   - quantity
   - unit_price
   - subtotal

## Installation

1. **Install Python Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Initialize Database:**
```bash
python database.py
```

3. **Run the Application:**
```bash
python app.py
```

4. **Access the Website:**
```
http://localhost:5000
```

## Usage

### 1. Browse Products
- Visit the "Shop" page to view all available products
- See product details including price and stock availability

### 2. Add to Cart
- Select quantity and click "Add to Cart"
- Items are stored in browser's localStorage

### 3. Place Order
- Go to "Cart" page to review items
- Click "Proceed to Checkout"
- Enter customer details (name, email, address, etc.)
- Click "Place Order"

### 4. View Bill
- After successful order, you'll be redirected to the bill page
- View order details, items, and total amount
- Click "Print Bill" to generate a printable invoice

### 5. Track Orders
- Go to "Orders" page
- Enter your Customer ID to view your orders
- Click "View Bill" to see the invoice for any order

## API Endpoints

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get single product
- `POST /api/products` - Add new product

### Customers
- `GET /api/customers` - Get all customers
- `POST /api/customers` - Add new customer

### Orders
- `POST /api/orders` - Create new order
- `GET /api/orders/<customer_id>` - Get customer's orders
- `GET /api/orders/<order_id>/items` - Get order items
- `GET /api/orders/<order_id>/bill` - Get bill details

## Project Structure

```
shopping_store/
├── app.py                 # Flask application and API routes
├── database.py            # Database initialization and setup
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates
│   ├── index.html         # Home page
│   ├── shop.html          # Products listing
│   ├── cart.html          # Shopping cart
│   ├── checkout.html      # Checkout form
│   ├── orders.html        # Order history
│   └── bill.html          # Invoice/bill
└── static/                # Static files
    ├── style.css          # Stylesheets
    └── script.js          # JavaScript
```

## Key Concepts Demonstrated

1. **One-to-Many Relationships**
   - Customers ↔ Orders (one customer can have many orders)
   - Orders ↔ Order_Items (one order can have many items)

2. **CRUD Operations**
   - Create: Add products, customers, orders
   - Read: View products, orders, bills
   - Update: Modify cart quantities, product stock
   - Delete: Remove items from cart

3. **Database Integrity**
   - Foreign key relationships
   - Data validation
   - Inventory management

## Sample Data

The application comes pre-loaded with 8 sample products:
- Laptop
- Mouse
- Keyboard
- Monitor
- Headphones
- USB-C Cable
- Webcam
- Phone Stand

## Notes

- Cart data is stored in browser's localStorage (not persistent after clearing)
- Shipping cost is ₹99 for orders under ₹5000, free above that
- Customer email must be unique
- All amounts are in Indian Rupees (₹)

## Future Enhancements

- User authentication and login
- Payment gateway integration
- Order status updates
- Customer reviews and ratings
- Admin dashboard
- Email notifications
