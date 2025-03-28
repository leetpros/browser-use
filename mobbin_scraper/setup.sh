#!/bin/bash

# Setup script for Mobbin Scraper

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$SCRIPT_DIR"

# Create necessary directories if they don't exist
mkdir -p logs checkpoints downloads extracted flows mobbin_flows mobbin_screenshots

# Check if .env.mobbin_scraper file exists, otherwise copy the example
if [ ! -f .env.mobbin_scraper ]; then
    echo "Creating .env.mobbin_scraper from example file..."
    cp .env.mobbin_scraper.example .env.mobbin_scraper
    echo "Please edit .env.mobbin_scraper with your actual credentials"
fi

# Install required dependencies
echo "Installing required Python packages..."
pip install -r requirements.txt

# Install browser-use requirements
echo "Installing Playwright (required by browser-use)..."
python -m playwright install

echo "Setup complete!"
echo "Next steps:"
echo "1. Edit .env.mobbin_scraper with your AWS credentials and Chrome settings"
echo "2. Ensure you have the required JSON app file (mobbin_apps_complete.json)"
echo "3. Run the scraper with: python scrape_mobbin_flow_tree.py" 