import re

# Function to process the input file and extract English terms and Sanskrit transliterations
def process_file(input_file, output_file):
    # Regex pattern to match English terms and their corresponding Sanskrit transliterations
    pattern = r"(\w+)\¦"
    sans = r'.*?{#([^#]+)#}'

    # Open the input file for reading
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()  # Read the entire content of the file

    # Find all matches in the text
    matches = re.findall(pattern, text)
    matches2 = re.findall(sans, text)

    # Open the output file for writing
    with open(output_file, 'w', encoding='utf-8') as f_out:
        # Write the header for the output file
        f_out.write("English Term, Sanskrit Transliteration\n")
        
        # Output the results
        for english_term in matches and sans in matches2:
            # Write each matched pair to the output file
            f_out.write(f"{english_term}, {sans}\n")

    print(f"Processed {len(matches)} matches. Results saved to '{output_file}'.")

# Main function to execute the script
def main():
    input_file = 'input2.txt'  # Replace with your input file name
    output_file = 'last2.txt'  # Desired output file name
    process_file(input_file, output_file)

# Run the program
if __name__ == "__main__":
    main()
