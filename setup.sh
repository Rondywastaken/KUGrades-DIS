#!/bin/bash

# check dependencies
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "Python not found. Please install Python and try again"
    exit 1
fi

if ! command -v psql &>/dev/null; then
  echo "psql not found. Please install PostgreSQL and try again"
fi

if ! python -c "import psycopg2" &>/dev/null; then
    echo "psycopg2 not found. Please install psycopg2 or run 'pip install -r requirements.txt' and try again"
    exit 1
fi

# 1. Creates the database with the name kugrades:
echo "[1/3] Creating database 'kugrades'..."
if psql -d postgres -c "CREATE DATABASE kugrades;"; then
    echo "Database created"
else
    echo "Failed to create database. Please make sure that PostgreSQL is running"
    exit 1
fi
echo ""

# 2. Constructs the database structure using the defined schema:
echo "[2/3] Building database schema..."
if psql -U postgres -d kugrades < schema.sql; then
    echo "Schema applied"
else
    echo "Failed to apply schema"
    exit 1
fi
echo ""

# 3. Populates the database with data from the data/ folder:
echo "[3/3] Populating database with data..."
if $PYTHON setup.py; then
    echo "Database populated"
else
    echo "Failed to populate database"
    exit 1
fi
echo ""

echo "Setup complete! Run '$PYTHON app.py' to start the application"
