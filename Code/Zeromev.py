import requests
import csv
import os

# Function to get MEV transactions from the API and save to multiple CSV files......
def get_mev_transactions_and_save(start_block, end_block, blocks_per_request, step, output_dir):
    base_url = "https://data.zeromev.org/v1/mevBlock"
    headers = {"Accept": "application/json"}

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for current_block in range(start_block, end_block, step):
        output_csv = f"{output_dir}/mev_transactions_{current_block}_{current_block + step - 1}.csv"
        
        with open(output_csv, mode='w', newline='') as csv_file:
            csv_writer = None
            
            for block in range(current_block, min(current_block + step, end_block), blocks_per_request):
                # Construct the request parameters
                print(block)
                params = {
                    "block_number": block,
                    "count": min(blocks_per_request, end_block - block)
                }
                
                # Perform the API request
                response = requests.get(base_url, headers=headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Initialize CSV writer with headers from the first request
                    if csv_writer is None and data:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                        csv_writer.writeheader()
                    
                    # Write data to CSV file
                    for entry in data:
                        csv_writer.writerow(entry)
                else:
                    print(f"Error fetching data for block {block}: {response.status_code}")
                    break

# Define the block range and parameters
start_block = xxxxx  # based your start block
end_block = xxxxx   # based your end block
blocks_per_request = 10
step = 100000
output_dir = "./" # Replace with the path to your desired output directory

# Call the function to fetch data and save to multiple CSV files
get_mev_transactions_and_save(start_block, end_block, blocks_per_request, step, output_dir)
print("end for get blocks")
