import sys
import dictionary
from helper import *

# Addressing Modes
# 1 = Absolute                             a
# 2 = Absolute Indexed Indirect           (a, x)
# 3 = Absolute Indexed with X              a, x
# 4 = Absolute Indexed with Y              a, y
# 5 = Absolute Indirect                   (a)
# 6 = Accumulator                          A
# 7 = Immediate Addressing                 #
# 8 = Implied Addressing                   i
# 9 = Program Counter Relative             r
# 10 = Stack                               s
# 11 = Zero Page                           zp
# 12 = Zero Page Indexed Indirect         (zp, x)
# 13 = Zero Page Indexed with X            zp, x
# 14 = Zero Page Indexed with Y            zp, y
# 15 = Zero Page Indirect                 (zp)
# 16 = Zero Page Indirect with Indexed    (zp), y

# Variables
linenum = 1
starting_address = 1536
address = starting_address
filename = ""
defines = {}
labels = {}
addressing_mode = [0]
addressing_dict = {}
opcode = ""
hexdump = []

# Dictionaries
instruction_dict = dictionary.instruction_dict
jump_dict = dictionary.jump_dict



################################################################################################################################

# Check if the user has provided a file name
if len(sys.argv) != 2:
    print("Usage: python assembler.py <filename>")
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


# Process file
for line in file:
    line = clean_line(line)
    words = split_instruction(line)
    


    if len(words) != 0:

        # Check if the line is a define
        if words[0].__eq__("define") or words[0].__eq__("DEFINE"):
            argument = words[1].split(" ")
            argument = list(filter(None, argument))

            if len(words) != 2:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nDefine only takes 2 arguments")
                exit(2)
            elif argument[0] in defines:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nDefine ({argument[0]}) already exists")
                exit(2)
            else:
                defines[argument[0]] = argument[1]

        # Check if the line is a label
        elif words[0][-1:] == ":":
            if len(words) != 1:
                print(f"**Syntax Error Line ({linenum}): ({line})**\Label only takes 1 argument")
                exit(2)
            elif words[0][:-1] in labels:
                print(f"**Syntax Error Line ({linenum}): ({line})**\Label ({words[0][:-1]}) already exists")
                exit(2)
            else:
                labels[words[0][:-1]] = address

        # Check if the line is in instruction dictionary
        elif words[0] in instruction_dict:
            
            # Check if the instruction is a jump instruction
            if words[0] in jump_dict:
                if (len(words) != 2):
                    print(f"**Syntax Error Line ({linenum}): ({line})**\nJump instruction takes 1 argument")
                    exit(2)

                hexdump.append([words[0], words[1], jump_dict[words[0]]])
                for i in range(jump_dict[words[0]]):
                    hexdump.append([])

                address += jump_dict[words[0]] + 1

            else:
                addressing_dict = instruction_dict[words[0]]
                addressing_mode = []
                argument = ""
                hex = ""

                if len(words) == 2:
                    argument = words[1]
                    for name in defines:
                        argument = argument.replace(name, defines[name])

                # Parse argument
                hex, addressing_mode = parse_argument(argument)

                # Check if addressing mode exists in addressing_dict
                if (addressing_mode[0] == 0):
                    print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid argument {argument}")
                    exit(2)
                
                for num in addressing_mode:
                    if num in addressing_dict:
                        opcode = addressing_dict[num]

                if (opcode == ""):
                    print(f"**Syntax Error Line ({linenum}): {line}**\nInstruction {words[0]} does not support addressing mode {addressing_mode}")
                    exit(2)

                hex = fix_hex(hex)

                # Print opcode and hex in little-endian
                if (len(hex) == 0):
                    hexdump.append(f"{opcode}")
                    address += 1
                elif (len(hex) == 2):
                    hexdump.append(f"{opcode}")
                    hexdump.append(f"{hex[0:2]}")
                    address += 2
                elif (len(hex) == 4):
                    hexdump.append(f"{opcode}")
                    hexdump.append(f"{hex[2:4]}")
                    hexdump.append(f"{hex[0:2]}")
                    address += 3
            
    linenum += 1


# Sort defines and labels longest to shortest
defines = dict(sorted(defines.items(), key=lambda item: len(item[0]), reverse=True))
labels = dict(sorted(labels.items(), key=lambda item: len(item[0]), reverse=True))


# Reiterate through hexdump to replace labels
address = starting_address
count = len(hexdump)

for i in range(len(hexdump)):

    
    if type(hexdump[i]) == list and hexdump[i] != []:

        # hexdump[i][0] = instruction
        # hexdump[i][1] = argument
        # hexdump[i][2] = jump type
        
        addressing_dict = instruction_dict[hexdump[i][0]]
        addressing_mode = [0]
        opcode = ""
        hex = ""

        for label in labels:
            if label in hexdump[i][1]:
                
                # Relative
                if hexdump[i][2] == 1:
                    relative_address = ((labels[label] - address - 2) % 256)
                    hexdump[i][1] = hexdump[i][1].replace(label, str(relative_address))
                    # address += 1

                # Absolute
                elif hexdump[i][2] == 2:
                    absolute_address = labels[label]
                    hexdump[i][1] = hexdump[i][1].replace(label, str(absolute_address))
                    # address += 2
                
        # Parse argument
        hex, addressing_mode = parse_argument(hexdump[i][1])
        
        # Check if addressing mode exists in addressing_dict
        if (addressing_mode[0] == 0):
            print(f"**Invalid argument {hexdump[i][1]}**")
            exit(2)
        
        for num in addressing_mode:
            if num in addressing_dict:
                opcode = addressing_dict[num]

        if (opcode == ""):
            print(f"**Addressing mode {addressing_mode} not supported by instruction {hexdump[i][0]}**")
            exit(2)

        hex = fix_hex(hex)

        # Print opcode and hex in little-endian
        if (len(hex) == 2):
            hexdump[i] = (f"{opcode}")
            hexdump[i+1] = (f"{hex[0:2]}")
        elif (len(hex) == 4):
            hexdump[i] = (f"{opcode}")
            hexdump[i+1] = (f"{hex[2:4]}")
            hexdump[i+2] = (f"{hex[0:2]}")
        else:
            print(f"**Invalid hex {hex}**")
            exit(2)

    address += 1
        
# Close read file
file.close()



# Open write file
file = open(filename[:-4] + ".hex", "w")

# Write hexdump to file
# address = starting_address

for address in range(0x10000):
    if (address < starting_address):
        if address % 16 == 0:
            file.write(f"{address:04x}: ")
            
        file.write(f"00 ")

        if address % 16 == 15:
            file.write("\n")

    elif (starting_address <= address and 
          address < starting_address + len(hexdump)):

            if address % 16 == 0:
                file.write(f"{address:04x}: ")

            file.write(f"{hexdump[address - starting_address]} ")

            if address % 16 == 15:
                file.write("\n")

    else:
        if address % 16 == 0:
            file.write(f"{address:04x}: ")
            
        file.write(f"00 ")

        if address % 16 == 15:
            file.write("\n")


# Close write file
file.close()



# Exit program
exit(0)
