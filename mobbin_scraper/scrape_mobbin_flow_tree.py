import os
import sys
import asyncio
import json
import random
import shutil
import zipfile
import boto3
import logging
import concurrent.futures
import time
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional, Union, cast
from botocore.exceptions import NoCredentialsError

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from browser_use import Browser, BrowserConfig, BrowserContextConfig

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from the specific .env file
load_dotenv(dotenv_path=os.path.join(SCRIPT_DIR, '.env.mobbin_scraper'))

# Set up logging
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"mobbin_scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mobbin_scraper")

# Checkpoint file paths
CHECKPOINT_DIR = os.path.join(SCRIPT_DIR, "checkpoints")
os.makedirs(CHECKPOINT_DIR, exist_ok=True)
APPS_CHECKPOINT_FILE = os.path.join(CHECKPOINT_DIR, "apps_progress.json")
FLOWS_CHECKPOINT_FILE = os.path.join(CHECKPOINT_DIR, "flows_progress.json")

# Define base directories
DOWNLOADS_DIR = os.path.join(SCRIPT_DIR, "downloads")
EXTRACTED_DIR = os.path.join(SCRIPT_DIR, "extracted")
FLOWS_DIR = os.path.join(SCRIPT_DIR, "flows")
MOBBIN_FLOWS_DIR = os.path.join(SCRIPT_DIR, "mobbin_flows")
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "mobbin_screenshots")

# Create base directories
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(EXTRACTED_DIR, exist_ok=True)
os.makedirs(FLOWS_DIR, exist_ok=True)
os.makedirs(MOBBIN_FLOWS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

class FlowTreeItem(BaseModel):
    """A flow tree item with title, link, and interaction count"""
    title: str = Field(description="The title of the flow")
    link: str = Field(description="The URL to the flow")
    count: int = Field(description="Number of interactions in the flow")
    clicked: bool = Field(default=False, description="Whether the action button was clicked")
    downloaded: bool = Field(default=False, description="Whether the flow was downloaded")
    unzipped: bool = Field(default=False, description="Whether the flow was successfully unzipped")

def save_checkpoint(checkpoint_file: str, data: Union[Dict, List]) -> None:
    """Save checkpoint data to file"""
    try:
        with open(checkpoint_file, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Checkpoint saved to {checkpoint_file}")
    except Exception as e:
        logger.error(f"Failed to save checkpoint to {checkpoint_file}: {str(e)}")

def load_checkpoint(checkpoint_file: str) -> Optional[Union[Dict, List]]:
    """Load checkpoint data from file if it exists"""
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                data = json.load(f)
            logger.info(f"Checkpoint loaded from {checkpoint_file}")
            return data
        except Exception as e:
            logger.error(f"Failed to load checkpoint from {checkpoint_file}: {str(e)}")
    return None

def upload_single_file(args: Tuple[str, str, str, str]) -> bool:
    """Upload a single file to S3, used for parallel uploads"""
    local_path, bucket_name, s3_path, file_type = args
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(local_path, bucket_name, s3_path)
        return True
    except Exception as e:
        logger.error(f"Error uploading {file_type} file {local_path}: {str(e)}")
        return False

def upload_to_s3(local_directory, bucket_name, s3_directory):
    """Upload directory contents to an S3 bucket in parallel and return success status"""
    try:
        # Check if directory exists
        if not os.path.exists(local_directory):
            logger.warning(f"Directory not found: {local_directory}")
            return False
        
        # Get the max number of threads from environment variables or default to 10
        max_workers = int(os.environ.get('S3_UPLOAD_WORKERS', 10))
        
        # Collect all files to upload
        upload_tasks = []
        total_files = 0
        
        # Walk through all files in the directory
        for root, dirs, files in os.walk(local_directory):
            for file in files:
                # Get full local path and relative path for S3
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_directory)
                s3_path = os.path.join(s3_directory, relative_path).replace("\\", "/")
                
                # Add to upload tasks
                upload_tasks.append((local_path, bucket_name, s3_path, "directory"))
                total_files += 1
        
        # If no files to upload
        if total_files == 0:
            logger.info(f"No files found in {local_directory}")
            return True
            
        logger.info(f"Preparing to upload {total_files} files from {local_directory} to s3://{bucket_name}/{s3_directory}")
        
        # Use ThreadPoolExecutor for parallel uploads
        successful_uploads = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(upload_single_file, upload_tasks))
            successful_uploads = sum(results)
        
        # Report results
        logger.info(f"Uploaded {successful_uploads}/{total_files} files to S3")
        return successful_uploads == total_files  # Return True only if all uploads succeeded
        
    except NoCredentialsError:
        logger.error("S3 credentials not found. Please configure AWS credentials.")
        return False
    except Exception as e:
        logger.error(f"Error in batch upload to S3: {str(e)}")
        return False

def unzip_flow(zip_path, extract_dir):
    """Unzip a flow archive and return success status"""
    try:
        if not os.path.exists(zip_path):
            logger.warning(f"Zip file not found: {zip_path}")
            return False
            
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        logger.info(f"Successfully unzipped: {zip_path}")
        return True
    except zipfile.BadZipFile:
        logger.error(f"Invalid zip file: {zip_path}")
        return False
    except Exception as e:
        logger.error(f"Error unzipping {zip_path}: {str(e)}")
        return False

async def scrape_flows_for_app(app_data: Dict[str, str], browser: Browser, save_screenshots_path: str) -> List[Dict[str, Any]]:
    """Scrape flows for a single app"""
    app_name = app_data['title'].replace(' ', '_')
    app_downloads_dir = os.path.join(DOWNLOADS_DIR, app_name)
    app_extracted_dir = os.path.join(EXTRACTED_DIR, app_name)
    
    # Load flow checkpoint if it exists
    app_flow_checkpoint = os.path.join(CHECKPOINT_DIR, f"flow_{app_name}.json")
    existing_flows = load_checkpoint(app_flow_checkpoint)
    
    # Get configuration from environment variables
    download_timeout = int(os.environ.get('DOWNLOAD_TIMEOUT', 60000))
    max_retries = int(os.environ.get('MAX_RETRIES', 3))
    min_delay = float(os.environ.get('RANDOM_DELAY_MIN', 1.0))
    max_delay = float(os.environ.get('RANDOM_DELAY_MAX', 3.0))
    
    logger.info(f"Starting to process app: {app_data['title']}")
    
    try:
        browser_context = await browser.new_context()
        page = await browser_context.get_current_page()
        
        # Extract app ID from URL
        app_url = app_data['url']
        app_id = app_url.split('/')[-2]  # Get the second to last part of the URL
        
        # Construct flows URL
        flows_url = app_url
        
        # Create app-specific directories
        app_screenshot_dir = os.path.join(save_screenshots_path, app_name)
        os.makedirs(app_screenshot_dir, exist_ok=True)
        os.makedirs(app_downloads_dir, exist_ok=True)
        os.makedirs(app_extracted_dir, exist_ok=True)
        
        # Check if we already have flows data from checkpoint
        flow_items: List[Dict[str, Any]] = []
        if existing_flows and isinstance(existing_flows, list):
            logger.info(f"Resuming from checkpoint with {len(existing_flows)} flows for {app_name}")
            flow_items = existing_flows
        else:
            # Collect all flow items from flows URL
            logger.info(f"Navigating to {flows_url} to collect flows")
            await page.goto(flows_url)
            await asyncio.sleep(random.uniform(min_delay, max_delay))  # Random delay after page load
            
            try:
                await page.wait_for_selector('div[data-sentry-component="FlowsTree"]', timeout=30000)
                await page.wait_for_selector('li[data-tree-node-id]', timeout=30000)
                
                flow_nodes = await page.query_selector_all('li[data-tree-node-id]')
                
                for node in flow_nodes:
                    await asyncio.sleep(random.uniform(0.2, 0.7))  # Random delay between node processing
                    node_id = await node.get_attribute('data-tree-node-id')
                    title_elem = await node.query_selector('span.grow.truncate.text-fg-primary')
                    title = await title_elem.text_content() if title_elem else "No Title"
                    title = title.strip() if title else "No Title"
                    
                    count_elem = await node.query_selector('span.text-compact.text-fg-tertiary')
                    count_text = await count_elem.text_content() if count_elem else "0"
                    count = int(count_text) if count_text and count_text.isdigit() else 0
                    
                    link = f"https://mobbin.com/flows/{node_id}?tab=prototype" if node_id else flows_url
                    
                    flow_items.append(FlowTreeItem(
                        title=title,
                        link=link,
                        count=count
                    ).model_dump())

                    if len(flow_items) == 5:
                        break
                
                # Save flow items to checkpoint
                save_checkpoint(app_flow_checkpoint, flow_items)
                logger.info(f"Collected {len(flow_items)} flows for app {app_name}")
                
            except Exception as e:
                logger.error(f"Error collecting flows for {app_name}: {str(e)}")
                if len(flow_items) == 0:
                    logger.error(f"No flows collected for {app_name}, skipping app")
                    return []

        # Load app processing checkpoint
        progress_checkpoint = os.path.join(CHECKPOINT_DIR, f"progress_{app_name}.json")
        progress_data = load_checkpoint(progress_checkpoint)
        processed_flows_dict: Dict[str, Any] = {"processed_flows": []} if not progress_data or not isinstance(progress_data, dict) else progress_data
        processed_flows = set(processed_flows_dict.get("processed_flows", []))

        # Process each flow (skip already processed ones)
        for index, flow in enumerate(flow_items):
            flow_title = flow['title']
            if flow_title in processed_flows:
                logger.info(f"Skipping already processed flow: {flow_title} for app: {app_data['title']}")
                continue
                
            logger.info(f"Processing flow {index+1}/{len(flow_items)}: {flow_title} for app: {app_data['title']}")
            
            # Generate safe flow title once
            safe_flow_title = flow_title.replace('/', '_').replace('\\', '_').replace(':', '_')
            safe_flow_title = ''.join(c for c in safe_flow_title if c.isalnum() or c in '_-.')[:200]
            
            # Create flow-specific directory for extracted files
            flow_extract_dir = os.path.join(app_extracted_dir, safe_flow_title)
            os.makedirs(flow_extract_dir, exist_ok=True)
            
            # Check if this flow was already downloaded successfully
            zip_path = os.path.join(app_downloads_dir, f"{safe_flow_title}.zip")
            if os.path.exists(zip_path) and os.listdir(flow_extract_dir):
                logger.info(f"Flow {flow_title} already downloaded and extracted, skipping download")
                flow['downloaded'] = True
                flow['unzipped'] = True
                processed_flows.add(flow_title)
                processed_flows_dict["processed_flows"] = list(processed_flows)
                save_checkpoint(progress_checkpoint, processed_flows_dict)
                continue
            
            # Attempt download with retries
            retry_count = 0
            while retry_count < max_retries:
                try:
                    await page.goto(flow['link'])
                    await asyncio.sleep(random.uniform(min_delay, max_delay))  # Random delay after navigation
                    
                    # First click: Open options menu
                    menu_selector = (
                        'span[data-sentry-source-file="FlowActionsDropdownMenu.tsx"] '
                        '> button[data-sentry-source-file="FlowModalPrototypeFooter.tsx"]'
                    )
                    await page.wait_for_selector(menu_selector, timeout=20000)
                    menu_button = await page.query_selector(menu_selector)
                    
                    if not menu_button:
                        logger.warning(f"Menu button not found with selector: {menu_selector}")
                        retry_count += 1
                        if retry_count < max_retries:
                            logger.info(f"Retrying ({retry_count}/{max_retries})...")
                            await asyncio.sleep(random.uniform(1.0, 3.0))
                            continue
                        else:
                            break
                    
                    await menu_button.hover()
                    await asyncio.sleep(random.uniform(0.5, 1.2))  # Random delay after hover
                    await menu_button.click(delay=random.randint(100, 200))  # Random click delay

                    # Second click: Download button
                    download_selector = (
                        'div[data-sentry-element="AbstractMenuItem"] '
                        'div:has-text("Download screens as PNG")'
                    )
                    
                    await asyncio.sleep(random.uniform(0.8, 1.5))
                    
                    await page.wait_for_selector(download_selector, state="visible", timeout=15000)
                    download_button = await page.query_selector(download_selector)
                    
                    if not download_button:
                        logger.warning(f"Download button not found for {flow_title}")
                        retry_count += 1
                        if retry_count < max_retries:
                            logger.info(f"Retrying ({retry_count}/{max_retries})...")
                            await asyncio.sleep(random.uniform(1.0, 3.0))
                            continue
                        else:
                            break
                    
                    async with page.expect_download(timeout=download_timeout) as download_info:
                        await download_button.click(delay=random.randint(80, 150))
                        logger.info(f"Initiated download for {flow_title}")
                    
                    download = await download_info.value
                    logger.info(f"Download completed for {flow_title}")
                    
                    # Generate filename for zip
                    zip_filename = f"{safe_flow_title}.zip"
                    zip_path = os.path.join(app_downloads_dir, zip_filename)
                    
                    # Save the file
                    await download.save_as(zip_path)
                    logger.info(f"Saved download to {zip_path}")
                    
                    flow['downloaded'] = True
                    screenshot_path = os.path.join(app_screenshot_dir, f"{safe_flow_title}_downloaded.png")
                    await page.screenshot(path=screenshot_path)
                    logger.info(f"Captured screenshot to {screenshot_path}")
                    
                    # Unzip the downloaded file
                    unzip_success = unzip_flow(zip_path, flow_extract_dir)
                    flow['unzipped'] = unzip_success
                    
                    if unzip_success:
                        logger.info(f"Successfully extracted files to {flow_extract_dir}")
                    else:
                        logger.error(f"Failed to extract {zip_path}")
                    
                    # Mark flow as processed
                    processed_flows.add(flow_title)
                    processed_flows_dict["processed_flows"] = list(processed_flows)
                    save_checkpoint(progress_checkpoint, processed_flows_dict)
                    
                    # Update flow checkpoint
                    save_checkpoint(app_flow_checkpoint, flow_items)
                    
                    # Success - break out of retry loop
                    break
                    
                except Exception as e:
                    logger.error(f"Error downloading {flow_title}: {str(e)}")
                    retry_count += 1
                    if retry_count < max_retries:
                        logger.info(f"Retrying ({retry_count}/{max_retries})...")
                        await asyncio.sleep(random.uniform(2.0, 5.0))
                    else:
                        flow['downloaded'] = False
                        flow['unzipped'] = False
                        logger.error(f"Failed to download {flow_title} after {max_retries} attempts")
            
            # Delay before next flow
            await asyncio.sleep(random.uniform(min_delay * 2, max_delay * 2))  # Random longer delay for downloads

        # Save flows for this app
        app_flows_file = os.path.join(MOBBIN_FLOWS_DIR, f"{app_name}_flows.json")
        os.makedirs(MOBBIN_FLOWS_DIR, exist_ok=True)
        with open(app_flows_file, "w") as f:
            json.dump(flow_items, f, indent=4)
        logger.info(f"Saved flow data to {app_flows_file}")

        return flow_items

    except Exception as e:
        logger.error(f"Error processing app {app_data['title']}: {str(e)}")
        return []
    finally:
        await browser_context.close()

async def upload_app_data_to_s3(app_name, app_downloads_dir, app_extracted_dir, flow_json_path, s3_bucket):
    """Upload all data for an app to S3 using batch uploads"""
    s3_directory = f"mobbin_flows/{app_name}"
    upload_success_extracted = False
    upload_success_zips = False
    
    # Upload flow JSON data first (it's small and important)
    if os.path.exists(flow_json_path):
        try:
            s3_client = boto3.client('s3')
            json_s3_path = f"{s3_directory}/{app_name}_flows.json"
            s3_client.upload_file(flow_json_path, s3_bucket, json_s3_path)
            logger.info(f"Uploaded flow metadata to s3://{s3_bucket}/{json_s3_path}")
        except Exception as e:
            logger.error(f"Error uploading flow metadata: {str(e)}")
    
    # Upload the extracted files in batch if they exist
    if os.path.exists(app_extracted_dir) and os.listdir(app_extracted_dir):
        logger.info(f"Batch uploading extracted files for {app_name}...")
        upload_success_extracted = upload_to_s3(app_extracted_dir, s3_bucket, f"{s3_directory}/extracted")
        if upload_success_extracted:
            logger.info(f"Successfully uploaded all extracted files for {app_name}")
        else:
            logger.warning(f"Some files failed to upload for {app_name}")
    
    # Upload the original zip files in batch
    if os.path.exists(app_downloads_dir) and os.listdir(app_downloads_dir):
        logger.info(f"Batch uploading zip files for {app_name}...")
        upload_success_zips = upload_to_s3(app_downloads_dir, s3_bucket, f"{s3_directory}/zips")
        if upload_success_zips:
            logger.info(f"Successfully uploaded all zip files for {app_name}")
        else:
            logger.warning(f"Some zip files failed to upload for {app_name}")
    
    # Return overall success status
    return upload_success_extracted or upload_success_zips

async def scrape_all_apps():
    save_screenshots_path = SCREENSHOTS_DIR
    
    start_time = time.time()
    logger.info("Starting Mobbin scraping process")
    
    # Get S3 settings from environment variables
    s3_bucket = os.environ.get('S3_BUCKET_NAME')
    if not s3_bucket:
        logger.warning("S3_BUCKET_NAME environment variable not set. S3 upload will be skipped.")
    
    # Load apps from JSON file
    apps_json_path = os.path.join(SCRIPT_DIR, "mobbin_apps_complete.json")
    with open(apps_json_path, "r") as f:
        all_apps = json.load(f)
    
    # Load checkpoint to see which apps have been processed
    checkpoint_data = load_checkpoint(APPS_CHECKPOINT_FILE)
    checkpoint_dict: Dict[str, Any] = {"processed_apps": [], "current_index": 0}
    
    if checkpoint_data and isinstance(checkpoint_data, dict):
        checkpoint_dict = checkpoint_data
        
    processed_apps = set(checkpoint_dict["processed_apps"])
    start_index = checkpoint_dict["current_index"]
    
    logger.info(f"Found {len(all_apps)} apps total. {len(processed_apps)} already processed. Starting from index {start_index}.")
    
    # Skip already processed apps
    apps_to_process = all_apps[start_index:]
    
    chrome_path = os.environ.get('CHROME_PATH', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    chrome_profile = os.environ.get('CHROME_PROFILE', 'Profile 4')
    
    browser = Browser(config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            save_screenshots_path=save_screenshots_path,
            browser_window_size={'width': 1980, 'height': 1200}
        ),
        chrome_instance_path=chrome_path,
        extra_chromium_args=[
            f'--profile-directory={chrome_profile}'
        ]
    ))
    
    try:
        all_flows = []
        for index, app in enumerate(apps_to_process):
            current_index = start_index + index
            app_name = app['title'].replace(' ', '_')
            
            # Skip if already processed
            if app_name in processed_apps:
                logger.info(f"Skipping already processed app: {app['title']}")
                continue
                
            app_downloads_dir = os.path.join(DOWNLOADS_DIR, app_name)
            app_extracted_dir = os.path.join(EXTRACTED_DIR, app_name)
            
            logger.info(f"\nProcessing app {current_index+1}/{len(all_apps)}: {app['title']}")
            
            # Update checkpoint before processing
            checkpoint_dict["current_index"] = current_index
            save_checkpoint(APPS_CHECKPOINT_FILE, checkpoint_dict)
            
            # Process the app
            flows = await scrape_flows_for_app(app, browser, save_screenshots_path)
            all_flows.extend(flows)
            
            # Mark app as processed
            processed_apps.add(app_name)
            checkpoint_dict["processed_apps"] = list(processed_apps)
            checkpoint_dict["current_index"] = current_index + 1
            save_checkpoint(APPS_CHECKPOINT_FILE, checkpoint_dict)
            
            # Upload to S3 if bucket name is set
            if s3_bucket:
                logger.info(f"Uploading {app_name} data to S3...")
                flow_json_path = os.path.join(MOBBIN_FLOWS_DIR, f"{app_name}_flows.json")
                
                # Upload all app data in batch
                upload_success = await upload_app_data_to_s3(
                    app_name, app_downloads_dir, app_extracted_dir, flow_json_path, s3_bucket
                )
                
                # Clean up local files if upload was successful
                if upload_success:
                    logger.info(f"Cleaning up local downloads for {app_name}...")
                    if os.path.exists(app_downloads_dir):
                        shutil.rmtree(app_downloads_dir, ignore_errors=True)
                    if os.path.exists(app_extracted_dir):
                        shutil.rmtree(app_extracted_dir, ignore_errors=True)
                    logger.info(f"Local downloads for {app_name} deleted.")
                else:
                    logger.warning(f"S3 upload failed, keeping local files for {app_name}")
            
            # Add delay between apps to avoid rate limiting
            if index < len(apps_to_process) - 1:  # Don't delay after the last app
                delay = random.uniform(10.0, 15.0)
                logger.info(f"Waiting {delay:.1f} seconds before processing next app...")
                await asyncio.sleep(delay)

        elapsed_time = time.time() - start_time
        logger.info(f"\nCompleted processing {len(processed_apps)}/{len(all_apps)} apps in {elapsed_time:.2f} seconds")
        logger.info(f"Total flows processed: {len(all_flows)}")
        logger.info(f"Successfully downloaded: {len([f for f in all_flows if f.get('downloaded', False)])}")
        logger.info(f"Successfully unzipped: {len([f for f in all_flows if f.get('unzipped', False)])}")
        
        # Clear checkpoint if all apps are processed
        if len(processed_apps) == len(all_apps):
            logger.info("All apps processed successfully! Clearing checkpoint.")
            if os.path.exists(APPS_CHECKPOINT_FILE):
                os.remove(APPS_CHECKPOINT_FILE)
            
        return all_flows

    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        return []
    finally:
        await browser.close()

if __name__ == '__main__':
    try:
        asyncio.run(scrape_all_apps())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user. Progress has been saved to checkpoints.")
        logger.info("Run the script again to resume from where you left off.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.info("Progress has been saved to checkpoints. Run the script again to resume.")
        sys.exit(1)