#!/bin/bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Update system
log_info "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required packages
log_info "Installing Docker and dependencies..."
sudo apt install -y docker.io docker-compose git curl

# Add current user to docker group
log_info "Adding user to docker group..."
sudo usermod -aG docker $USER

# Create application directory
log_info "Creating application directory..."
sudo mkdir -p /opt/fastapi-production
sudo chown -R $USER:$USER /opt/fastapi-production
cd /opt/fastapi-production

# Clone your repository (REPLACE WITH YOUR ACTUAL REPO URL)
log_info "Cloning your GitHub repository..."
# Replace this with your actual GitHub repository URL
GITHUB_REPO="https://github.com/elvisquant/fleet-manager.git"

if [ -z "$GITHUB_REPO" ] || [ "$GITHUB_REPO"="https://github.com/elvisquant/fleet-manager.git" ]; then
    log_error "Please update the GITHUB_REPO variable in this script with your actual repository URL"
    exit 1
fi

git clone $GITHUB_REPO . || {
    log_warn "Repository already exists or clone failed. Pulling latest changes..."
    git pull origin main
}

# Make scripts executable
log_info "Making scripts executable..."
chmod +x scripts/*.sh

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    log_info "Creating .env file from example..."
    cp .env.example .env
    log_warn "Please update the .env file with your actual values!"
fi

# Install Certbot for SSL
log_info "Installing Certbot for SSL certificates..."
sudo apt install -y certbot python3-certbot-nginx

# Create SSL certificates (this will prompt for email)
log_info "Setting up SSL certificates..."
read -p "Enter your email for SSL certificate notifications: " EMAIL
sudo certbot certonly --standalone \
    -d app.elvisquant.com \
    -d api.elvisquant.com \
    -d monitor.elvisquant.com \
    --non-interactive --agree-tos --email "$EMAIL" || {
    log_warn "SSL certificate setup may have failed. You can run this manually later:"
    log_warn "sudo certbot certonly --standalone -d app.elvisquant.com -d api.elvisquant.com -d monitor.elvisquant.com --non-interactive --agree-tos --email your-email@example.com"
}

# Set up automatic certificate renewal
log_info "Setting up automatic SSL certificate renewal..."
sudo crontab -l | { cat; echo "0 3 * * * certbot renew --quiet --deploy-hook \"docker-compose -f /opt/fastapi-production/docker-compose.prod.yml exec nginx nginx -s reload\""; } | sudo crontab -

# Create Docker network if it doesn't exist
log_info "Creating Docker network..."
docker network create fastapi-network 2>/dev/null || true

# Build and start the application
log_info "Building and starting the application..."
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to start
log_info "Waiting for services to become healthy..."
sleep 30

# Run health check
log_info "Running health check..."
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    log_info "✅ Application is healthy and running!"
else
    log_error "❌ Application health check failed"
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi

# Print success message
log_info "🎉 Setup completed successfully!"
log_info "Your application is running at: http://localhost:8000"
log_info "API health check: http://localhost:8000/health"
log_info ""
log_info "Next steps:"
log_info "1. Update your .env file with production values"
log_info "2. Configure your DNS records to point to this server's IP"
log_info "3. Set up GitHub Secrets for CI/CD automation"
log_info ""
log_info "You may need to reboot for all changes to take effect:"
log_info "sudo reboot"