import re

def process_lexical_entry(entry, seen_terms):
    """
    Processes a single lexical entry, extracting Sanskrit terms, prefixes, suffixes, 
    and corresponding English meanings along with parts of speech.
    """
    formatted_output = []
    
    # Regular expressions to extract relevant parts
    english_term_regex = r'\{@(.*?)@\}'  # Extracts English term between '{@' and '@}'
    part_of_speech_regex = r'\{%([^%]+)%\}'  # Extracts part of speech between '{%' and '%}'
    sanskrit_term_regex = r'\{#(.*?)#\}'  # Extracts Sanskrit term between '{#' and '#}'
    meaning_variation_regex = r'\{@(\d+)@\}'  # Extracts meaning variation number '{@1@}', '{@2@}', etc.
    
    # Extracting the components of the entry
    english_terms = re.findall(english_term_regex, entry)
    parts_of_speech = re.findall(part_of_speech_regex, entry)
    sanskrit_terms = re.findall(sanskrit_term_regex, entry)
    meaning_variations = re.findall(meaning_variation_regex, entry)
    
    # Default values for prefix, suffix, and root management
    prefix = ""
    suffix = ""
    next_sanskrit_root = ""

    # Process each English term and its corresponding parts
    for i, english_term in enumerate(english_terms):
        part_of_speech = parts_of_speech[i] if i < len(parts_of_speech) else ''
        
        # Check for prefixes/suffixes in English term
        if english_term.endswith('-'):
            prefix = english_term.strip('-')
            continue
        elif english_term.startswith('-'):
            suffix = english_term.strip('-')
            continue
        else:
            # If no prefix/suffix, this is the main English term
            if prefix:
                english_term = f"{prefix}_{english_term}"
                prefix = ""  # Reset the prefix after using it
            
            if suffix:
                english_term = f"{english_term}_{suffix}"
                suffix = ""  # Reset the suffix after using it
        
        # Handle the corresponding Sanskrit term
        if i < len(sanskrit_terms):
            next_sanskrit_root = sanskrit_terms[i]
        else:
            next_sanskrit_root = ""

        # Append the entry with the Sanskrit and English term
        if next_sanskrit_root:
            formatted_output.append(f"{english_term} (#{next_sanskrit_root}#) {{{part_of_speech}}}")

        # Handle meaning variations
        if i < len(meaning_variations):
            formatted_output.append(f"Meaning variation: {meaning_variations[i]}")

    return '\n'.join(formatted_output)


def process_file(input_filename, output_filename):
    """
    Processes the input file, extracting and formatting each lexical entry.
    """
    with open(input_filename, 'r', encoding='utf-8') as infile:
        entries = infile.read().split('<LEND>')  # Assuming entries are separated by '<LEND>'
    
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        seen_terms = set()
        for entry_id, entry in enumerate(entries, start=1):
            if entry.strip():
                processed_entry = process_lexical_entry(entry.strip(), seen_terms)
                outfile.write(f"{processed_entry}\n\n")


# Example usage
if __name__ == "__main__":
    input_filename = ' ../input.txt'
    output_filename = ' ../ska-eng2.txt'
    process_file(input_filename, output_filename)
