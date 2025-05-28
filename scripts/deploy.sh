# scripts/deploy.sh - Deployment script
#!/bin/bash

set -e

echo "🚀 Starting deployment process..."

# Check if required environment variables are set
check_env_vars() {
    local required_vars=("SECRET_KEY" "DATABASE_URL")
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var}" ]]; then
            echo "❌ Error: $var environment variable is not set"
            exit 1
        fi
    done
    echo "✅ Environment variables check passed"
}

# Install dependencies
install_dependencies() {
    echo "📦 Installing dependencies..."
    pip install --no-cache-dir -r requirements.txt
    echo "