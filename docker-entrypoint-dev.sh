#!/bin/sh

# Maximum number of retries for database connection
MAX_RETRIES=30
RETRY_INTERVAL=2
POSTGRES_PORT=5432
POSTGRES_HOST=db

echo "Development mode: Hot reloading enabled"

echo "Waiting for PostgreSQL to become available..."
echo "Host: $POSTGRES_HOST, Port: $POSTGRES_PORT"

# Function to check if PostgreSQL is ready
check_postgres() {
    nc -z "$POSTGRES_HOST" "$POSTGRES_PORT" > /dev/null 2>&1
    return $?
}

# Wait for PostgreSQL with timeout
retry_count=0
until check_postgres; do
    retry_count=$((retry_count + 1))
    
    if [ $retry_count -ge $MAX_RETRIES ]; then
        echo "Error: PostgreSQL did not become available in time. Exiting..."
        exit 1
    fi
    
    echo "PostgreSQL is not available yet. Retry $retry_count of $MAX_RETRIES..."
    sleep $RETRY_INTERVAL
done

echo "PostgreSQL is now available"

# Run database migrations with error handling
echo "Running database migrations..."
if flask db upgrade; then
    echo "Database migrations completed successfully"
else
    migration_exit_code=$?
    echo "Error: Database migration failed with exit code $migration_exit_code"
    
    # Check if it's a common migration error
    if flask db current 2>&1 | grep -q "Error: Can't locate revision identified by"; then
        echo "Error: Migration history is inconsistent. Please check your migration files and database state."
    elif flask db current 2>&1 | grep -q "Error: Connection refused"; then
        echo "Error: Could not connect to the database. Please check your database connection settings."
    else
        echo "Error: An unexpected error occurred during migration. Please check the logs for more details."
    fi
    
    exit $migration_exit_code
fi

# Start Flask development server with hot reloading
echo "Starting Flask development server with hot reloading..."
export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
exec flask run --host=0.0.0.0 --port=8000 --reload 