# Mobbin Scraper Quick Start Guide

This guide will help you get up and running with the Mobbin Flow Scraper quickly.

## 1. Prerequisites

- Python 3.7+ installed
- AWS account with S3 bucket set up
- Chrome browser installed

## 2. Installation

```bash
# Clone the repository (if applicable)
git clone <repository-url>
cd <repository-directory>

# Install dependencies
pip install python-dotenv boto3 pydantic browser-use
```

## 3. Configuration

Create a file named `.env.mobbin_scraper` in the root directory with the following content:

```
# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=your-mobbin-data-bucket

# Chrome Configuration
CHROME_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
CHROME_PROFILE=Profile 4

# Scraper Configuration (Optional, these are the defaults)
DOWNLOAD_TIMEOUT=60000
MAX_RETRIES=3
RANDOM_DELAY_MIN=2.0
RANDOM_DELAY_MAX=5.0
S3_UPLOAD_WORKERS=10
```

Replace the placeholder values with your actual AWS credentials and settings.

## 4. Prepare App List

Create a file named `mobbin_apps_complete.json` in the root directory with your list of Mobbin apps to scrape:

```json
[
  {
    "title": "App Name 1",
    "url": "https://mobbin.com/apps/app-identifier/some-id/screens",
    "description": "App description"
  },
  {
    "title": "App Name 2",
    "url": "https://mobbin.com/apps/another-app/another-id/screens",
    "description": "Another app description"
  }
]
```

## 5. Run the Scraper

```bash
python scrape_mobbin_flow_tree.py
```

The script will:
1. Process each app in the list
2. Download and extract flow data
3. Upload files to your S3 bucket
4. Clean up local files after successful upload

## 6. Monitor Progress

- Check the terminal output for real-time progress
- View detailed logs in the `logs/` directory
- If the script is interrupted, simply run it again to resume from where it left off

## 7. Access Your Data

Your data will be organized in S3 as follows:

```
s3://your-bucket/
└── mobbin_flows/
    ├── App_Name_1/
    │   ├── App_Name_1_flows.json  # Flow metadata
    │   ├── extracted/             # Extracted flow assets
    │   └── zips/                  # Original ZIP files
    ├── App_Name_2/
    ...
```

## 8. Troubleshooting

If you encounter issues:

1. Check the log files in the `logs/` directory
2. Verify your AWS credentials and S3 bucket permissions
3. Make sure Chrome is properly installed and configured
4. Check your internet connection

For more detailed information, refer to the full README.md documentation. 