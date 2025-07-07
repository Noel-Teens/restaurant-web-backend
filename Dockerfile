# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=restaurant_backend.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
        libffi-dev \
        libssl-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/media/menu_images \
    && mkdir -p /app/staticfiles \
    && mkdir -p /app/logs

# Set permissions
RUN chmod -R 755 /app/media \
    && chmod -R 755 /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Create database and run migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Create superuser and sample data
RUN python manage.py shell -c "
from django.contrib.auth import get_user_model
from restaurant_server.models import MenuItem
import os

User = get_user_model()

# Create superuser if it doesn't exist
if not User.objects.filter(email='admin@gmail.com').exists():
    User.objects.create_superuser(
        username='Admin',
        email='admin@gmail.com',
        password='admin@123',
        first_name='Restaurant',
        last_name='Admin'
    )
    print('Superuser created')
"

# Expose port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/api/menu/ || exit 1

# Start command
CMD ["python", "manage.py", "runserver", "0.0.0.0:7860"]
