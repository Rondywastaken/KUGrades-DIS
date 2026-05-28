#!/bin/bash

# 1. Creates the database with the name KUGrades:
echo "[1/3] Creating database 'kugrades'..."
psql -U postgres -c "CREATE DATABASE kugrades OWNER postgres;"
echo "Database created"
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
