# Check if API is running
curl http://localhost:5001/

# GET /api/users
curl http://localhost:5001/api/users

# POST /api/users
curl -X POST http://localhost:5001/api/users \
     -H "Content-Type: application/json" \
     -d '{
           "username": "jiani_test",
           "password": "test123",
           "email": "jiani_test@example.com"
         }'

# POST /api/login
curl -X POST http://localhost:5001/api/login \
     -H "Content-Type: application/json" \
     -d '{
           "username": "jiani_test",
           "password": "test123"
         }'

# GET /api/items
curl http://localhost:5001/api/items
curl "http://localhost:5001/api/items?type=lost"
curl "http://localhost:5001/api/items?search=iphone"

# GET /api/items/<id>
curl http://localhost:5001/api/items/3

# POST /api/items
curl -X POST http://localhost:5001/api/items \
     -H "Content-Type: application/json" \
     -d '{
           "title": "iPad Pro",
           "description": "Left it in Tech LR5",
           "type": "lost",
           "address": "2145 Sheridan Rd",
           "city": "Evanston",
           "zipCode": "60208",
           "email": "ipadowner@northwestern.edu"
         }'

# Get API statistics
curl http://localhost:5001/api/stats

# Create a new user
curl -X POST http://localhost:5001/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "newpass123",
    "email": "newuser@example.com"
  }'

# Create a lost item
curl -X POST http://localhost:5001/api/items \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Lost iPhone",
    "description": "Black iPhone 14 with blue case",
    "type": "lost",
    "address": "Northwestern University",
    "city": "Evanston",
    "zipCode": "60208",
    "email": "student@northwestern.edu"
  }'

# Create a found item
curl -X POST http://localhost:5001/api/items \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Found Keys",
    "description": "Set of house keys with red keychain",
    "type": "found",
    "address": "Main Library",
    "city": "Evanston",
    "zipCode": "60208",
    "email": "finder@northwestern.edu"
  }'

# Get all items
curl http://localhost:5001/api/items

# Get only found items
curl http://localhost:5001/api/items?type="found"

# Get specific item by ID
curl http://localhost:5001/api/items/1

# Update item status
curl -X PUT http://localhost:5001/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved"
  }'

# Delete an item
curl -X DELETE http://localhost:5001/api/items/1

# User Authentication
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user",
    "password": "password"
  }'

# Search items
curl "http://localhost:5001/api/search?q=iPhone"

# Search with type filter
curl "http://localhost:5001/api/search?q=phone&type=lost"

# Create a report
curl -X POST http://localhost:5001/api/reports \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Lost Wallet",
    "type": "lost",
    "address": "Student Center",
    "city": "Evanston",
    "zipCode": "60208",
    "description": "Brown leather wallet with ID cards",
    "email": "student@northwestern.edu"
  }'

# Test validation errors
# Missing required fields
curl -X POST http://localhost:5001/api/items \
  -H "Content-Type: application/json" \
  -d '{"title":"Incomplete Item"}'

# Invalid item type
curl -X POST http://localhost:5001/api/items \
  -H "Content-Type: application/json" \
  -d '{"title":"Invalid Type","description":"Test","type":"invalid","address":"Test","city":"Test","zipCode":"12345","email":"test@test.com"}'

# GET /api/stats
curl http://localhost:5001/api/stats
