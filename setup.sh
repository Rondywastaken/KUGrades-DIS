#!/bin/bash
set -e

command -v psql >/dev/null 2>&1 || {
  echo "Error: psql not found. Install PostgreSQL and make sure it is on PATH."
  exit 1
}

command -v python >/dev/null 2>&1 || {
  echo "Error: python not found. Activate your virtual environment first."
  exit 1
}

python -c "import psycopg2" >/dev/null 2>&1 || {
  echo "Error: psycopg2 not installed. Run: pip install -r requirements.txt"
  exit 1
}

# 1. Creates the database with the name KUGrades:
echo "[1/3] Creating database 'kugrades'..."
if psql -U postgres -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = 'kugrades'" | grep -q 1; then
  echo "Database already exists"
else
  psql -U postgres -c "CREATE DATABASE kugrades OWNER postgres;"
  echo "Database created"
fi
echo ""

# 2. Constructs the database structure using the defined schema, which follows the E/R diagram:
echo "[2/3] Building database schema..."
psql -U postgres -d kugrades < schema.sql
echo "Schema applied"
echo ""

# 3. Populates the database with data from the `data/` folder, which has been scraped using the scraper (see `scrape.py`):
echo "[3/3] Populating database with data..."
python setup.py
echo "Database has been populated"
echo ""

echo "Setup complete! Run 'python app.py' to start the application"
