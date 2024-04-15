#!/bin/bash

# Directory containing the .csv.gz files
DIRECTORY="./"

# Change to the directory.
cd "$DIRECTORY"

# Loop through all .csv.gz files and decompress them
for file in *.csv.gz; do
    echo "Decompressing $file..."
    gunzip "$file"
done

echo "Decompression complete."
