# Mobbin UI Flow Scraper

A robust web scraper designed to extract UI flow data from Mobbin.com, download and extract flow assets, and upload them to AWS S3 storage with resumable checkpoints.

## Overview

This scraper automates the process of:
1. Navigating to Mobbin app pages
2. Extracting flow information
3. Downloading flow assets as ZIP files
4. Extracting the content
5. Uploading the data to AWS S3
6. Cleaning up local files after successful upload

The script includes comprehensive checkpoint functionality, allowing it to resume from the exact point of interruption if the process is stopped for any reason.

## Documentation

For detailed information, please refer to the following documents in the `docs` directory:

- [Quick Start Guide](docs/QUICK_START.md) - Get up and running quickly
- [Output Format](docs/OUTPUT_FORMAT.md) - Understand the data structure
- [Contributing](docs/CONTRIBUTING.md) - Guidelines for contributing to the project

## Requirements

- Python 3.7+
- AWS account with S3 bucket and appropriate credentials
- Chrome browser

### Dependencies

```
pip install python-dotenv boto3 pydantic browser-use
```

## Configuration

Copy `.env.mobbin_scraper.example` to `.env.mobbin_scraper` and update with your credentials:

```bash
cp .env.mobbin_scraper.example .env.mobbin_scraper
```

Then edit the file with your actual AWS and Chrome settings.

## Usage

```bash
python scrape_mobbin_flow_tree.py
```

If the script is interrupted, simply run it again to resume from where it left off.

## License

This project is available for personal use. Please respect Mobbin's terms of service when using this tool. 