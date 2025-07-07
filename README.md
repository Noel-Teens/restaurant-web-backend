---
title: Restaurant Backend API
emoji: 🍽️
colorFrom: orange
colorTo: red
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 🍽️ Restaurant Backend API

A comprehensive Django REST API for restaurant management with user authentication, menu management, ordering system, reservations, and reviews.

## 🚀 Features

### 🔐 Authentication System
- User registration and login
- Admin authentication with enhanced permissions
- JWT-based authentication
- Role-based access control

### 🍽️ Menu Management
- Public menu browsing
- Admin menu item management (CRUD operations)
- Image upload support for menu items
- Availability status tracking

### 🛒 Ordering System
- Direct cart checkout
- Order history tracking
- Automatic order status management
- Price preservation at time of order

### 🪑 Reservation System
- User reservation creation
- Admin approval/rejection workflow
- Table assignment and availability checking
- Conflict prevention for double bookings

### ⭐ Review System
- Order-based reviews (one review per order)
- User can only review their own orders
- Public review viewing with pagination
- Admin moderation capabilities

### 👨‍💼 Admin Dashboard
- User management (view, delete, bulk operations)
- Menu management
- Reservation management
- Review moderation

## 📡 API Endpoints (26 Total)

### Public Endpoints (5)
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/admin-login/` - Admin login
- `GET /api/menu/` - Browse menu items
- `GET /api/reviews/` - View public reviews

### Protected Endpoints (8)
- `GET /api/auth/profile/` - User profile
- `POST /api/reservation/` - Create reservation
- `GET /api/reservations/` - User reservations
- `POST /api/checkout/` - Cart checkout
- `GET /api/orders/` - Order history
- `POST /api/review/` - Create review

### Admin Endpoints (14)
- `GET /api/admin/users/` - List all users
- `GET /api/admin/users/{id}/` - User details
- `DELETE /api/admin/users/{id}/` - Delete user
- `POST /api/admin/users/bulk-delete/` - Bulk delete users
- `POST /api/admin/menu/` - Add menu item
- `GET /api/admin/menu/all/` - List all menu items
- `DELETE /api/admin/menu/{id}/` - Delete menu item
- `GET /api/admin/reviews/` - List all reviews
- `DELETE /api/admin/review/{id}/` - Delete review
- `GET /api/admin/reservations/` - All reservations
- `GET /api/admin/reservations/pending/` - Pending reservations
- `GET /api/admin/reservations/available-tables/` - Check table availability
- `POST /api/admin/reservations/{id}/approve/` - Approve reservation
- `POST /api/admin/reservations/{id}/reject/` - Reject reservation

## 🧪 Demo Credentials

### Admin Account
- **Email**: `admin@restaurant.com`
- **Password**: `admin123`

### Test User Account
- **Email**: `test@example.com`
- **Password**: `testpassword123`

## 📖 Quick Start

### 1. Browse Menu (Public)
```bash
curl https://your-space-url.hf.space/api/menu/
```

### 2. User Login
```bash
curl -X POST https://your-space-url.hf.space/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### 3. Cart Checkout (Authenticated)
```bash
curl -X POST https://your-space-url.hf.space/api/checkout/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"menu_item_id": 1, "quantity": 2},
      {"menu_item_id": 2, "quantity": 1}
    ],
    "special_instructions": "Extra spicy please"
  }'
```

### 4. Create Reservation (Authenticated)
```bash
curl -X POST https://your-space-url.hf.space/api/reservation/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reservation_date": "2025-07-20",
    "reservation_time": "18:00:00",
    "party_size": 4,
    "special_requests": "Window seat preferred"
  }'
```

### 5. Admin Login
```bash
curl -X POST https://your-space-url.hf.space/api/auth/admin-login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@restaurant.com",
    "password": "admin123"
  }'
```

## 🏗️ Architecture

### Database Models
- **User**: Custom user model with email authentication
- **MenuItem**: Restaurant menu items with images and pricing
- **OrderHistory**: Customer orders with status tracking
- **OrderItem**: Individual items within orders
- **TableReservation**: Restaurant table reservations
- **Review**: Customer reviews linked to orders

### Key Relationships
- User → Orders (1:many)
- User → Reservations (1:many)
- User → Reviews (1:many)
- Order → Review (1:1, optional)
- Order → OrderItems (1:many)
- MenuItem → OrderItems (1:many)

## 🔧 Technical Stack

- **Framework**: Django 5.2 + Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (auto-configured)
- **Image Processing**: Pillow
- **CORS**: django-cors-headers for frontend integration

## 📱 Frontend Ready

This backend provides:
- ✅ Complete CORS support
- ✅ Detailed error messages
- ✅ Consistent JSON response formats
- ✅ File upload support for menu images
- ✅ Pagination for large datasets
- ✅ JWT authentication
- ✅ Role-based access control

## 📋 Sample Data Included

- 🍕 9 menu items (Pizza, Salad, Chicken, Pasta, etc.)
- 👤 Admin and test user accounts
- 🔧 Ready-to-use API endpoints

## 🧪 Testing

The deployment includes comprehensive test scripts that verify:
- ✅ User authentication and registration
- ✅ Menu browsing and management
- ✅ Cart checkout functionality
- ✅ Order history tracking
- ✅ Review system (order-based)
- ✅ Reservation management
- ✅ Admin dashboard operations

## 📚 Documentation

Complete API documentation with request/response examples is available in the repository.

## 🚀 Production Ready

This API is containerized and ready for:
- Hugging Face Spaces (current deployment)
- Docker containers
- Cloud platforms (AWS, GCP, Azure)
- Traditional hosting services

---

**Built with Django REST Framework** 🐍 **Deployed on Hugging Face Spaces** 🤗

*Perfect for restaurant web applications, food delivery apps, or learning Django REST API development!*
