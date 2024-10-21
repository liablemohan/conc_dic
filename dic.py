import re
import csv

def parse_entry(entry_text):
    # Parse an individual entry
    entry_dict = {}
    
    # Extract entry number from the entry
    L_match = re.search(r'<L>(\d+)<pc>(\d+)<k1>(.*?)<k2>(.*?)\n', entry_text)
    if L_match:
        entry_dict['Entry_No'] = L_match.group(1)

    # Initialize lists to store transliterations, definitions, and examples
    transliterations = []
    definitions = []
    examples = []

    # Find definitions, examples, and transliterations
    definition_match = re.findall(r'{@(.*?)}¦\s*(.*?)({#(.*?)#}|\'(.*?)\'|$)', entry_text, re.DOTALL)
    if definition_match:
        for group in definition_match:
            # Extract transliteration
            transliteration = re.findall(r'{#(.*?)#}', group[2])  # Get transliteration
            if transliteration:
                transliterations.extend(transliteration)  # Add to the list
            
            # Extract examples
            example = group[4]  # Single quoted example
            if example:
                examples.append(example)

            # Append word info (remove '@') and definition
            word_info = group[0].strip().replace('@', '')  # Remove '@'
            definition = group[1].strip()
            definitions.append((word_info, definition))

    entry_dict['Transliteration'] = ', '.join(transliterations)  # Combine transliterations
    entry_dict['Examples'] = ', '.join(examples)  # Combine examples into a string
    entry_dict['Definitions'] = definitions  # Store definitions as a list of tuples

    return entry_dict

def extract_entries(text):
    entries = re.split(r'<LEND>', text)  # Split by entry end marker
    parsed_entries = []
    
    for entry in entries:
        entry = entry.strip()
        if entry:  # Skip empty entries
            parsed_entry = parse_entry(entry)
            if parsed_entry:
                parsed_entries.append(parsed_entry)
    
    return parsed_entries

def write_entries_to_file(entries, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        # Write header
        file.write(f"{'Entry No':<10} {'Word Info':<30} {'Definition':<60} {'Transliteration'}\n")
        file.write("="*150 + "\n")  # Separator line
        
        for entry in entries:
            if 'Entry_No' in entry:
                entry_no = entry['Entry_No']
                
                # Write each definition on a new line
                for word_info, definition in entry.get('Definitions', []):
                    transliteration = entry.get('Transliteration', '')  # Get transliteration
                    examples = entry.get('Examples', '')  # Get examples
                    file.write(f"{entry_no:<10} {word_info:<30} {definition:<60} {transliteration}\n")
                    
            file.write("\n")  # New line between entries

def write_entries_to_csv(entries, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header
        csv_writer.writerow(['Entry No', 'Word Info', 'Definition', 'Transliteration'])
        
        for entry in entries:
            if 'Entry_No' in entry:
                entry_no = entry['Entry_No']
                
                # Write each definition on a new row
                for word_info, definition in entry.get('Definitions', []):
                    transliteration = entry.get('Transliteration', '')  # Get transliteration
                    csv_writer.writerow([entry_no, word_info, definition, transliteration])

# Read the input file
input_file_path = 'input.txt'  # Change this path as needed
with open(input_file_path, 'r', encoding='utf-8') as file:
    text_data = file.read()

# Extract the entries
entries = extract_entries(text_data)

# Write the extracted entries to a txt file
output_file_path = 'out_dict12.txt'  # Change this path as needed
write_entries_to_file(entries, output_file_path)

# Write the extracted entries to a csv file
csv_file_path = 'out_dict12.csv'  # Change this path as needed
write_entries_to_csv(entries, csv_file_path)

print(f"Output written to {output_file_path} and {csv_file_path}")
