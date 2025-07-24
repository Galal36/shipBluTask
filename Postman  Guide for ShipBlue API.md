Important to know / Hints:
first you have to create a env and use pip install -r requriements.txt
-database used is postgres
-For testing apis I used postman
-I tried to put the most important part of the logic in models instead of views to be reusable(best practice).
- I used jwt or json web token, so every 5 minutes, the user will have to get another token again using http://127.0.0.1:8001/api/token/
with enabling POST {"username":"jalal","password":"adminPass123"} which is the only admin user
- admin user can create users,orders(such as status) or update, list all, or even delete with no priviles. Unlike normal user which can just now his OrderTracking or his customer details. 
- Authentication and autheroization are both applied.
-I tried to put some constraints in the serilizers files for each app
- for rate limiting and forbid attackers I used to use throttle-class to limit how many requests a user or ip can send.
-tried to avoid reduncancy and bad quality code to save computer's power/memory.
-pagination exists(the bonus)
- tried to validate and test most cases/errors expected from the users such as creating a new order with validation for unique tracking_number



# Postman Authentication Guide for ShipBlue API

## Step-by-Step Authentication Process

### Step 1: Obtain JWT Token

1. **Create a new POST request in Postman**
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/token/`

2. **Set Headers**
   - `Content-Type: application/json`

3. **Set Request Body**
   - Select `raw` and `JSON` format
   - Enter the following JSON:
   ```json
   {
     "username": "adminJalal",
     "password": "adminpassword123"
   }
   ```

4. **Send the request**
   - Click "Send"
   - You should receive a response like:
   ```json
   {
     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
   }
   ```

5. **Copy the access token**
   - Copy the value of the `access` field (without quotes)

### Step 2: Use Token for Authenticated Requests

For all subsequent API requests that require authentication:

1. **Add Authorization Header**
   - Go to the `Headers` tab in your request
   - Add a new header:
     - Key: `Authorization`
     - Value: `Bearer YOUR_ACCESS_TOKEN_HERE`
   
   Example:
   ```
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyNzg5MjAwLCJpYXQiOjE2NDI3ODg5MDAsImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoxfQ.abc123def456
   ```

### Step 3: Test Authentication

**Test with a protected endpoint:**

1. **Create Customer (Admin Only)**
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/customers/`
   - Headers:
     - `Content-Type: application/json`
     - `Authorization: Bearer YOUR_ACCESS_TOKEN`
   - Body (raw JSON):
   ```json
   {
     "name": "Ahmed Mohamed",
     "phone": "01234567890"
   }
   ```

## Complete API Testing Workflow

### 1. Authentication
```
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
  "username": "adminJalal",
  "password": "adminpassword123"
}
```

### 2. Create Customer
```
POST http://127.0.0.1:8000/api/customers/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "name": "Ahmed Mohamed",
  "phone": "01234567890"
}
```

### 3. List Customers
```
GET http://127.0.0.1:8000/api/customers/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 4. Create Order
```
POST http://127.0.0.1:8000/api/orders/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "tracking_number": "SB001",
  "customer": 1,
  "status": "Created"
}
```

### 5. List Orders
```
GET http://127.0.0.1:8000/api/orders/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 6. Update Order Status
```
PATCH http://127.0.0.1:8000/api/orders/1/status/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "status": "Picked"
}
```

### 7. Get Order Tracking History
```
GET http://127.0.0.1:8000/api/tracking/1/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Token Management

### Token Expiration
- Access tokens expire after 5 minutes (configurable in settings)
- When a token expires, you'll get a 401 Unauthorized response
- You can either:
  1. Get a new token using the `/api/token/` endpoint
  2. Use the refresh token to get a new access token

### Refresh Token
```
POST http://127.0.0.1:8000/api/token/refresh/
Content-Type: application/json

{
  "refresh": "YOUR_REFRESH_TOKEN_HERE"
}
```

## Postman Collection Setup

### Option 1: Manual Setup
Follow the steps above for each request.

### Option 2: Environment Variables
1. Create a new environment in Postman
2. Add variables:
   - `base_url`: `http://127.0.0.1:8000`
   - `access_token`: (leave empty initially)
3. Use `{{base_url}}` and `{{access_token}}` in your requests
4. After getting the token, manually update the `access_token` variable

### Option 3: Pre-request Script (Advanced)
Add this to your collection's pre-request script to automatically handle authentication:

```javascript
// Check if we have a valid token
if (!pm.environment.get("access_token")) {
    // Get new token
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/token/",
        method: 'POST',
        header: {
            'Content-Type': 'application/json'
        },
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                username: "adminJalal",
                password: "adminpassword123"
            })
        }
    }, function (err, response) {
        if (response.code === 200) {
            var jsonData = response.json();
            pm.environment.set("access_token", jsonData.access);
        }
    });
}
```

## Troubleshooting

### Common Issues:

1. **401 Unauthorized**
   - Token expired or invalid
   - Solution: Get a new token

2. **403 Forbidden**
   - User doesn't have permission
   - Solution: Make sure you're using admin credentials

3. **400 Bad Request**
   - Invalid request format
   - Solution: Check JSON syntax and required fields

4. **Connection Refused**
   - Django server not running
   - Solution: Run `python manage.py runserver`

### User Accounts Available:

**Admin User (Full Access):**
- Username: `adminJalal`
- Password: `adminpassword123`

**Normal User (Limited Access):**
- Username: `normalUser`
- Password: `userpassword123`

