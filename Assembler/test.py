import sys


# Check if the user has provided a file name
if len(sys.argv) != 2:
    print("Usage: python Assembler.py <filename>")
    exit(2)

# Check if the file exists
try:
    filename = sys.argv[1]
    file = open(filename, "r")
except FileNotFoundError:
    print(f"File ({filename}) not found")
    exit(2)

# Check if the file is asm
if filename[-4:] != ".asm":
    print(f"File ({filename}) is not an asm file")
    exit(2)

def clean_line(line):
    line = line.split(";")[0]
    line = line.strip()
    return line

def clean_words(line):
    words = line.split(maxsplit=1)
    return words

# Process file
for line in file:
    line = clean_line(line)
    words = clean_words(line)
    if len(words) == 2:
        words[1] = words[1].replace("movingUp", "1")
        
    print(words)