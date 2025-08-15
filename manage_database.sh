#!/bin/bash

echo "🗄️ Diet Planner Database Management Tool"
echo "========================================"

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
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check PostgreSQL connection
check_connection() {
    if pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Connected to database successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to connect to database${NC}"
        return 1
    fi
}

# Function to show database status
show_status() {
    echo -e "${BLUE}📊 Database Status:${NC}"
    
    # Check connection
    if check_connection; then
        # Get table counts
        echo "Table Information:"
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "
            SELECT 
                schemaname,
                tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes
            FROM pg_stat_user_tables 
            ORDER BY tablename;
        " 2>/dev/null || echo "Could not retrieve table statistics"
        
        # Get database size
        echo ""
        echo "Database Size:"
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "
            SELECT 
                pg_size_pretty(pg_database_size('$DB_NAME')) as size;
        " 2>/dev/null || echo "Could not retrieve database size"
    fi
}

# Function to backup database
backup_database() {
    echo -e "${BLUE}💾 Creating database backup...${NC}"
    
    BACKUP_FILE="diet_planner_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    if pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > "$BACKUP_FILE" 2>/dev/null; then
        echo -e "${GREEN}✅ Backup created successfully: $BACKUP_FILE${NC}"
        echo "Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"
    else
        echo -e "${RED}❌ Backup failed${NC}"
    fi
}

# Function to restore database
restore_database() {
    echo -e "${BLUE}🔄 Database Restore${NC}"
    
    # List available backup files
    echo "Available backup files:"
    ls -la *.sql 2>/dev/null | grep backup || echo "No backup files found"
    
    read -p "Enter backup filename to restore (or press Enter to cancel): " BACKUP_FILE
    
    if [ -n "$BACKUP_FILE" ] && [ -f "$BACKUP_FILE" ]; then
        echo -e "${YELLOW}⚠️  This will overwrite the current database. Are you sure? (y/N):${NC}"
        read -p "" confirm
        
        if [[ $confirm =~ ^[Yy]$ ]]; then
            echo "Restoring from $BACKUP_FILE..."
            if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME < "$BACKUP_FILE" 2>/dev/null; then
                echo -e "${GREEN}✅ Database restored successfully${NC}"
            else
                echo -e "${RED}❌ Restore failed${NC}"
            fi
        else
            echo "Restore cancelled"
        fi
    else
        echo "Invalid backup file or operation cancelled"
    fi
}

# Function to insert sample data
insert_sample_data() {
    echo -e "${BLUE}📝 Inserting sample data...${NC}"
    
    if [ -f "insert_sample_data.sql" ]; then
        if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f insert_sample_data.sql 2>/dev/null; then
            echo -e "${GREEN}✅ Sample data inserted successfully${NC}"
        else
            echo -e "${RED}❌ Failed to insert sample data${NC}"
        fi
    else
        echo -e "${RED}❌ Sample data file not found${NC}"
    fi
}

# Function to clear all data
clear_database() {
    echo -e "${RED}🗑️  Clear Database${NC}"
    echo -e "${YELLOW}⚠️  WARNING: This will delete ALL data from the database!${NC}"
    read -p "Are you absolutely sure? Type 'DELETE ALL' to confirm: " confirm
    
    if [ "$confirm" = "DELETE ALL" ]; then
        echo "Clearing all data..."
        if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
            TRUNCATE TABLE meal_logs CASCADE;
            TRUNCATE TABLE diet_plans CASCADE;
            TRUNCATE TABLE users CASCADE;
        " 2>/dev/null; then
            echo -e "${GREEN}✅ Database cleared successfully${NC}"
        else
            echo -e "${RED}❌ Failed to clear database${NC}"
        fi
    else
        echo "Operation cancelled"
    fi
}

# Function to show table data
show_table_data() {
    echo -e "${BLUE}📋 Show Table Data${NC}"
    echo "1. Users"
    echo "2. Diet Plans"
    echo "3. Meal Logs"
    echo "4. All Tables"
    
    read -p "Select option (1-4): " choice
    
    case $choice in
        1)
            echo "Users table:"
            psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT * FROM users;" 2>/dev/null
            ;;
        2)
            echo "Diet Plans table:"
            psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT * FROM diet_plans;" 2>/dev/null
            ;;
        3)
            echo "Meal Logs table:"
            psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT * FROM meal_logs;" 2>/dev/null
            ;;
        4)
            echo "All tables:"
            psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
                SELECT 'Users' as table_name, COUNT(*) as count FROM users
                UNION ALL
                SELECT 'Diet Plans' as table_name, COUNT(*) as count FROM diet_plans
                UNION ALL
                SELECT 'Meal Logs' as table_name, COUNT(*) as count FROM meal_logs;
            " 2>/dev/null
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
}

# Function to run custom SQL
run_custom_sql() {
    echo -e "${BLUE}🔧 Run Custom SQL${NC}"
    echo "Enter your SQL query (or 'exit' to return):"
    
    while true; do
        read -p "SQL> " sql_query
        
        if [ "$sql_query" = "exit" ]; then
            break
        fi
        
        if [ -n "$sql_query" ]; then
            echo "Executing: $sql_query"
            psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "$sql_query" 2>/dev/null
        fi
    done
}

# Function to show menu
show_menu() {
    echo ""
    echo -e "${BLUE}📋 Available Operations:${NC}"
    echo "1. Show Database Status"
    echo "2. Show Table Data"
    echo "3. Insert Sample Data"
    echo "4. Backup Database"
    echo "5. Restore Database"
    echo "6. Run Custom SQL"
    echo "7. Clear Database"
    echo "8. Exit"
    echo ""
}

# Main menu loop
main() {
    while true; do
        show_menu
        read -p "Select operation (1-8): " choice
        
        case $choice in
            1)
                show_status
                ;;
            2)
                show_table_data
                ;;
            3)
                insert_sample_data
                ;;
            4)
                backup_database
                ;;
            5)
                restore_database
                ;;
            6)
                run_custom_sql
                ;;
            7)
                clear_database
                ;;
            8)
                echo -e "${GREEN}👋 Goodbye!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Invalid option. Please select 1-8.${NC}"
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Check if PostgreSQL tools are available
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL client tools not found. Please install PostgreSQL.${NC}"
    exit 1
fi

# Start the application
main
