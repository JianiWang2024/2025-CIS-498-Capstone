# Programming Lab 5: PostgreSQL Database and Flask API Development
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy import func

app = Flask(__name__)
CORS(app)

# Lab 5 Step 1-2: PostgreSQL Database Configuration
# Connect to PostgreSQL database created in pgAdmin
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/lost_and_found'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Lab 5 Step 4: Create database design and tables for the Capstone project application

# User Model for Authentication
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Item Model for Lost and Found Items
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'lost' or 'found'
    location = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50))  # Formatted date like "July 5"
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Report Model for Tracking Submissions
class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

# Home Route
@app.route('/')
def home():
    return jsonify({
        "message": "Lost & Found API is running",
        "version": "1.0",
        "author": "Jiani Wang",
        "course": "ACIS 498: Information Systems Capstone",
        "endpoints": {
            "items": "/api/items",
            "users": "/api/users",
            "reports": "/api/reports",
            "login": "/api/login",
            "stats": "/api/stats",
            "search": "/api/search"
        }
    })

# Lab 5 Step 3: Performing CRUD operations on the database

# User Management Routes - CREATE and READ operations for users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    } for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({"error": "Username, password, and email are required"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 409
    
    new_user = User(
        username=data['username'],
        password=data['password'],
        email=data['email']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201

# Authentication Route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# Lab 5 Step 3: Complete CRUD Operations - CREATE, READ, UPDATE, DELETE for Items

@app.route('/api/items', methods=['GET'])
def get_items():
    # READ operation - Get all items with filtering
    item_type = request.args.get('type')
    search = request.args.get('search', '').lower()
    
    query = Item.query
    
    if item_type and item_type in ['lost', 'found']:
        query = query.filter_by(type=item_type)
    
    items = query.order_by(Item.created_at.desc()).all()
    
    if search:
        items = [item for item in items if 
                search in item.title.lower() or 
                search in item.location.lower() or 
                search in item.description.lower()]
    
    return jsonify([{
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "type": item.type,
        "location": item.location,
        "email": item.email,
        "date": item.date or item.created_at.strftime('%B %d'),
        "status": item.status,
        "created_at": item.created_at.isoformat()
    } for item in items])

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    # READ operation - Get specific item by ID
    item = Item.query.get_or_404(item_id)
    
    return jsonify({
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "type": item.type,
        "location": item.location,
        "address": item.address,
        "city": item.city,
        "zip_code": item.zip_code,
        "email": item.email,
        "date": item.date,
        "status": item.status,
        "created_at": item.created_at.isoformat()
    })

@app.route('/api/items', methods=['POST'])
def create_item():
    # CREATE operation - Add new item to database
    data = request.get_json()
    
    required_fields = ['title', 'description', 'type', 'address', 'city', 'zipCode', 'email']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    if data['type'] not in ['lost', 'found']:
        return jsonify({"error": "Type must be 'lost' or 'found'"}), 400
    
    location = f"{data['address']}, {data['city']} {data['zipCode']}"
    current_date = datetime.now().strftime('%B %d')
    
    new_item = Item(
        title=data['title'],
        description=data['description'],
        type=data['type'],
        location=location,
        address=data['address'],
        city=data['city'],
        zip_code=data['zipCode'],
        email=data['email'],
        date=current_date
    )
    
    db.session.add(new_item)
    db.session.commit()
    
    return jsonify({
        "message": f"{data['type'].capitalize()} item created successfully",
        "item": {
            "id": new_item.id,
            "title": new_item.title,
            "description": new_item.description,
            "type": new_item.type,
            "location": new_item.location,
            "email": new_item.email,
            "date": new_item.date,
            "status": new_item.status
        }
    }), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    # UPDATE operation - Modify existing item
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    
    if 'title' in data:
        item.title = data['title']
    if 'description' in data:
        item.description = data['description']
    if 'status' in data:
        item.status = data['status']
    if 'email' in data:
        item.email = data['email']
    
    db.session.commit()
    
    return jsonify({
        "message": "Item updated successfully",
        "item": {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "type": item.type,
            "location": item.location,
            "email": item.email,
            "date": item.date,
            "status": item.status
        }
    })

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    # DELETE operation - Remove item from database
    item = Item.query.get_or_404(item_id)
    item_title = item.title
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({
        "message": f"Item '{item_title}' deleted successfully"
    })

# Report Management Routes
@app.route('/api/reports', methods=['GET'])
def get_reports():
    reports = Report.query.order_by(Report.submitted_at.desc()).all()
    
    return jsonify([{
        "id": report.id,
        "title": report.title,
        "type": report.type,
        "address": report.address,
        "city": report.city,
        "zip_code": report.zip_code,
        "description": report.description,
        "email": report.email,
        "submitted_at": report.submitted_at.isoformat()
    } for report in reports])

@app.route('/api/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    
    required_fields = ['title', 'type', 'address', 'city', 'zipCode', 'description', 'email']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    new_report = Report(
        title=data['title'],
        type=data['type'],
        address=data['address'],
        city=data['city'],
        zip_code=data['zipCode'],
        description=data['description'],
        email=data['email']
    )
    
    db.session.add(new_report)
    db.session.commit()
    
    return jsonify({
        "message": "Report submitted successfully",
        "report": {
            "id": new_report.id,
            "title": new_report.title,
            "type": new_report.type,
            "submitted_at": new_report.submitted_at.isoformat()
        }
    }), 201

# Statistics and Analytics Routes
@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_items = Item.query.count()
    lost_items = Item.query.filter_by(type='lost').count()
    found_items = Item.query.filter_by(type='found').count()
    active_items = Item.query.filter_by(status='active').count()
    resolved_items = Item.query.filter_by(status='resolved').count()
    
    latest_item = Item.query.order_by(Item.created_at.desc()).first()
    
    return jsonify({
        "total_items": total_items,
        "lost_items": lost_items,
        "found_items": found_items,
        "active_items": active_items,
        "resolved_items": resolved_items,
        "latest_item": {
            "id": latest_item.id,
            "title": latest_item.title,
            "type": latest_item.type,
            "location": latest_item.location,
            "date": latest_item.date
        } if latest_item else None
    })

@app.route('/api/search', methods=['GET'])
def search_items():
    query = request.args.get('q', '').lower()
    item_type = request.args.get('type')
    
    if not query:
        return jsonify([])
    
    items_query = Item.query
    
    if item_type and item_type in ['lost', 'found']:
        items_query = items_query.filter_by(type=item_type)
    
    items = items_query.all()
    
    filtered_items = []
    for item in items:
        if (query in item.title.lower() or 
            query in item.description.lower() or 
            query in item.location.lower()):
            filtered_items.append({
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "type": item.type,
                "location": item.location,
                "email": item.email,
                "date": item.date,
                "status": item.status
            })
    
    return jsonify(filtered_items)

def init_sample_data():
    if User.query.first():
        print("Sample data already exists")
        return
    
    print("Initializing sample data...")
    
    sample_users = [
        User(username='user', password='password', email='user@example.com'),
        User(username='admin', password='admin123', email='admin@example.com'),
        User(username='jiani', password='student123', email='jianiwang2024@u.northwestern.edu')
    ]
    
    for user in sample_users:
        db.session.add(user)
    
    sample_items = [
        Item(
            title='Black Umbrella',
            description='Black umbrella found near entrance',
            type='found',
            location='Pritzker Legal Research Center',
            address='Northwestern University',
            city='Evanston',
            zip_code='60208',
            email='finder@example.com',
            date='July 5'
        ),
        Item(
            title='Blue Jacket',
            description='Blue denim jacket, size M',
            type='lost',
            location='356-350 E Chicago Ave',
            address='356 E Chicago Ave',
            city='Chicago',
            zip_code='60611',
            email='owner@example.com',
            date='July 3'
        ),
        Item(
            title='iPhone 13',
            description='Black iPhone 13 with cracked screen protector',
            type='lost',
            location='Kellogg School of Management',
            address='2211 Campus Dr',
            city='Evanston',
            zip_code='60208',
            email='student@northwestern.edu',
            date='July 1'
        )
    ]
    
    for item in sample_items:
        db.session.add(item)
    
    sample_report = Report(
        title='Lost Wallet',
        type='lost',
        address='Northwestern University',
        city='Evanston',
        zip_code='60208',
        description='Brown leather wallet with student ID',
        email='report@northwestern.edu'
    )
    
    db.session.add(sample_report)
    db.session.commit()
    print("Sample data initialized successfully")

def demonstrate_basic_queries():
    """Lab 5 Step 2: Write basic SQL queries - Demonstrate database query operations"""
    print("\nLab 5: SQL Queries Demonstration")
    print("=" * 50)
    
    try:
        # Basic COUNT query - equivalent to SELECT COUNT(*) FROM items
        total_items = Item.query.count()
        print(f"1. Total items: {total_items}")
        
        # GROUP BY equivalent - equivalent to SELECT type, COUNT(*) FROM items GROUP BY type
        lost_count = Item.query.filter_by(type='lost').count()
        found_count = Item.query.filter_by(type='found').count()
        print(f"2. Lost items: {lost_count}, Found items: {found_count}")
        
        # WHERE clause with date filtering - equivalent to SELECT * FROM items WHERE created_at >= date
        recent_items = Item.query.filter(Item.created_at >= datetime.utcnow() - timedelta(days=30)).count()
        print(f"3. Recent items (30 days): {recent_items}")
        
        # GROUP BY city with counting - equivalent to SELECT city, COUNT(*) FROM items GROUP BY city
        city_stats = db.session.query(Item.city, func.count(Item.id)).group_by(Item.city).all()
        print("4. Items by city:")
        for city, count in city_stats:
            print(f"   {city}: {count}")
        
        # Status filtering - equivalent to SELECT * FROM items WHERE status = 'active'
        active_items = Item.query.filter_by(status='active').count()
        print(f"5. Active items: {active_items}")
        
        # Text search - equivalent to SELECT * FROM items WHERE title ILIKE '%umbrella%'
        umbrella_items = Item.query.filter(Item.title.ilike('%umbrella%')).count()
        print(f"6. Items with 'umbrella': {umbrella_items}")
        
        print("\nCRUD Operations Working:")
        print(f"   CREATE: New items can be added via POST /api/items")
        print(f"   READ: Items retrieved via GET /api/items")
        print(f"   UPDATE: Items updated via PUT /api/items/<id>")  
        print(f"   DELETE: Items deleted via DELETE /api/items/<id>")
        
        print("\nDatabase Schema Created:")
        print(f"   users table: {User.query.count()} records")
        print(f"   items table: {Item.query.count()} records")
        print(f"   reports table: {Report.query.count()} records")
        
        print("\nLab 5 Requirements Completed Successfully!")
        
    except Exception as e:
        print(f"Error in queries: {e}")

if __name__ == '__main__':
    print("Lost & Found API - Programming Lab 5")
    print("Author: Jiani Wang")
    print("Course: ACIS 498: Information Systems Capstone")
    print("Database: PostgreSQL with Flask-SQLAlchemy")
    print("-" * 50)
    
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
            
            init_sample_data()
            demonstrate_basic_queries()
            
            print("\nFlask API Server starting...")
            print("Available at: http://localhost:5001")
            
        except Exception as e:
            print(f"Setup error: {e}")
            exit(1)
    
    app.run(debug=True, host='0.0.0.0', port=5001)