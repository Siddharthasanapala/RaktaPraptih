#!/bin/bash
# scripts/start.sh - Production startup script

set -e

echo "🚀 Starting RaktaPraptih application..."

# Function to wait for the database to be ready (unchanged)
wait_for_db() {
    echo "⏳ Waiting for database to be ready..."
    python << END
import sys
import time
import psycopg2
import os
from urllib.parse import urlparse
import socket

def wait_for_db():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("DATABASE_URL not set. Exiting...")
        sys.exit(1)
    
    try:
        parsed_url = urlparse(db_url)
        host = parsed_url.hostname
        # Try to resolve host to IPv4
        hostaddr = None
        try:
            hostaddr = socket.getaddrinfo(host, None, socket.AF_INET)[0][4][0]
            print(f"Resolved host {host} to IPv4: {hostaddr}")
        except socket.gaierror as e:
            print(f"Could not resolve host {host} to IPv4: {str(e)}. Falling back to default host resolution.")
        
        # Base connection parameters
        db_params = {
            'host': host,
            'port': parsed_url.port or 5432,
            'user': parsed_url.username,
            'password': parsed_url.password,
            'dbname': parsed_url.path.lstrip('/'),
            'sslmode': 'require'  # Required for Supabase
        }
        # Add hostaddr if IPv4 resolution succeeded
        if hostaddr:
            db_params['hostaddr'] = hostaddr
        
        print(f"Attempting to connect to database: host={db_params['host']}, port={db_params['port']}, dbname={db_params['dbname']}, sslmode={db_params['sslmode']}")
        if db_params['host']=='test-postgres':
            db_params['sslmode']='disable'

        max_attempts = 30
        attempt = 1
        db_conn = None
        while not db_conn and attempt <= max_attempts:
            try:
                db_conn = psycopg2.connect(**db_params)
                print('Database available!')
                db_conn.close()
            except psycopg2.OperationalError as e:
                print(f'Database unavailable, attempt {attempt}/{max_attempts}: {str(e)}')
                time.sleep(1)
                attempt += 1
        if not db_conn:
            print(f"Failed to connect to database after {max_attempts} attempts. Exiting...")
            sys.exit(1)
    except Exception as e:
        print(f"Error parsing DATABASE_URL or connecting to database: {str(e)}")
        sys.exit(1)

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
from django.contrib.auth import get_user_model

User = get_user_model()
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

# Main execution function
main() {
    # Wait for the database
    wait_for_db
    
    # Run migrations
    run_migrations
    
    # Collect static files
    collect_static
    
    # Create superuser if environment variables are set
    create_superuser
    
    echo "🎉 Application startup completed successfully!"

    if [ "$1" = "dev" ]; then
        echo "🔧 Starting development server..."
        python manage.py runserver 0.0.0.0:8000
    else
        echo "🚀 Starting production server..."
        gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 4 --timeout 90 RaktaPraptih.wsgi:application &
        echo "Gunicorn started in background (PID: $!)."
        tail -f /dev/null
    fi
}

# Run main function with provided arguments
main "$@"