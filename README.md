# ShipBlue Order Management System

A Django REST framework project for ShipBlue, an Egyptian shipping company, focused on order management, tracking, and customer management with JWT authentication.

## Features

- **Customer Management**: Create and manage customers with validation for Egyptian phone numbers and names
- **Order Management**: Create, list, update, delete orders with status tracking
- **Order Tracking**: Track order status history with timestamps and comments
- **JWT Authentication**: Secure API access with JSON Web Tokens
- **Role-based Permissions**: Admin users (adminJalal) have full access, regular users can only view their own orders
- **Pagination**: Paginated API responses for better performance
- **Filtering & Search**: Filter orders by status, customer name, and search functionality
- **Rate Limiting**: Throttling to control API usage
- **Validation**: Proper validation for phone numbers, customer names, and order status transitions

## Models

### Customer
- `id`: Auto-generated primary key
- `user`: Foreign key to Django User model (optional)
- `name`: Customer name (validated to not contain numbers)
- `phone`: Egyptian phone number (validated with regex: `01[0-9]{9}`)

### Order
- `id`: Auto-generated primary key
- `tracking_number`: Unique tracking identifier
- `customer`: Foreign key to Customer
- `status`: Order status (Created, Picked, Shipped, Delivered)
- `created_at`: Timestamp when order was created
- `updated_at`: Timestamp when order was last updated

### OrderTrackingEvent
- `id`: Auto-generated primary key
- `order`: Foreign key to Order
- `status`: Status at this tracking event
- `timestamp`: When the status change occurred
- `comment`: Description of the status change

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
   # Password: adminpassword123
   ```

5. **Run development server**:
   ```bash
   python manage.py runserver
   ```

## User Accounts

### Admin User
- **Username**: adminJalal
- **Password**: adminpassword123
- **Permissions**: Full access to all endpoints

### Normal User
- **Username**: normalUser
- **Password**: userpassword123
- **Permissions**: Can only view their own order details

## Testing with Postman

1. **Get JWT Token**:
   ```
   POST /api/token/
   {
     "username": "adminJalal",
     "password": "adminpassword123"
   }
   ```

2. **Use Token in Headers**:
   ```
   Authorization: Bearer <your_access_token>
   ```

3. **Create Customer**:
   ```
   POST /api/customers/
   {
     "name": "Ahmed Mohamed",
     "phone": "01234567890"
   }
   ```

4. **Create Order**:
   ```
   POST /api/orders/
   {
     "tracking_number": "SB001",
     "customer": 1,
     "status": "Created"
   }
   ```

5. **Update Order Status**:
   ```
   PATCH /api/orders/1/status/
   {
     "status": "Picked"
   }
   ```

## Configuration

The project is configured to use SQLite for development. For production with PostgreSQL, update the `DATABASES` setting in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'order_tracking_db',
        'USER': 'postgres',
        'PASSWORD': 'myPass123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Security Features

- JWT authentication with configurable token lifetime
- Rate limiting (100 requests/day for anonymous, 1000/day for authenticated users)
- Input validation and sanitization
- CSRF protection
- Proper permission classes for role-based access



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

