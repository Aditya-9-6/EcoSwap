import csv
import os

input_file = r'C:\Users\om laptop house\ecoswap\data\Amazon.csv'
output_file = r'C:\Users\om laptop house\ecoswap\data\sustainable_products.csv'

# Define the columns we need
fieldnames = ['Product', 'Alternative', 'ImpactScore', 'Link', 'Description']

data = []

if os.path.exists(input_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Map Amazon columns to EcoSwap columns
            # We don't have a 'Product' (the bad thing), so we'll leave it generic so 'Alternatives' search picks it up.
            item = {
                'Product': 'Eco-Friendly Item', # Context for RAG
                'Alternative': row.get('Title', 'Unknown Product')[:100], # Trucate for display
                'ImpactScore': 9, # Default high score for these curated items
                'Link': row.get('alinknormal_URL', 'https://amazon.com'),
                'Description': row.get('Title', '')
            }
            data.append(item)

# Write the new format
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Successfully converted {len(data)} items from Amazon.csv to sustainable_products.csv")
