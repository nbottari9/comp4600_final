#!/bin/bash

# Check if an input file was provided
if [[ -z "$1" ]]; then
  echo "$0: Usage: $0 <file_with_urls>"
  exit 1
fi

mkdir -p html

echo "Downloading data..."

while IFS= read -r line; do
    outfile="$(echo "$line" | sed 's/[^A-Za-z0-9._-]/_/g').html"
    curl -sL "$line" -o "./html/$outfile"
    
done < "$1"
