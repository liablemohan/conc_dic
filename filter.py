import re
import csv

# Patterns to match English term, POS tags, and Sanskrit terms
english_term_pattern = r"<k1>(.*?)<k2>"
pos_pattern = r"\{%((?!To).+?)%\}"               # POS tags excluding '{%To%}'
sanskrit_pattern = r"{#(.*?)#}"                  # Sanskrit terms with symbols
sanskrit_filter_pattern = r"\b([a-zA-Z]+H)(?=\s*-|,|\s*$)"  # Sanskrit terms ending in 'H'

# Function to process each entry
def process_entry(entry_text):
    # Extract English term
    english_term = re.search(english_term_pattern, entry_text)
    english_term = english_term.group(1) if english_term else ""
    
    # Extract POS tags (excluding '{%To%}')
    pos_tags = re.findall(pos_pattern, entry_text)
    
    # Extract Sanskrit terms with their brackets and symbols intact
    sanskrit_terms = re.findall(sanskrit_pattern, entry_text)
    
    # Filter each Sanskrit term using a loop and the sanskrit_filter_pattern
    filtered_sanskrit_terms = []
    for term in sanskrit_terms:
        # Apply the filter pattern to each term
        if re.search(sanskrit_filter_pattern, term) and not (term.startswith('-') or term.endswith('-')):
            filtered_sanskrit_terms.append(term)
    
    # Format filtered Sanskrit terms with preserved brackets
    sanskrit_terms_formatted = ", ".join(f"{{#{term}#}}" for term in filtered_sanskrit_terms)
    
    # Return as a tuple
    return (english_term, " | ".join(pos_tags), sanskrit_terms_formatted)

# Main function to read from .txt file and write to .csv file
def process_document(input_file, output_file):
    # Read the input document
    with open(input_file, 'r', encoding='utf-8') as file:
        document = file.read()
    
    # Split document by entries using '<LEND>' as delimiter
    entries = document.split("<LEND>")
    
    # Open the output CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        # Define CSV writer and write the header
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["English Term", "POS Tags", "Sanskrit Terms"])
        
        # Process each entry and write to CSV
        for entry in entries:
            entry = entry.strip()
            if entry:  # Skip empty entries
                row = process_entry(entry)
                csv_writer.writerow(row)

# File paths
input_file = 'input2.txt'  # Input text file
output_file = 'dict2.csv'   # Output CSV file

# Process the document and save to CSV
process_document(input_file, output_file)
print(f"Data successfully written to {output_file}")
