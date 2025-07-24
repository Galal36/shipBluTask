# ShipBlue Order Management System - Project Details

## Important Notes / Hints

*   **Environment Setup**: First, you have to create a virtual environment and use `pip install -r requirements.txt`.
*   **Database**: The database used is **PostgreSQL**. 
*   **API Testing**: For testing APIs, **Postman** was used.
*   **Logic Location**: I tried to put the most important part of the logic in **models** instead of views to be reusable (*best practice*).
*   **Authentication (JWT)**: I used **JWT (JSON Web Token)**. Please note that access tokens expire after a certain period (e.g., 5 minutes), so the user will have to get another token again using `http://127.0.0.1:8000/api/token/`.
    *   **Admin User**: `jalal` with password `adminPass123` has **full privileges** (can create users, orders, update status, list all, or even delete).
    *   **Normal User**: `normalUser` with password `normalpassword123` is permitted just to **read (GET methods)** and cannot perform delete/update operations. They can only access their own `OrderTracking` or `Customer` details(I applied authorization concept).
*   **Authorization**: Both authentication and authorization concepts are applied.
*   **Serializers**: I tried to put some constraints in the serializer files for each app.
*   **Rate Limiting**: For rate limiting and to forbid attackers, I used `throttle_classes` to limit how many requests a user or IP can send.
*   **Code Quality**: I tried to avoid redundancy and bad quality code to save computer's power/memory.
*   **Pagination**: Pagination exists (a *bonus feature*).Pagination
*   **Validation & Error Handling**: I tried to validate and test most cases/errors expected from the users, such as creating a new order with validation for a unique `tracking_number`.
### consider these mock data to save time!
## Postman Authentication & API Testing Guide

This section provides a step-by-step guide on how to authenticate and test the API endpoints using Postman.

### Step 1: Obtain JWT Token 
### Consider these data to save time!

1.  **Create a new POST request in Postman**
    *   **Method**: `POST`
    *   **URL**: `http://127.0.0.1:8000/api/token/`

2.  **Set Headers**
    *   `Content-Type: application/json` => always consider that

3.  **Set Request Body**
    *   Select `raw` and `JSON` format
    *   Enter the following JSON for **Admin User**:
    ```json
    {
      "username": "jalal",
      "password": "adminPass123"
    }
    ```
    *   Or for **Normal User**:
    ```json
    {
      "username": "normalUser",
      "password": "normalpassword123"
    }
    ```

4.  **Send the request**
    *   Click "Send"
    *   You should receive a response like:
    ```json
    {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
    ```

5.  **Copy the access token**
    *   Copy the value of the `access` field (without quotes).

### Step 2: Use Token for Authenticated Requests

For all subsequent API requests that require authentication:

1.  **Add Authorization Header**
    *   Go to the `Headers` tab in your request
    *   Add a new header:
        *   **Key**: `Authorization`
        *   **Value**: `Bearer YOUR_ACCESS_TOKEN_HERE`

    **Example**:
    ```
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyNzg5MjAwLCJpYXQiOjE2NDI3ODg5MDAsImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoxfQ.abc123def456
    ```

### Step 3: Test Authentication

**Test with a protected endpoint (using Admin Token):**

1.  **Create Customer (Admin Only)**
    *   **Method**: `POST`
    *   **URL**: `http://127.0.0.1:8000/api/customers/`
    *   **Headers**:
        *   `Content-Type: application/json`
        *   `Authorization: Bearer YOUR_ACCESS_TOKEN`
    *   **Body** (raw JSON):
    ```json
    {
      "name": "Ahmed Mohamed",
      "phone": "01234567890"
    }
    ```
Note Try to enter same data twice like ahmed with same phone number, error appears(Error Validation/handling)
## Complete API Testing Workflow Examples

### 1. Authentication
```
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
  "username": "jalal",
  "password": "adminPass123"
}
```

### 2. Create Customer (Admin Only)
```
POST http://127.0.0.1:8000/api/customers/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "name": "Ahmed Mohamed",
  "phone": "01234567890"
}
```

### 3. List Customers (Admin: all, Normal User: only their own if linked)
```
GET http://127.0.0.1:8000/api/customers/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 4. Create Order (Admin Only)
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

### 5. List Orders (Admin: all, Normal User: only their own)
```
GET http://127.0.0.1:8000/api/orders/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 6. Update Order Status (Admin Only)
```
PATCH http://127.0.0.1:8000/api/orders/1/status/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "status": "Picked"
}
```

### 7. Get Order Tracking History (Admin: any, Normal User: only their own orders)
```
GET http://127.0.0.1:8000/api/tracking/1/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Token Management

### Token Expiration
*   Access tokens expire after a configured time (default 5 minutes).
*   When a token expires, requests will return `401 Unauthorized`.
*   You can obtain a new access token using the refresh token or by re-authenticating with username/password.

### Refresh Token
```
POST http://127.0.0.1:8000/api/token/refresh/
Content-Type: application/json

{
  "refresh": "YOUR_REFRESH_TOKEN_HERE"
}
```
## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Customers (Admin only)
- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create new customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

### Orders
- `GET /api/orders/` - List orders (admin sees all, users see their own)
- `POST /api/orders/` - Create new order (admin only)
- `GET /api/orders/{id}/` - Get order details
- `PUT /api/orders/{id}/` - Update order (admin only)
- `DELETE /api/orders/{id}/` - Delete order (admin only)
- `PATCH /api/orders/{id}/status/` - Update order status (admin only)

### Order Tracking
- `GET /api/tracking/{order_id}/` - Get tracking history for an order
- `GET /api/tracking/{id}/detail/` - Get specific tracking event details

## Status Transitions

Orders follow a strict status transition flow:
- Created → Picked
- Picked → Shipped
- Shipped → Delivered
- Delivered (final state)

## Installation & Setup

1. **Create virtual environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   # Username: adminJalal
   # Password: adminpassword12
## Video Demo

=> A video demo will be provided for the API testing.




## Project Structure

```
├── Cus_Ord_Tracking/          # Main project settings
├── Customer/                  # Customer app
├── Order/                     # Order app
├── OrderTracking/             # Order tracking app
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

