#!/bin/bash
# scripts/start.sh - Production startup script

set -e

echo "🚀 Starting RaktaPraptih application..."

# Function to wait for database to be ready
wait_for_db() {
    echo "⏳ Waiting for database to be ready..."
    python << END
import sys
import time
import psycopg2
import os

def wait_for_db():
    db_conn = None
    while not db_conn:
        try:
            db_conn = psycopg2.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                port=os.environ.get('DB_PORT', '5432'),
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASSWORD', ''),
                dbname=os.environ.get('DB_NAME', 'postgres')
            )
        except psycopg2.OperationalError:
            print('Database unavailable, waiting 1 second...')
            time.sleep(1)
    
    print('Database available!')

wait_for_db()
END
}

# Function to run migrations
run_migrations() {
    echo "🔄 Running database migrations..."
    python manage.py migrate --noinput
    echo "✅ Migrations completed"
}

# Function to collect static files
collect_static() {
    echo "📦 Collecting static files..."
    python manage.py collectstatic --noinput --clear
    echo "✅ Static files collected"
}

# Function to create superuser if it doesn't exist
create_superuser() {
    if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "👤 Creating superuser..."
        python manage.py shell << END
import os
from django.contrib.auth.models import User

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully')
else:
    print(f'Superuser {username} already exists')
END
    fi
}

# Main execution
main() {
    # Wait for database (only if using PostgreSQL)
    if [ "$DATABASE_URL" ] || [ "$DB_HOST" ]; then
        wait_for_db
    fi
    
    # Run migrations
    run_migrations
    
    # Collect static files
    collect_static
    
    # Create superuser if environment variables are set
    create_superuser
    
    echo "🎉 Application startup completed successfully!"
    
    # Start the application
    if [ "$1" = "dev" ]; then
        echo "🔧 Starting development server..."
        python manage.py runserver 0.0.0.0:8000
    else
        echo "🚀 Starting production server..."
        exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 RaktaPraptih.wsgi:application
    fi
}

# Run main function
main "$@"