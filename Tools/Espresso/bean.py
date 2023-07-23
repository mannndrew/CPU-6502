import sys
import os


# Check if espresso is compiled
if not os.path.exists("bin/espresso"):
    # Change directory to espresso-src
    os.chdir("espresso-src")
    # Compile espresso
    os.system("make -B")
    # Change directory back to original
    os.chdir("..")


# open input file
try:
    file_one = open('input-hex/one.txt', 'r')
    file_dcs = open('input-hex/dcs.txt', 'r')
except IOError:
    print("Failed to open file")
    sys.exit()

one = []
dcs = []

# read hex file
dup = set()
for line in file_one:
    hex = line.strip()
    # Check if empty
    if hex == '': continue
    # Check if duplicate
    if hex in dup: continue
    else: dup.add(hex)
    binary_val = bin(int(hex, 16))[2:].zfill(8)
    one.append(binary_val)

# read dcs file
dup = set()
for line in file_dcs:
    hex = line.strip()
    # Check if empty
    if hex == '': continue
    # Check if duplicate
    if hex in dup: continue
    else: dup.add(hex)
    space_val = bin(int(hex, 16))[2:].zfill(8)
    dcs.append(space_val)

# close file
file_one.close()
file_dcs.close()

# Move to bin directory
os.chdir("bin")

# open output file
file_output = open("data.txt", 'w')

# print to file output.txt
file_output.write(".i 8\n")
file_output.write(".o 1\n")

# print ones
for i in range(len(one)):
    file_output.write(one[i] + " " + "1\n")

# print dcs
for i in range(len(dcs)):
    file_output.write(dcs[i] + " " + "-\n")

# Close output file
file_output.close()



# Run espresso
os.system("./espresso data.txt")




