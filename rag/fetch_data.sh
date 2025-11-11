#!/bin/bash

mkdir html

while IFS= read -r line; do
    echo "Downloading $line"
    outfile="$(echo "$line" | sed 's/[^A-Za-z0-9._-]/_/g').html"
    curl -sL "$line" -o "./html/$outfile"
    
done < "$1"