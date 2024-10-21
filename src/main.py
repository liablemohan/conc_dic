import re

def process_lexical_entry(entry, entry_id):
    # Extract the English term from the entry
    english_term_match = re.search(r"<k1>(.*?)<", entry)
    english_term = english_term_match.group(1) if english_term_match else "Unknown"

    # Extract Sanskrit words in WX notation
    sanskrit_words = re.findall(r"{#(.*?)#}", entry)

    # Extract English meanings and parts of speech
    english_meaning_matches = re.findall(r"{@(.*?)@}", entry)

    # Handle distinct meanings in different lines based on digits in (@@)
    distinct_meanings = [em for em in english_meaning_matches if re.search(r'\d', em)]

    # Handle prefixes and suffixes starting or ending with hyphen (-)
    suffixes_prefixes = [sp for sp in english_meaning_matches if re.search(r'-', sp)]

    # Initialize output for processed entry
    formatted_output = []

    # Iterate over distinct meanings and map them to Sanskrit words
    for idx, meaning in enumerate(distinct_meanings):
        sanskrit_word = sanskrit_words[idx] if idx < len(sanskrit_words) else "Unknown_Sanskrit"
        formatted_output.append(f"{english_term}_{entry_id}.{idx + 1} (#{sanskrit_word}#)_{entry_id}.{idx + 1} "
                                f"{{{meaning}}}_{entry_id}.{idx + 1}")

    # Merge suffixes/prefixes with the English term and append them to output
    for sp in suffixes_prefixes:
        if sp.startswith('-'):
            # Append to the English term if it's a suffix
            formatted_output.append(f"{english_term}{sp}_{entry_id} (#{sanskrit_words[0]}#)_{entry_id} {{}}_{entry_id}" 
                                    if sanskrit_words else f"{english_term}{sp}_{entry_id} (#{'Unknown'}#)_{entry_id} {{}}_{entry_id}")
        elif sp.endswith('-'):
            # Prepend to the English term if it's a prefix
            formatted_output.append(f"{sp[:-1]}{english_term}_{entry_id} (#{sanskrit_words[0]}#)_{entry_id} {{}}_{entry_id}" 
                                    if sanskrit_words else f"{sp[:-1]}{english_term}_{entry_id} (#{'Unknown'}#)_{entry_id} {{}}_{entry_id}")
        else:
            # Handle any other cases (if needed)
            formatted_output.append(f"{english_term}_{entry_id} (#{sanskrit_words[0]}#)_{entry_id} {{}}_{entry_id}" 
                                    if sanskrit_words else f"{english_term}_{entry_id} (#{'Unknown'}#)_{entry_id} {{}}_{entry_id}")

    return formatted_output

def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile:
        entries = infile.read().split("<LEND>")
    
    processed_entries = []
    entry_id = 1  # Starting point for identification numbers

    for entry in entries:
        if entry.strip():  # Process non-empty entries
            processed_entry = process_lexical_entry(entry.strip(), entry_id)
            processed_entries.extend(processed_entry)
            entry_id += 1

    # Write the processed entries to the output file
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write("\n".join(processed_entries))

if __name__ == "__main__":
    input_filename = "input.txt"  # Input file with lexical entries
    output_filename = "output3.txt"  # Output file for processed entries
    process_file(input_filename, output_filename)
