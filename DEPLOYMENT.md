# TechStore - Deployment Guide

## 🚀 Project Successfully Deployed to GitHub

**Repository**: https://github.com/code001111/DBMS-PROJECT

All files have been pushed to the main branch. Here's what's included:

## 📁 Project Structure

```
shopping_store/
├── app.py                      # Flask backend API (routes & endpoints)
├── database.py                 # SQLite database initialization
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
├── QUICKSTART.txt              # Quick start guide
├── DEPLOYMENT.md               # This file
├── shopping_store.db           # SQLite database (auto-created)
│
├── templates/                  # HTML templates
│   ├── index.html              # Home page
│   ├── shop.html               # Product listing page
│   ├── cart.html               # Shopping cart
│   ├── checkout.html           # Checkout form
│   ├── orders.html             # Order history page
│   └── bill.html               # Invoice/bill page
│
└── static/                     # Static assets
    ├── style.css               # Dark theme CSS
    ├── script.js               # Frontend JavaScript
    ├── favicon.svg             # Browser tab icon
    └── images/
        ├── laptop.svg
        ├── mouse.svg
        ├── keyboard.svg
        ├── monitor.svg
        ├── headphones.svg
        ├── usb-cable.svg
        ├── webcam.svg
        └── phone-stand.svg
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.7+
- Git
- pip (Python package manager)

### Local Setup

1. **Clone the repository:**
```bash
git clone https://github.com/code001111/DBMS-PROJECT.git
cd shopping_store
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Initialize database:**
```bash
python database.py
```

4. **Run the application:**
```bash
python app.py
```

5. **Access the website:**
```
http://localhost:5000
```

## 📊 Database Schema

### Tables (One-to-Many Relationships)

**Products**
- product_id (PK)
- product_name
- description
- price
- quantity_available
- image_url
- created_at

**Customers**
- customer_id (PK)
- customer_name
- email (UNIQUE)
- phone
- address
- city
- created_at

**Orders** (1 → Many from Customers)
- order_id (PK)
- customer_id (FK)
- order_date
- total_amount
- status

**Order_Items** (1 → Many from Orders)
- item_id (PK)
- order_id (FK)
- product_id (FK)
- quantity
- unit_price
- subtotal

## 🔌 API Endpoints

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get single product
- `POST /api/products` - Create new product

### Customers
- `GET /api/customers` - Get all customers
- `POST /api/customers` - Create new customer

### Orders
- `POST /api/orders` - Create new order
- `GET /api/orders/<customer_id>` - Get customer orders
- `GET /api/orders/<order_id>/items` - Get order items
- `GET /api/orders/<order_id>/bill` - Get bill details

### Pages
- `GET /` - Home page
- `GET /shop` - Shop page
- `GET /cart` - Cart page
- `GET /checkout` - Checkout page
- `GET /orders` - Orders page
- `GET /bill/<order_id>` - Bill page

## 🎨 Features

✅ **Dark Theme** - Modern dark UI
✅ **Real Product Images** - From Unsplash CDN
✅ **Shopping Cart** - Local storage based
✅ **Order Management** - Complete order tracking
✅ **Bill Generation** - Printable invoices
✅ **Responsive Design** - Works on all devices
✅ **One-to-Many Relationships** - Proper database design

## 📱 Sample Workflow

1. Visit http://localhost:5000
2. Click "Shop" to browse products
3. Add items to cart
4. View cart and proceed to checkout
5. Enter customer details
6. Place order
7. Get instant bill with print option
8. Track orders using Customer ID

## 🔧 Configuration

### Change Port
Edit `app.py` line: `app.run(debug=True, port=5000)`

### Database Path
Edit `database.py` line: `DB_PATH = 'shopping_store.db'`

### Shipping Costs
Edit `app.py` order calculation logic to modify shipping rates

## 📦 Sample Products

Pre-loaded in database:
- Laptop - ₹999.99
- Mouse - ₹29.99
- Keyboard - ₹149.99
- Monitor - ₹399.99
- Headphones - ₹199.99
- USB-C Cable - ₹19.99
- Webcam - ₹89.99
- Phone Stand - ₹24.99

## 🚀 Deployment to Production

### Using Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Install gunicorn
pip install gunicorn

# Create app
heroku create your-app-name

# Push to Heroku
git push heroku main

# View logs
heroku logs --tail
```

### Using PythonAnywhere

1. Sign up at pythonywhere.com
2. Upload files via Web UI
3. Create new web app with Flask
4. Configure WSGI file
5. Reload web app

### Using AWS, Azure, or Google Cloud

Deploy using respective cloud CLI tools and Docker containerization.

## 🐛 Troubleshooting

### Port already in use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Database errors
```bash
# Delete and recreate database
rm shopping_store.db
python database.py
```

### Flask not found
```bash
pip install -r requirements.txt
```

## 📚 Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Images**: Unsplash API
- **Version Control**: Git & GitHub

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Developer

Created as a DBMS project demonstrating one-to-many database relationships.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests!

---

**Last Updated**: December 7, 2025
**Status**: ✅ Deployed to GitHub
