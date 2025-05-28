#!/usr/bin/env python
import os
import sys
import django
import requests
from django.core.management import execute_from_command_line

def check_database():
    """Check database connectivity"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database check failed: {e}")
        return False

def check_migrations():
    """Check if there are pending migrations"""
    try:
        from django.core.management.commands.showmigrations import Command
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        
        command = Command()
        command.handle()
        
        output = buffer.getvalue()
        sys.stdout = old_stdout
        
        if '[ ]' in output:
            print("Pending migrations found")
            return False
        return True
    except Exception as e:
        print(f"Migration check failed: {e}")
        return False

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RaktaPraptih.settings')
    django.setup()
    
    checks = [
        ("Database", check_database),
        ("Migrations", check_migrations),
    ]
    
    all_passed = True
    for name, check_func in checks:
        if check_func():
            print(f"✓ {name} check passed")
        else:
            print(f"✗ {name} check failed")
            all_passed = False
    
    if all_passed:
        print("All health checks passed!")
        sys.exit(0)
    else:
        print("Some health checks failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()