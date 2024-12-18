# Sneaker Store API

A Django-based REST API for managing a sneaker store. This project provides endpoints for product management and shopping cart functionality.

## Features

- Product management (CRUD operations)
- Shopping cart functionality
- Token-based authentication
- Admin interface for easy management

## Setup

1. Clone the repository:
```bash
git clone https://github.com/suiunov/store.git
cd store
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

- `/api/products/` - Product listing and creation
- `/api/cart/` - Shopping cart management
- `/admin/` - Admin interface

## Authentication

The API uses token-based authentication. To get a token:

1. Create a user account
2. Use the admin interface to generate a token
3. Include the token in your requests:
   ```
   Authorization: Token your-token-here
   ```
