import sys

########################################################### File IO ###########################################################

# Check if the user has provided a file name
if len(sys.argv) != 2:
    print("Usage: python simulator.py <filename>")
    exit(2)

# Get the file name
filename = sys.argv[1]

# Check if the file is hex
if filename[-4:] != ".hex":
    print(f"File ({filename}) is not an hex file")
    exit(2)

# Check if the file exists
try:
    file = open(filename, "r")
except FileNotFoundError:
    print(f"File ({filename}) not found")
    exit(2)

# Store hex file in memory
memory = []

for line in file:
    clean_line = line[6:].strip()
    for i in range(0, len(clean_line), 3):
        memory.append(clean_line[i:i+2])

# Close file
file.close()


########################################################### Simulator ###########################################################
print(memory)