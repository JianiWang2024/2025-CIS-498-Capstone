# Programming Lab 4: Set up a Flask project for API development in Python environment
from flask import Flask, request, jsonify  # Flask core imports for API
from flask_cors import CORS  # Enable cross-origin requests
from datetime import datetime  # For timestamping
import uuid  # For unique IDs
import functools  # For decorators

# Programming Lab 4: Flask Project Setup
app = Flask(__name__)
CORS(app)

# In-memory data store (temporary, will use DB in Lab 5)
users = {}
items = [
    {
        'id': str(uuid.uuid4()),
        'title': 'Black Umbrella',
        'location': 'Pritzker Legal Research Center',
        'date': 'July 5',
        'type': 'found',
        'description': 'Black umbrella found near entrance',
        'email': 'finder@example.com',
        'created_at': datetime.now().isoformat()
    },
    {
        'id': str(uuid.uuid4()),
        'title': 'Blue Jacket',
        'location': '356-350 E Chicago Ave',
        'date': 'July 3',
        'type': 'lost',
        'description': 'Blue denim jacket, size M',
        'email': 'owner@example.com',
        'created_at': datetime.now().isoformat()
    }
]

# Programming Lab 4: Improve python code to handle errors and format API responses
def handle_errors(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except KeyError as e:
            return jsonify({'error': f'Missing field: {str(e)}'}), 400
        except ValueError as e:
            return jsonify({'error': f'Invalid value: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    return wrapper

def validate_item_data(data):
    required_fields = ['title', 'location', 'type', 'description', 'email']
    for field in required_fields:
        if field not in data or not data[field].strip():
            raise ValueError(f'{field} is required')
    if data['type'] not in ['lost', 'found']:
        raise ValueError('type must be "lost" or "found"')
    if '@' not in data['email'] or '.' not in data['email']:
        raise ValueError('Invalid email')

def format_response(data, message=None, status_code=200):
    response = {'data': data}
    if message:
        response['message'] = message
    return jsonify(response), status_code

# Programming Lab 4: Creating and managing API routes in Flask
@app.route('/api/auth/login', methods=['POST'])
@handle_errors
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    username = data['username']
    password = data['password']
    valid_users = {'user': 'password', 'admin': '123456'}
    if username in valid_users and valid_users[username] == password:
        user_info = {
            'id': str(uuid.uuid4()),
            'username': username,
            'login_time': datetime.now().isoformat()
        }
        users[username] = user_info
        return format_response({'user': user_info, 'token': 'demo_token_' + username}, 'Login successful')
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/register', methods=['POST'])
@handle_errors
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    username = data['username']
    password = data['password']
    if username in users:
        return jsonify({'error': 'Username exists'}), 409
    user_info = {
        'id': str(uuid.uuid4()),
        'username': username,
        'password': password,
        'created_at': datetime.now().isoformat()
    }
    users[username] = user_info
    response_user = {k: v for k, v in user_info.items() if k != 'password'}
    return format_response({'user': response_user}, 'User registered', 201)

@app.route('/api/auth/logout', methods=['POST'])
@handle_errors
def logout():
    return format_response(None, 'Logout successful')

# Programming Lab 4: Develop REST APIs to implement CRUD operations in Flask
@app.route('/api/items', methods=['GET'])
@handle_errors
def get_items():
    item_type = request.args.get('type')
    search_term = request.args.get('search', '').lower()
    filtered_items = items
    if item_type in ['lost', 'found']:
        filtered_items = [item for item in filtered_items if item['type'] == item_type]
    if search_term:
        filtered_items = [item for item in filtered_items if search_term in item['title'].lower() or search_term in item['location'].lower() or search_term in item['description'].lower()]
    return format_response(filtered_items, f'{len(filtered_items)} items retrieved')

@app.route('/api/items/<item_id>', methods=['GET'])
@handle_errors
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return format_response(item, 'Item retrieved')

@app.route('/api/items', methods=['POST'])
@handle_errors
def create_item():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    validate_item_data(data)
    new_item = {
        'id': str(uuid.uuid4()),
        'title': data['title'].strip(),
        'location': data['location'].strip(),
        'type': data['type'],
        'description': data['description'].strip(),
        'email': data['email'].strip(),
        'date': data.get('date', datetime.now().strftime('%B %d')),
        'created_at': datetime.now().isoformat()
    }
    items.append(new_item)
    return format_response(new_item, 'Item created', 201)

@app.route('/api/items/<item_id>', methods=['PUT'])
@handle_errors
def update_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    index = next((i for i, item in enumerate(items) if item['id'] == item_id), None)
    if index is None:
        return jsonify({'error': 'Item not found'}), 404
    validate_item_data(data)
    items[index].update({
        'title': data['title'].strip(),
        'location': data['location'].strip(),
        'type': data['type'],
        'description': data['description'].strip(),
        'email': data['email'].strip(),
        'date': data.get('date', items[index]['date']),
        'updated_at': datetime.now().isoformat()
    })
    return format_response(items[index], 'Item updated')

@app.route('/api/items/<item_id>', methods=['DELETE'])
@handle_errors
def delete_item(item_id):
    index = next((i for i, item in enumerate(items) if item['id'] == item_id), None)
    if index is None:
        return jsonify({'error': 'Item not found'}), 404
    deleted = items.pop(index)
    return format_response({'deleted_item': deleted}, 'Item deleted')

@app.route('/api/stats', methods=['GET'])
@handle_errors
def get_stats():
    stats = {
        'total_items': len(items),
        'lost_items': len([i for i in items if i['type'] == 'lost']),
        'found_items': len([i for i in items if i['type'] == 'found']),
        'total_users': len(users),
        'last_updated': datetime.now().isoformat()
    }
    return format_response(stats, 'Stats retrieved')

@app.route('/api/health', methods=['GET'])
def health_check():
    return format_response({'status': 'healthy', 'timestamp': datetime.now().isoformat(), 'version': '1.0.0'}, 'API OK')

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal error'}), 500

if __name__ == '__main__':
    print("Lost & Found API Server Starting...")
    print("Endpoints:")
    print("GET    /api/health")
    print("POST   /api/auth/login")
    print("POST   /api/auth/register")
    print("POST   /api/auth/logout")
    print("GET    /api/items")
    print("GET    /api/items/<id>")
    print("POST   /api/items")
    print("PUT    /api/items/<id>")
    print("DELETE /api/items/<id>")
    print("GET    /api/stats")
    app.run(debug=True, host='127.0.0.1', port=5000)