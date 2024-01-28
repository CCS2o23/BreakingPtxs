#!/bin/bash

# Set the start and end dates
START_DATE="20220103"
END_DATE="20231231"

DOMAIN="https://archive.blocknative.com/"

# Initialize variables to track successful and failed downloads
SUCCESSFUL_DOWNLOADS=0
FAILED_DOWNLOADS=0

# Define a delay between requests in seconds
DELAY_BETWEEN_REQUESTS=5

# File to log failed downloads
ERROR_LOG="error.txt"

# Function to increment a date
increment_date() {
    date -I -d "$1 + 1 day"
}

# Function to download data for a single date
download_data_for_date() {
    local DATE=$1

    # Loop through each hour (00 to 23)
    for HOUR in {00..23}; do
        # Construct the URL for the current hour's data
        URL="${DOMAIN}${DATE}/${HOUR}.csv.gz"

        # Define the filename for the current hour's data
        FILENAME="${DATE}_${HOUR}.csv.gz"

        # Initialize a variable to keep track of retries
        RETRIES=0

        # Loop to handle retries on 404, 429, and 504 responses
        while true; do
            # Download the data and check the response status code
            HTTP_STATUS=$(curl -o "$FILENAME" -w "%{http_code}" -L "$URL")

            # Check the status code and print a message
            if [ "$HTTP_STATUS" -eq 200 ]; then
                echo "Downloaded $FILENAME"
                ((SUCCESSFUL_DOWNLOADS++))
                break  # Exit the retry loop on success
            elif [ "$HTTP_STATUS" -eq 429 ] || [ "$HTTP_STATUS" -eq 504 ]; then
                echo "Received $HTTP_STATUS. Retrying in $RETRIES second(s)..."
                sleep $RETRIES  # Wait before retrying
                ((RETRIES++))
                if [ $RETRIES -ge 3 ]; then
                    echo "Retry limit reached. Logging error for $FILENAME."
                    echo "$FILENAME" >> "$ERROR_LOG"
                    ((FAILED_DOWNLOADS++))
                    break
                fi
            elif [ "$HTTP_STATUS" -eq 404 ]; then
                echo "File not found (404). Logging error for $FILENAME."
                echo "$FILENAME" >> "$ERROR_LOG"
                ((FAILED_DOWNLOADS++))
                break  # Exit the retry loop for 404
            else
                echo "Error downloading $FILENAME - Status code: $HTTP_STATUS"
                rm -f "$FILENAME"
                echo "$FILENAME" >> "$ERROR_LOG"
                ((FAILED_DOWNLOADS++))
                break  # Exit the retry loop on other errors
            fi
        done

        # Wait for a specified delay before making the next request
        echo "Waiting for $DELAY_BETWEEN_REQUESTS seconds before the next request..."
        sleep $DELAY_BETWEEN_REQUESTS
    done
}

# Current date starts from the start date
CURRENT_DATE="$START_DATE"

# Loop through each date from start to end
while [[ "$CURRENT_DATE" != $(increment_date "$END_DATE") ]]; do
    download_data_for_date "$CURRENT_DATE"
    # Increment the current date
    CURRENT_DATE=$(increment_date "$CURRENT_DATE")
done

echo "Downloaded $SUCCESSFUL_DOWNLOADS files successfully."
echo "Failed to download $FAILED_DOWNLOADS files. Check $ERROR_LOG for details."
