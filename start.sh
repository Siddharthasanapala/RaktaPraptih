#!/bin/bash

# Django startup script for Render deployment
# Version: Modified for proper command separation

set -e  # Exit on any error

echo "Starting Django application deployment..."

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:10000 --workers 3 --timeout 120 RaktaPraptih.wsgi:application