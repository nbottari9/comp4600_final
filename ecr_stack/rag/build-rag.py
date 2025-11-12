import argparse
import os
import asyncio
import aiohttp
import boto3

# IMPORTANT: IF UPLOADING TO A CONTAINER REGISTRY, YOU MUST SPECIFY A OCI-IMAGE-NAME AND NOT A DIRECTORY FOR THE TARGET

VERBOSE=False
target_folder = "./html-data"
s3_client = boto3.client("s3")

if __name__ == "__main__":
    main()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Produce a RAG DB given a file of URLs."
    )

    # Required positional arguments
    parser.add_argument(
        "links-file-path",
        required=True,
        help="Path to the links file (required)."
    )
    parser.add_argument(
        "target",
        required=True,
        help="Target OCI image name (required)."
    )
    parser.add_argument(
        "registry-uri",
        required=True,
        help="URI of container registry"
    )
    parser.add_argument(
        "s3-bucket-name",
        help="S3 bucket name. HTML data uploaded here. (optional)"
    )

    # Optional -v flag for verbose output
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )
    
    args = parse_args()
    VERBOSE = args.verbose

    valid_modes = ["local", "local-mac", "container-registry"]
    if args.mode not in valid_modes:
        parser.error(f"Error: Invalid mode '{args.mode}'. Must be one of {', '.join(valid_modes)}.")

    if args.mode == "container-registry" and not in args.registry_uri:
        parser.error("Error: --registry-uri is required with mode 'container-registry'")
    
    return args 


def main():
    args = parse_args()
    log(f"Links file: {args.links-file-path}")
    log(f"Mode: {args.mode}")
    log(f"Target (OCI/directory): {args.target}")
    log(f"Registry URI: {args.registry-uri}") if args.registry-uri else pass

    build_db()
    cleanup()

def log(message, verbose):
    """Print message only if verbose is enabled."""
    if VERBOSE:
        print(f"[VERBOSE] {message}")

async def fetch_data(links-path: str):
    print("Downloading data...")
    if s3_bucket:
        async with aiohttp.ClientSession() as session:
            tasks = [download_and_upload(session, url) for url in urls]
            await asyncio.gather(*tasks)
    else:
        async with aiohttp.ClientSession as session:
            tasks = [download_file(session, url) for url in urls]
            await asyncio.gather(*tasks)
                 
async def download_and_upload(session, url):
    """Download a file from URL and upload directly to S3."""
    key = url.split("/")[-1]  # S3 object key (filename)
    
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            log(f"Downloading {url} -> s3://{s3_bucket}/{key}")
            
            # Buffer content in memory
            file_buffer = io.BytesIO()
            async for chunk in response.content.iter_chunked(8192):
                file_buffer.write(chunk)
            
            file_buffer.seek(0)  # rewind buffer
            s3_client.upload_fileobj(file_buffer, s3_bucket, key)
            log(f"Uploaded {key} to S3 successfully!")

    except aiohttp.ClientError as e:
        log(f"Failed to download {url}: {e}")
    except boto3.exceptions.Boto3Error as e:
        log(f"Failed to upload {url} to S3: {e}")

async def download_file(session, url):
    """Download a single file from URL asynchronously."""
    filename = target_folder / Path(url).name
    counter = 1
    while filename.exists():
        filename = target_folder / f"{filename.stem}_{counter}{filename.suffix}"
        counter += 1

    try:
        async with session.get(url) as response:
            response.raise_for_status()
            print(f"Downloading {url} -> {filename}")
            with open(filename, "wb") as f:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
    except aiohttp.ClientError as e:
        print(f"Failed to download {url}: {e}")
 
def build_db(args):
    fetch_data(args.links-file-path, args.s3-bucket-name if args.s3-bucket-name else None)
    vectorize(

