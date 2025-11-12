import argparse
import os
import asyncio
import aiohttp
import boto3

VERBOSE=True
s3_client = boto3.client("s3")
BUCKET_NAME=None

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
        "s3-bucket-name",
        required=True,
        help="S3 bucket name. HTML data uploaded here. (required)"
    )

    # Optional -v flag for verbose output
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )
    
    args = parse_args()
    VERBOSE = args.verbose
    BUCKET_NAME = args.s3-bucket-name

    return args 


def main():
    args = parse_args()
    log(f"Links file: {args.links-file-path}")
    log(f"S3 Bucket Name: {BUCKET_NAME}")
    
    fetch_data(args.links-file-path, BUCKET_NAME)

def log(message, verbose):
    """Print message only if verbose is enabled."""
    if VERBOSE:
        print(f"[VERBOSE] {message}")

async def fetch_data(links_path: str, s3_bucket_name=BUCKET_NAME):
    print("Downloading data...")
    with open(links_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    if s3_bucket-name:
        async with aiohttp.ClientSession() as session:
            tasks = [download_and_upload_stream(session, url, s3_bucket_name) for url in urls]
            await asyncio.gather(*tasks)
    else:
        async with aiohttp.ClientSession as session:
            tasks = [download_file(session, url) for url in urls]
            await asyncio.gather(*tasks)
                
class StreamToS3(io.RawIOBase):
    def __init__(self, s3_client, bucket, key):
        self.s3_client = s3_client
        self.bucket = bucket
        self.key = key
        self.buffer = bytearray()

    def write(self, b):
        self.buffer.extend(b)
        if len(self.buffer) > 8*1024*1024:  # upload in 8MB chunks
            self.flush()
        return len(b)

    def flush(self):
        if self.buffer:
            self.s3_client.put_object(Bucket=self.bucket, Key=self.key, Body=self.buffer)
            self.buffer = bytearray()

    def close(self):
        self.flush()

async def download_and_upload_stream(session, url, bucket):
    key = url.split("/")[-1]
    async with session.get(url) as response:
        response.raise_for_status()
        s3_stream = StreamToS3(s3_client, bucket, key)
        async for chunk in response.content.iter_chunked(8192):
            s3_stream.write(chunk)
        s3_stream.close()

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

