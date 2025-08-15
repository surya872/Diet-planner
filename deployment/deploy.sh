#!/bin/bash

# Deployment Automation Script
# Supports multiple deployment targets

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    echo "Diet Planner Deployment Script"
    echo ""
    echo "Usage: $0 [TARGET] [OPTIONS]"
    echo ""
    echo "Targets:"
    echo "  render     Deploy to Render.com"
    echo "  railway    Deploy to Railway.app"
    echo "  vercel     Deploy to Vercel"
    echo "  heroku     Deploy to Heroku"
    echo "  docker     Build and run with Docker"
    echo "  local      Deploy locally"
    echo ""
    echo "Options:"
    echo "  --env ENV     Environment (development|staging|production)"
    echo "  --build       Force rebuild"
    echo "  --migrate     Run database migrations"
    echo "  --help        Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 render --env production"
    echo "  $0 docker --build"
    echo "  $0 local --migrate"
}

check_dependencies() {
    local deps=("git" "curl")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            log_error "Required dependency '$dep' is not installed"
            exit 1
        fi
    done
}

validate_environment() {
    log_info "Validating environment configuration..."
    
    # Check for required environment variables
    local required_vars=("GEMINI_API_KEY")
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var}" ]]; then
            log_error "Required environment variable '$var' is not set"
            exit 1
        fi
    done
    
    log_success "Environment validation passed"
}

deploy_render() {
    log_info "Deploying to Render.com..."
    
    # Check if render.yaml exists
    if [[ ! -f "render.yaml" ]]; then
        log_error "render.yaml not found. Please ensure you're in the project root."
        exit 1
    fi
    
    # Push to git (Render deploys from git)
    if [[ -n "$(git status --porcelain)" ]]; then
        log_warning "You have uncommitted changes. Committing them..."
        git add .
        git commit -m "Deploy to Render: $(date)"
    fi
    
    git push origin main
    
    log_success "Code pushed to git. Render will automatically deploy."
    log_info "Monitor deployment at: https://dashboard.render.com"
}

deploy_railway() {
    log_info "Deploying to Railway..."
    
    # Check if railway CLI is installed
    if ! command -v railway &> /dev/null; then
        log_error "Railway CLI is not installed. Install it from: https://railway.app/cli"
        exit 1
    fi
    
    # Login check
    if ! railway whoami &> /dev/null; then
        log_info "Please login to Railway..."
        railway login
    fi
    
    # Deploy
    railway up
    
    log_success "Deployed to Railway successfully"
}

deploy_vercel() {
    log_info "Deploying to Vercel..."
    
    # Check if vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        log_error "Vercel CLI is not installed. Install it with: npm i -g vercel"
        exit 1
    fi
    
    # Build frontend
    log_info "Building frontend..."
    cd frontend
    npm run build
    cd ..
    
    # Deploy
    if [[ "$ENV" == "production" ]]; then
        vercel --prod
    else
        vercel
    fi
    
    log_success "Deployed to Vercel successfully"
}

deploy_heroku() {
    log_info "Deploying to Heroku..."
    
    # Check if heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        log_error "Heroku CLI is not installed. Install it from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Check if logged in
    if ! heroku auth:whoami &> /dev/null; then
        log_info "Please login to Heroku..."
        heroku login
    fi
    
    # Create app if it doesn't exist
    APP_NAME="diet-planner-$(whoami)"
    if ! heroku apps:info "$APP_NAME" &> /dev/null; then
        log_info "Creating Heroku app: $APP_NAME"
        heroku create "$APP_NAME"
    fi
    
    # Add PostgreSQL addon
    if ! heroku addons:info postgresql --app="$APP_NAME" &> /dev/null; then
        log_info "Adding PostgreSQL addon..."
        heroku addons:create heroku-postgresql:mini --app="$APP_NAME"
    fi
    
    # Set environment variables
    log_info "Setting environment variables..."
    heroku config:set FLASK_ENV=production --app="$APP_NAME"
    heroku config:set GEMINI_API_KEY="$GEMINI_API_KEY" --app="$APP_NAME"
    
    # Deploy
    git push heroku main
    
    log_success "Deployed to Heroku successfully"
    log_info "App URL: https://$APP_NAME.herokuapp.com"
}

deploy_docker() {
    log_info "Building and running with Docker..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Stop existing containers
    docker-compose -f deployment/docker-compose.prod.yml down 2>/dev/null || true
    
    # Build and start
    if [[ "$BUILD" == "true" ]]; then
        docker-compose -f deployment/docker-compose.prod.yml up --build -d
    else
        docker-compose -f deployment/docker-compose.prod.yml up -d
    fi
    
    # Wait for services to be healthy
    log_info "Waiting for services to be healthy..."
    sleep 30
    
    # Check health
    if curl -f http://localhost:5001/api/health > /dev/null 2>&1; then
        log_success "Backend is healthy"
    else
        log_error "Backend health check failed"
    fi
    
    if curl -f http://localhost:3001 > /dev/null 2>&1; then
        log_success "Frontend is healthy"
    else
        log_error "Frontend health check failed"
    fi
    
    log_success "Docker deployment completed"
    log_info "Backend: http://localhost:5001"
    log_info "Frontend: http://localhost:3001"
}

deploy_local() {
    log_info "Deploying locally..."
    
    # Install dependencies
    log_info "Installing backend dependencies..."
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    
    log_info "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
    
    # Run migrations if requested
    if [[ "$MIGRATE" == "true" ]]; then
        log_info "Running database migrations..."
        ./setup_database.sh
    fi
    
    # Start services
    log_info "Starting services..."
    ./start_simple.sh
    
    log_success "Local deployment completed"
}

# Parse command line arguments
TARGET=""
ENV="development"
BUILD="false"
MIGRATE="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        render|railway|vercel|heroku|docker|local)
            TARGET="$1"
            shift
            ;;
        --env)
            ENV="$2"
            shift 2
            ;;
        --build)
            BUILD="true"
            shift
            ;;
        --migrate)
            MIGRATE="true"
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if target is specified
if [[ -z "$TARGET" ]]; then
    log_error "No deployment target specified"
    show_help
    exit 1
fi

# Main execution
log_info "Starting deployment to $TARGET (environment: $ENV)"

check_dependencies
validate_environment

case $TARGET in
    render)
        deploy_render
        ;;
    railway)
        deploy_railway
        ;;
    vercel)
        deploy_vercel
        ;;
    heroku)
        deploy_heroku
        ;;
    docker)
        deploy_docker
        ;;
    local)
        deploy_local
        ;;
    *)
        log_error "Unknown deployment target: $TARGET"
        exit 1
        ;;
esac

log_success "Deployment to $TARGET completed successfully!"
