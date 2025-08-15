#!/bin/bash

echo "🗄️ Setting up Diet Planner Database..."

# Database configuration
DB_NAME="diet_planner"
DB_USER="diet_user"
DB_PASSWORD="diet_password"
DB_HOST="localhost"
DB_PORT="5432"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if PostgreSQL is running
check_postgres() {
    if ! pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2>&1; then
        echo -e "${RED}❌ PostgreSQL is not running on $DB_HOST:$DB_PORT${NC}"
        echo "Please start PostgreSQL and try again."
        exit 1
    fi
    echo -e "${GREEN}✅ PostgreSQL is running${NC}"
}

# Function to create database and user
setup_database() {
    echo "🔧 Creating database and user..."
    
    # Create database and user using psql
    psql -h $DB_HOST -p $DB_PORT -U postgres -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || echo "Database already exists"
    psql -h $DB_HOST -p $DB_PORT -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || echo "User already exists"
    psql -h $DB_HOST -p $DB_PORT -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || echo "Privileges already granted"
    
    echo -e "${GREEN}✅ Database and user created successfully${NC}"
}

# Function to initialize schema
init_schema() {
    echo "📋 Initializing database schema..."
    
    if [ -f "database/init.sql" ]; then
        # Grant schema privileges
        psql -h $DB_HOST -p $DB_PORT -U postgres -d $DB_NAME -c "GRANT ALL ON SCHEMA public TO $DB_USER;" 2>/dev/null
        
        # Run initialization script
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f database/init.sql
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Database schema initialized successfully${NC}"
        else
            echo -e "${RED}❌ Failed to initialize database schema${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ init.sql file not found in database/ directory${NC}"
        exit 1
    fi
}

# Function to verify setup
verify_setup() {
    echo "🔍 Verifying database setup..."
    
    # Check if tables exist
    TABLE_COUNT=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
    
    if [ "$TABLE_COUNT" -ge 3 ]; then
        echo -e "${GREEN}✅ Database setup verified successfully${NC}"
        echo "📊 Tables created: $TABLE_COUNT"
    else
        echo -e "${RED}❌ Database setup verification failed${NC}"
        exit 1
    fi
}

# Function to show connection info
show_connection_info() {
    echo ""
    echo -e "${GREEN}🎉 Database setup completed successfully!${NC}"
    echo ""
    echo "📋 Connection Information:"
    echo "   Database: $DB_NAME"
    echo "   User: $DB_USER"
    echo "   Password: $DB_PASSWORD"
    echo "   Host: $DB_HOST"
    echo "   Port: $DB_PORT"
    echo ""
    echo "🔗 Connection string:"
    echo "   postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
    echo ""
    echo "📝 Update your .env file with these credentials:"
    echo "   POSTGRES_DB=$DB_NAME"
    echo "   POSTGRES_USER=$DB_USER"
    echo "   POSTGRES_PASSWORD=$DB_PASSWORD"
    echo "   POSTGRES_HOST=$DB_HOST"
    echo "   POSTGRES_PORT=$DB_PORT"
    echo ""
    echo "🚀 You can now run the application with: ./start.sh"
}

# Main execution
main() {
    echo "🍎 Diet Planner Database Setup"
    echo "================================"
    
    check_postgres
    setup_database
    init_schema
    verify_setup
    show_connection_info
}

# Run main function
main
