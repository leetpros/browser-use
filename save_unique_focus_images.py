import os
import shutil
import argparse
import logging
import hashlib
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_unique_filename(directory, filename):
    """Generate a unique filename by appending (1), (2), etc., if a file already exists."""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f'{base} ({counter}){ext}'
        counter += 1
    return new_filename

def calculate_sha256(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read the file in chunks to handle large files efficiently
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def save_unique_focus_images(source_dir, output_dir=None):
    """
    Save unique focus images to a separate folder using SHA-256 hashing.
    
    Args:
        source_dir: Directory containing the images
        output_dir: Directory to save unique images (defaults to 'focus_unique' in source_dir)
    
    Returns:
        Path to the output directory
    """
    source_dir = Path(source_dir)
    if not source_dir.exists():
        raise ValueError(f"Source directory {source_dir} does not exist")
    
    # Set default output directory if not provided
    if output_dir is None:
        output_dir = source_dir / 'focus_unique'
    else:
        output_dir = Path(output_dir)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Dictionary to store image hashes and their paths (only first occurrence)
    hash_dict = {}
    duplicate_count = 0
    
    try:
        # Define supported image extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        
        # Get all image files in the directory
        focus_images = []
        for filename in os.listdir(source_dir):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                # Only include images with "focus" in their filename
                if "focus" in filename.lower():
                    focus_images.append(filename)
        
        logger.info(f"Found {len(focus_images)} focus images in {source_dir}")
        
        # Process each focus image
        for filename in focus_images:
            image_path = source_dir / filename
            
            try:
                # Calculate SHA-256 hash
                file_hash = calculate_sha256(image_path)
                
                # Store only the first occurrence of each unique image
                if file_hash not in hash_dict:
                    hash_dict[file_hash] = {'path': image_path, 'duplicates': []}
                else:
                    duplicate_count += 1
                    hash_dict[file_hash]['duplicates'].append(filename)
            except Exception as e:
                logger.warning(f"Error processing image {image_path}: {e}")
        
        # Save unique images to the output folder
        if hash_dict:
            unique_count = len(hash_dict)
            logger.info(f"Found {unique_count} unique images (with {duplicate_count} duplicates)")
            logger.info(f"Saving {unique_count} unique focus images to {output_dir}")
            
            # Copy each unique image to the output folder
            copied_files = []
            for img_hash, data in hash_dict.items():
                image_path = data['path']
                duplicates = data['duplicates']
                
                # Get the filename from the original path
                filename = os.path.basename(image_path)
                # Create the destination path with a unique filename
                dest_filename = get_unique_filename(output_dir, filename)
                dest_path = os.path.join(output_dir, dest_filename)
                
                # Copy the file
                try:
                    shutil.copy2(image_path, dest_path)
                    copied_files.append((img_hash, filename, dest_filename, duplicates))
                    logger.debug(f"Copied {filename} to {dest_path}")
                except Exception as e:
                    logger.error(f"Error copying {filename}: {e}")
            
            # Create a report file
            report_path = output_dir / "unique_focus_images.md"
            with open(report_path, "w") as f:
                f.write("# Unique Focus Screenshots\n\n")
                f.write(f"Found {unique_count} unique focus screenshots out of {len(focus_images)} total focus images ")
                f.write(f"({duplicate_count} duplicates identified).\n\n")
                
                # Group files by hash for better organization
                for img_hash, filename, dest_filename, duplicates in copied_files:
                    f.write(f"- SHA-256: `{img_hash}`\n")
                    f.write(f"  - Saved: `{dest_filename}` (Original: `{filename}`)\n")
                    if duplicates:
                        f.write("  - Duplicates:\n")
                        for dup in duplicates:
                            f.write(f"    - `{dup}`\n")
                    f.write("\n")
            
            logger.info(f"Successfully saved {len(copied_files)} unique images to {output_dir}")
            return output_dir
        else:
            logger.warning("No unique focus images found")
            return None
            
    except Exception as e:
        logger.error(f"Error saving unique images: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Save unique focus images to a separate folder')
    parser.add_argument('source_dir', help='Directory containing the images')
    parser.add_argument('--output-dir', help='Directory to save unique images (defaults to focus_unique in source_dir)')
    
    args = parser.parse_args()
    
    output_dir = save_unique_focus_images(args.source_dir, args.output_dir)
    if output_dir:
        print(f"Unique focus images saved to: {output_dir}")

if __name__ == "__main__":
    main() 