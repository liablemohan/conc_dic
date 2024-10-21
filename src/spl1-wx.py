# Mapping from SLP1 to WX notation
slp1_to_wx = {
    'a': 'a', 'A': 'A', 'i': 'i', 'I': 'I', 'u': 'u', 'U': 'U', 'f': 'q', 'F': 'Q',
    'x': 'L', 'e': 'e', 'E': 'E', 'o': 'o', 'O': 'O', 'M': 'M', 'H': 'H',
    'k': 'k', 'K': 'K', 'g': 'g', 'G': 'G', 'N': 'f', 'c': 'c', 'C': 'C', 'j': 'j',
    'J': 'J', 'Y': 'F', 'w': 't', 'W': 'T', 'q': 'd', 'Q': 'D', 't': 'w', 'T': 'W', 'd': 'x',
    'D': 'X', 'n': 'n', 'p': 'p', 'P': 'P', 'b': 'b', 'B': 'B', 'm': 'm', 'y': 'y',
    'r': 'r', 'l': 'l', 'v': 'v', 'S': 'S', 'z': 'R', 's': 's', 'h': 'h', 'L': 'l',
}

def slp1_to_wx_convert(text):
    """Convert a string from SLP1 to WX notation."""
    wx_text = ''.join([slp1_to_wx.get(char, char) for char in text])
    return wx_text

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            new_line = ''
            i = 0
            while i < len(line):
                if line[i:i+2] == '(#':  # Detect "(#"
                    new_line += '(#'
                    i += 2
                    inner_text = ''
                    while i < len(line) and line[i:i+2] != '#)':  # Until "#)"
                        inner_text += line[i]
                        i += 1
                    new_line += slp1_to_wx_convert(inner_text)  # Convert SLP1 to WX
                    new_line += '#)'  # Add the closing "#)"
                    i += 2
                else:
                    new_line += line[i]
                    i += 1
            outfile.write(new_line)

if __name__ == "__main__":
    input_file = 'ae.txt'   # Input file path
    output_file = 'ae-wx.txt' # Output file path
    process_file(input_file, output_file)
    print("Conversion completed. Check the output file.")
