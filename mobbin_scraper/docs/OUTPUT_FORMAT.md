# Mobbin Scraper Output Format

This document describes the structure and format of the data extracted by the Mobbin Flow Scraper.

## Overview

The scraper extracts flow data from Mobbin.com and organizes it into a structured format with associated assets. The data is stored both locally (temporarily) and in S3 (permanently).

## JSON Metadata Format

Each app's flow data is stored in a JSON file with the following structure:

```json
{
  "app_name": "Example App",
  "app_url": "https://mobbin.com/apps/example-app/screens",
  "timestamp": "2023-09-25T14:30:45.123456",
  "flows": [
    {
      "flow_id": "flow_12345",
      "flow_name": "Login Flow",
      "flow_url": "https://mobbin.com/flows/12345",
      "screens": [
        {
          "screen_id": "screen_67890",
          "screen_name": "Login Screen",
          "screen_url": "https://mobbin.com/screens/67890",
          "screenshot_path": "extracted/flow_12345/screen_67890.png",
          "order": 1,
          "annotations": [
            {
              "annotation_id": "anno_12345",
              "annotation_type": "button",
              "x": 150,
              "y": 300,
              "width": 100,
              "height": 50,
              "description": "Login button"
            }
          ]
        }
      ],
      "transitions": [
        {
          "from_screen_id": "screen_67890",
          "to_screen_id": "screen_67891",
          "transition_type": "tap",
          "description": "User taps login button"
        }
      ],
      "zip_path": "zips/flow_12345.zip",
      "extracted_path": "extracted/flow_12345/"
    }
  ]
}
```

## Directory Structure

### Local Storage (Temporary)

During execution, the scraper creates the following directory structure locally:

```
.
├── downloads/
│   └── {app_name}/
│       └── flow_{id}.zip
│
├── extracted/
│   └── {app_name}/
│       └── flow_{id}/
│           ├── screen_1.png
│           ├── screen_2.png
│           └── ...
│
├── flows/
│   └── {app_name}_flows.json
│
├── logs/
│   ├── mobbin_scraper_2023-09-25_14-30-45.log
│   └── ...
│
└── checkpoints/
    ├── apps_progress.json
    └── flows_progress.json
```

### S3 Storage (Permanent)

After processing, data is uploaded to S3 with this structure:

```
s3://your-bucket/
└── mobbin_flows/
    └── {app_name}/
        ├── {app_name}_flows.json  # Flow metadata
        ├── extracted/             # Directory containing all extracted content
        │   └── flow_{id}/
        │       ├── screen_1.png
        │       ├── screen_2.png
        │       └── ...
        └── zips/                  # Original ZIP files
            └── flow_{id}.zip
```

## Screenshots and Assets

- **Screenshots**: PNG format images of each screen in the flow
- **Annotations**: Metadata about interactive elements on screens (buttons, links, etc.)
- **ZIP Files**: Original compressed archives containing all assets for a flow

## S3 Object Metadata

Each S3 object includes the following metadata:

- `ContentType`: MIME type of the file (e.g., "application/json", "image/png")
- `app-name`: Name of the app the file belongs to
- `flow-id`: ID of the flow (for flow-specific files)
- `scrape-date`: Timestamp when the file was scraped
- `object-type`: Type of object ("flow-metadata", "screenshot", "zip-archive")

## Using the Data

The data is structured to allow:

1. **Flow Reconstruction**: Follow the sequence of screens and transitions
2. **UI Analysis**: Examine screenshots and annotations
3. **Pattern Identification**: Compare flows across different apps

The JSON metadata file serves as an index to all the assets and their relationships, allowing you to programmatically access and analyze the flow structure. 