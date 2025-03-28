<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./static/browser-use-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./static/browser-use.png">
  <img alt="Shows a black Browser Use Logo in light color mode and a white one in dark color mode." src="./static/browser-use.png"  width="full">
</picture>

<h1 align="center">Enable AI to control your browser 🤖</h1>

[![GitHub stars](https://img.shields.io/github/stars/gregpr07/browser-use?style=social)](https://github.com/gregpr07/browser-use/stargazers)
[![Discord](https://img.shields.io/discord/1303749220842340412?color=7289DA&label=Discord&logo=discord&logoColor=white)](https://link.browser-use.com/discord)
[![Documentation](https://img.shields.io/badge/Documentation-📕-blue)](https://docs.browser-use.com)
[![Cloud](https://img.shields.io/badge/Cloud-☁️-blue)](https://cloud.browser-use.com)
[![Twitter Follow](https://img.shields.io/twitter/follow/Gregor?style=social)](https://x.com/gregpr07)
[![Twitter Follow](https://img.shields.io/twitter/follow/Magnus?style=social)](https://x.com/mamagnus00)
[![Weave Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fapp.workweave.ai%2Fapi%2Frepository%2Fbadge%2Forg_T5Pvn3UBswTHIsN1dWS3voPg%2F881458615&labelColor=#EC6341)](https://app.workweave.ai/reports/repository/org_T5Pvn3UBswTHIsN1dWS3voPg/881458615)


🌐 Browser-use is the easiest way to connect your AI agents with the browser. 

💡 See what others are building and share your projects in our [Discord](https://link.browser-use.com/discord) - we'd love to see what you create!

🌩️ Skip the setup - try our hosted version for instant browser automation! [Try it now](https://cloud.browser-use.com).


# Quick start


With pip (Python>=3.11):

```bash
pip install browser-use
```

install playwright:

```bash
playwright install
```

Spin up your agent:

```python
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    agent = Agent(
        task="Go to Reddit, search for 'browser-use', click on the first post and return the first comment.",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

Add your API keys for the provider you want to use to your `.env` file.

```bash
OPENAI_API_KEY=
```

For other settings, models, and more, check out the [documentation 📕](https://docs.browser-use.com).


### Test with UI

You can test [browser-use with a UI repository](https://github.com/browser-use/web-ui)

Or simply run the gradio example:

```
uv pip install gradio
```

```bash
python examples/ui/gradio_demo.py
```

# Demos







<br/><br/>

[Task](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/shopping.py): Add grocery items to cart, and checkout.

[![AI Did My Groceries](https://github.com/user-attachments/assets/d9359085-bde6-41d4-aa4e-6520d0221872)](https://www.youtube.com/watch?v=L2Ya9PYNns8)


<br/><br/>


Prompt: Add my latest LinkedIn follower to my leads in Salesforce.

![LinkedIn to Salesforce](https://github.com/user-attachments/assets/1440affc-a552-442e-b702-d0d3b277b0ae)

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/find_and_apply_to_jobs.py): Read my CV & find ML jobs, save them to a file, and then start applying for them in new tabs, if you need help, ask me.'

https://github.com/user-attachments/assets/171fb4d6-0355-46f2-863e-edb04a828d04

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/browser/real_browser.py): Write a letter in Google Docs to my Papa, thanking him for everything, and save the document as a PDF.

![Letter to Papa](https://github.com/user-attachments/assets/242ade3e-15bc-41c2-988f-cbc5415a66aa)

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/custom-functions/save_to_file_hugging_face.py): Look up models with a license of cc-by-sa-4.0 and sort by most likes on Hugging face, save top 5 to file.

https://github.com/user-attachments/assets/de73ee39-432c-4b97-b4e8-939fd7f323b3


<br/><br/>


## More examples

For more examples see the [examples](examples) folder or join the [Discord](https://link.browser-use.com/discord) and show off your project.

# Vision

Tell your computer what to do, and it gets it done.

## Roadmap

### Agent
- [ ] Improve agent memory (summarize, compress, RAG, etc.)
- [ ] Enhance planning capabilities (load website specific context)
- [ ] Reduce token consumption (system prompt, DOM state)

### DOM Extraction
- [ ] Improve extraction for datepickers, dropdowns, special elements
- [ ] Improve state representation for UI elements

### Rerunning tasks
- [ ] LLM as fallback
- [ ] Make it easy to define workfows templates where LLM fills in the details
- [ ] Return playwright script from the agent

### Datasets
- [ ] Create datasets for complex tasks
- [ ] Benchmark various models against each other
- [ ] Fine-tuning models for specific tasks

### User Experience
- [ ] Human-in-the-loop execution
- [ ] Improve the generated GIF quality
- [ ] Create various demos for tutorial execution, job application, QA testing, social media, etc.

## Contributing

We love contributions! Feel free to open issues for bugs or feature requests. To contribute to the docs, check out the `/docs` folder.

## Local Setup

To learn more about the library, check out the [local setup 📕](https://docs.browser-use.com/development/local-setup).

## Cooperations

We are forming a commission to define best practices for UI/UX design for browser agents.
Together, we're exploring how software redesign improves the performance of AI agents and gives these companies a competitive advantage by designing their existing software to be at the forefront of the agent age.

Email [Toby](mailto:tbiddle@loop11.com?subject=I%20want%20to%20join%20the%20UI/UX%20commission%20for%20AI%20agents&body=Hi%20Toby%2C%0A%0AI%20found%20you%20in%20the%20browser-use%20GitHub%20README.%0A%0A) to apply for a seat on the committee.
## Citation

If you use Browser Use in your research or project, please cite:


    
```bibtex
@software{browser_use2024,
  author = {Müller, Magnus and Žunič, Gregor},
  title = {Browser Use: Enable AI to control your browser},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/browser-use/browser-use}
}
```
 


 <div align="center"> <img src="https://github.com/user-attachments/assets/402b2129-b6ac-44d3-a217-01aea3277dce" width="400"/> 
 
[![Twitter Follow](https://img.shields.io/twitter/follow/Gregor?style=social)](https://x.com/gregpr07)
[![Twitter Follow](https://img.shields.io/twitter/follow/Magnus?style=social)](https://x.com/mamagnus00)
 
 </div> 

<div align="center">
Made with ❤️ in Zurich and San Francisco
 </div> 

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

## Features

- **Batch Processing**: Process multiple apps sequentially from a JSON source
- **Resilient Scraping**: Automatic retry mechanism for download failures
- **Checkpointing**: Save progress at multiple levels (app, flow, and file)
- **Resumable**: Continue from the last processed point after interruption
- **Batch S3 Uploads**: Upload files in parallel for better performance
- **Automatic Extraction**: Extract downloaded ZIP files for immediate use
- **Detailed Logging**: Comprehensive logging for debugging and monitoring
- **Cleanup**: Automatic cleanup of local files after successful upload
- **Rate Limiting Protection**: Configurable delays between operations

## Requirements

- Python 3.7+
- AWS account with S3 bucket and appropriate credentials
- Chrome browser

### Dependencies

```
pip install python-dotenv boto3 pydantic browser-use
```

## Configuration

Create a `.env.mobbin_scraper` file with the following variables:

```
# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=your-mobbin-data-bucket
S3_UPLOAD_WORKERS=10

# Chrome Configuration
CHROME_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
CHROME_PROFILE=Profile 4

# Scraper Configuration
DOWNLOAD_TIMEOUT=60000
MAX_RETRIES=3
RANDOM_DELAY_MIN=2.0
RANDOM_DELAY_MAX=5.0
```

## Input Data

The scraper expects a JSON file named `mobbin_apps_complete.json` in the root directory with the following structure:

```json
[
  {
    "title": "App Name",
    "url": "https://mobbin.com/apps/app-name-identifier/some-id/screens",
    "description": "App description"
  },
  ...
]
```

## Usage

Simply run the script:

```bash
python scrape_mobbin_flow_tree.py
```

If the script is interrupted for any reason, you can restart it, and it will resume from where it left off.

## Directory Structure

The script creates and manages several directories:

- `logs/`: Contains timestamped log files of script execution
- `checkpoints/`: Stores progress checkpoint files for resuming
- `downloads/`: Temporarily stores downloaded ZIP files
- `extracted/`: Temporarily stores extracted content from ZIP files
- `mobbin_flows/`: Stores JSON metadata for each app's flows
- `mobbin_screenshots/`: Stores screenshots of the download process

## S3 Structure

Data is organized in S3 as follows:

```
s3://your-bucket/
└── mobbin_flows/
    ├── App_Name_1/
    │   ├── App_Name_1_flows.json
    │   ├── extracted/
    │   │   └── [Flow content in directories]
    │   └── zips/
    │       └── [Original ZIP files]
    ├── App_Name_2/
    ...
```

## Checkpoint System

The checkpoint system works at multiple levels:

1. **App-level**: Tracks which apps have been processed
2. **Flow-level**: For each app, tracks which flows have been processed
3. **Progress tracking**: Maintains detailed progress information

If the script is stopped for any reason, it will automatically resume from the last checkpoint when restarted.

## Logging

Logs are stored in the `logs/` directory with timestamped filenames. Each log includes:

- Detailed operation steps
- Errors and warnings
- Progress information
- Timing data

## Advanced Configuration

### S3 Upload Performance

Adjust the `S3_UPLOAD_WORKERS` value in the `.env.mobbin_scraper` file to control the number of parallel uploads. A higher value can improve upload speed but may increase resource usage.

### Rate Limiting Protection

Adjust the following values in the `.env.mobbin_scraper` file:
- `RANDOM_DELAY_MIN`: Minimum delay between operations
- `RANDOM_DELAY_MAX`: Maximum delay between operations

### Download Retries

Adjust the `MAX_RETRIES` value to control how many times the script will retry failed downloads.

## Troubleshooting

### Script Crashing

Check the log files in the `logs/` directory for detailed error information. Common issues include:

- Network connectivity problems
- AWS credentials not configured correctly
- Chrome browser issues

### Failed Downloads

The script automatically retries failed downloads. If downloads consistently fail:

1. Check your internet connection
2. Verify the Mobbin structure hasn't changed
3. Try increasing the `DOWNLOAD_TIMEOUT` value

### S3 Upload Issues

If S3 uploads fail:

1. Verify your AWS credentials
2. Check S3 bucket permissions
3. Ensure your AWS region is correctly set

## Development

### Code Structure

- **Main function**: `scrape_all_apps()` - Orchestrates the entire process
- **App processing**: `scrape_flows_for_app()` - Handles individual app processing
- **S3 uploading**: `upload_app_data_to_s3()` - Manages batch uploads to S3
- **Checkpoint functions**: `save_checkpoint()` and `load_checkpoint()` - Handle progress tracking

### Adding Features

To extend the scraper:

1. Add new functionality within the appropriate function
2. Update checkpoint logic if necessary
3. Add new logging for the new feature
4. Test with a small subset of apps

## License

This project is available for personal use. Please respect Mobbin's terms of service when using this tool.

## Disclaimer

This tool is provided for educational purposes only. Always respect website terms of service and don't overload their servers with excessive requests.




