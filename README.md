# Restaurant Backend API

A comprehensive Django REST API backend for a restaurant web application with JWT authentication, order management, table reservations, and review systems.

## Overview

This Django-based backend provides a complete restaurant management system with three main applications:
- **Authentication App**: User registration, login, and profile management
- **Restaurant Server**: Menu items, orders, reservations, and reviews
- **Admin App**: Administrative functions for managing users, menu items, and reviews

## Features

### 🔐 Authentication System
- Custom user model with email-based authentication
- JWT (JSON Web Token) authentication
- User registration and login endpoints
- Secure password validation
- User profile management

### 🍽️ Menu Management
- Menu item creation with image support
- Food name, description, and pricing
- Availability status tracking
- Public menu viewing (no authentication required)

### 📋 Order System
- Complete order placement functionality
- Multiple menu items per order with quantities
- Automatic total calculation
- Order status tracking (pending → confirmed → preparing → ready → delivered)
- Special instructions support
- Order history for users

### 🪑 Table Reservations
- Date and time-based reservations
- Party size specification (1-20 people)
- Special requests handling
- Reservation status management
- Table number assignment by admin

### ⭐ Review System
- Order-based reviews (one review per order)
- 5-star rating system
- Detailed review descriptions
- Public review viewing with pagination
- Review management by admins

### 👨‍💼 Admin Features
- User management (view all registered users)
- Menu item management (add/delete items)
- Review moderation (view/delete reviews)
- Staff and superuser privilege system

## Technology Stack

- **Framework**: Django 5.2
- **API**: Django REST Framework
- **Authentication**: Simple JWT
- **Database**: SQLite (development)
- **Image Handling**: Pillow
- **CORS**: django-cors-headers

## Project Structure

```
restaurant_backend/
├── auth_app/                 # User authentication
│   ├── models.py            # Custom User model
│   ├── serializers.py       # User serializers
│   ├── views.py             # Auth endpoints
│   └── urls.py              # Auth URL patterns
├── restaurant_server/        # Restaurant operations
│   ├── models.py            # Menu, Order, Reservation, Review models
│   ├── serializers.py       # Restaurant serializers
│   ├── views.py             # Restaurant endpoints
│   ├── urls.py              # Restaurant URL patterns
│   └── management/          # Custom management commands
├── admin_app/               # Admin functionality
│   ├── views.py             # Admin endpoints
│   └── urls.py              # Admin URL patterns
├── restaurant_backend/       # Main project settings
│   ├── settings.py          # Django configuration
│   └── urls.py              # Main URL configuration
└── manage.py                # Django management script
```

## Database Models

### User Model
- Custom user with email as username field
- Username, email, first name, last name
- Creation date tracking
- Staff and admin privileges

### MenuItem Model
- Food image (optional)
- Food name and description
- Price with validation
- Availability status
- Creation and update timestamps

### OrderHistory Model
- User relationship
- Order date and total amount
- Order status tracking
- Special instructions
- Related order items

### OrderItem Model
- Junction table for orders and menu items
- Quantity and price at time of order
- Preserves historical pricing

### TableReservation Model
- User relationship
- Reservation date and time
- Party size (1-20 people)
- Table number assignment
- Special requests and status

### Review Model
- One-to-one relationship with orders
- User relationship
- Star rating (1-5)
- Review description
- Creation and update timestamps


## Installation & Setup

1. **Clone the repository**
   ```bash
   cd restaurant_backend
   ```

2. **Install dependencies**
   ```bash
   pip install djangorestframework djangorestframework-simplejwt django-cors-headers Pillow
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```


## Authentication

The API uses JWT authentication. After login or registration, include the access token in requests:

```
Authorization: Bearer <access_token>
```

Tokens expire in 60 minutes and can be refreshed using the refresh token.

## Admin Interface

Access the Django admin interface at `http://127.0.0.1:8000/admin/` to manage:
- Users and their details
- Menu items with images
- Orders and order items
- Table reservations
- Reviews and ratings

## Security Features

- JWT-based authentication
- Password validation
- CORS configuration for frontend integration
- Admin-only endpoints protection
- Input validation and sanitization
- Secure file upload handling

## API Response Format

All endpoints return JSON responses with appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found

Error responses include descriptive messages for debugging and user feedback.

## Development Features

- Debug mode enabled for development
- Media file serving for uploaded images
- CORS headers for frontend integration
- Comprehensive error handling
- Pagination support for large datasets
- Automatic timestamp tracking
