import os, re

with open('/home/dell/Documents/GitHub/con_dic/input.txt', 'r', encoding = 'utf-8') as text_file:

    #Read the file content
    content = text_file.read()

    # Define the regular expression pattern
    pattern = re.compile(r'\{@(-.)@\}')
    
    #Find all matches in the context
    matches = pattern.finditer(content)

    #Iterate over the matches and print them 
    for match in matches:
        print(match.group()) # Use .group() to print the matched text 