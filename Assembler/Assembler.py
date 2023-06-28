import sys

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

instruction_dict = {
    "ADC":  {1: "6D", 3: "7D", 4: "79", 7: "69", 11: "65", 12: "61", 13: "75", 15: "72", 16: "71"},
    "AND":  {1: "2D", 3: "3D", 4: "39", 7: "29", 11: "25", 12: "21", 13: "35", 15: "32", 16: "31"},
    "ASL":  {1: "0E", 3: "1E", 6: "0A", 11: "06", 13: "16"},
    "BBR0": {9: "0F"},
    "BBR1": {9: "1F"},
    "BBR2": {9: "2F"},
    "BBR3": {9: "3F"},
    "BBR4": {9: "4F"},
    "BBR5": {9: "5F"},
    "BBR6": {9: "6F"},
    "BBR7": {9: "7F"},
    "BBS0": {9: "8F"},
    "BBS1": {9: "9F"},
    "BBS2": {9: "AF"},
    "BBS3": {9: "BF"},
    "BBS4": {9: "CF"},
    "BBS5": {9: "DF"},
    "BBS6": {9: "EF"},
    "BBS7": {9: "FF"},
    "BCC":  {9: "90"},
    "BCS":  {9: "B0"},
    "BEQ":  {9: "F0"},
    "BIT":  {1: "2C", 3: "3C", 7: "89", 11: "24", 13: "34"},
    "BMI":  {9: "30"},
    "BNE":  {9: "D0"},
    "BPL":  {9: "10"},
    "BRA":  {9: "80"},
    "BRK":  {10: "00"},
    "BVC":  {9: "50"},
    "BVS":  {9: "70"},
    "CLC":  {8: "18"},
    "CLD":  {8: "D8"},
    "CLI":  {8: "58"},
    "CLV":  {8: "B8"},
    "CMP":  {1: "CD", 3: "DD", 4: "D9", 7: "C9", 11: "C5", 12: "C1", 13: "D5", 15: "D2", 16: "D1"},
    "CPX":  {1: "EC", 7: "E0", 11: "E4"},
    "CPY":  {1: "CC", 7: "C0", 11: "C4"},
    "DEC":  {1: "CE", 3: "DE", 6: "3A", 11: "C6", 13: "D6"},
    "DEX":  {8: "CA"},
    "DEY":  {8: "88"},
    "EOR":  {1: "4D", 3: "5D", 4: "59", 7: "49", 11: "45", 12: "41", 13: "55", 15: "52", 16: "51"},
    "INC":  {1: "EE", 3: "FE", 6: "1A", 11: "E6", 13: "F6"},
    "INX":  {8: "E8"},
    "INY":  {8: "C8"},
    "JMP":  {1: "4C", 2: "7C", 5: "6C"},
    "JSR":  {1: "20"},
    "LDA":  {1: "AD", 3: "BD", 4: "B9", 7: "A9", 11: "A5", 12: "A1", 13: "B5", 15: "B2", 16: "B1"},
    "LDX":  {1: "AE", 4: "BE", 7: "A2", 11: "A6", 14: "B6"},
    "LDY":  {1: "AC", 3: "BC", 7: "A0", 11: "A4", 13: "B4"},
    "LSR":  {1: "4E", 3: "5E", 6: "4A", 11: "46", 13: "56"},
    "NOP":  {8: "EA"},
    "ORA":  {1: "0D", 3: "1D", 4: "19", 7: "09", 11: "05", 12: "01", 13: "15", 15: "12", 16: "11"},
    "PHA":  {10: "48"},
    "PHP":  {10: "D8"},
    "PHX":  {10: "DA"},
    "PHY":  {10: "5A"},
    "PLA":  {10: "68"},
    "PLP":  {10: "28"},
    "PLX":  {10: "FA"},
    "PLY":  {10: "7A"},
    "RMB0": {11: "07"},
    "RMB1": {11: "17"},
    "RMB2": {11: "27"},
    "RMB3": {11: "37"},
    "RMB4": {11: "47"},
    "RMB5": {11: "57"},
    "RMB6": {11: "67"},
    "RMB7": {11: "77"},
    "ROL":  {1: "2E", 3: "3E", 6: "2A", 11: "26", 13: "36"},
    "ROR":  {1: "6E", 3: "7E", 6: "6A", 11: "66", 13: "76"},
    "RTI":  {10: "40"},
    "RTS":  {10: "60"},
    "SBC":  {1: "ED", 3: "FD", 4: "F9", 7: "E9", 11: "E5", 12: "E1", 13: "F5", 15: "F2", 16: "F1"},
    "SEC":  {8: "38"},
    "SED":  {8: "F8"},
    "SEI":  {8: "78"},
    "SMB0": {11: "87"},
    "SMB1": {11: "97"},
    "SMB2": {11: "A7"},
    "SMB3": {11: "B7"},
    "SMB4": {11: "C7"},
    "SMB5": {11: "D7"},
    "SMB6": {11: "E7"},
    "SMB7": {11: "F7"},
    "STA":  {1: "8D", 3: "9D", 4: "99", 11: "85", 12: "81", 13: "95", 15: "92", 16: "91"},
    "STP":  {8: "DB"},
    "STX":  {1: "8E", 11: "86", 14: "96"},
    "STY":  {1: "8C", 11: "84", 13: "94"},
    "STZ":  {1: "9C", 3:"9E", 11: "64", 13: "74"},
    "TAX":  {8: "AA"},
    "TAY":  {8: "A8"},
    "TRB":  {1: "1C", 11: "14"},
    "TSB":  {1: "0C", 11: "04"},
    "TSX":  {8: "BA"},
    "TXA":  {8: "8A"},
    "TXS":  {8: "9A"},
    "TYA":  {8: "98"},
    "WAI":  {8: "CB"}
}

jump_dict = {
    "BBR0": 1,
    "BBR1": 1,
    "BBR2": 1,
    "BBR3": 1,
    "BBR4": 1,
    "BBR5": 1,
    "BBR6": 1,
    "BBR7": 1,
    "BBS0": 1,
    "BBS1": 1,
    "BBS2": 1,
    "BBS3": 1,
    "BBS4": 1,
    "BBS5": 1,
    "BBS6": 1,
    "BBS7": 1,
    "BCC": 1,
    "BCS": 1,
    "BEQ": 1,
    "BMI": 1,
    "BNE": 1,
    "BPL": 1,
    "BRA": 1,
    "BVC": 1,
    "BVS": 1,
    "JMP": 2,
    "JSR": 2
}

def clean_line(line):
    line = line.split(";")[0]
    line = line.strip()
    return line

def split_instruction(line):
    words = line.split(maxsplit=1)
    return words

def valid_dec_char(operand):
    if '0' <= operand and operand <= '9':
        return True
    else:
        return False
    
def valid_dec(operand):
    count = 0
    for letter in operand:
        if not valid_dec_char(letter):
            return count
        count += 1
    return count

def dec_to_hex(operand):
    conversion_table = ['0', '1', '2', '3', 
                        '4', '5', '6', '7', 
                        '8', '9','A', 'B', 
                        'C', 'D', 'E', 'F']
    
    dec = int(operand)
    remainder = 0
    hex = ""

    if dec == 0: return "0"
    
    while 0 < dec:
        remainder = dec % 16
        hex = conversion_table[remainder] + hex
        dec = dec // 16

    return hex

def valid_hex_char(letter):
    if '0' <= letter and letter <= '9':
        return True
    elif 'A' <= letter and letter <= 'F':
        return True
    else:
        return False
    
def valid_hex(operand):
    count = 0
    for letter in operand:
        if not valid_hex_char(letter):
            return count
        count += 1
    return count

def fix_hex(operand):
    if len(operand) % 2 == 1:
        return "0" + operand
    else:
        return operand
    
def parse_argument(argument):
    hex = ""
    addressing_mode = [0]

    if argument == "":
        addressing_mode = [8, 10] # Implied Addressing / Stack

    elif argument[0] == "A" and len(argument) == 1:
        addressing_mode = [6] # Accumulator

    elif valid_dec_char(argument[0]):
        count = valid_dec(argument)
        hex = dec_to_hex(argument[0:count])
        rest = argument[count:]
        count = len(hex)

        if (1 <= count and count <= 2):
            if rest == "":
                addressing_mode = [9, 11] # Program Counter Relative / Zero Page
            elif rest == ", X":
                addressing_mode = [13] # Zero Page Indexed with X
            elif rest == ", Y":
                addressing_mode = [14] # Zero Page Indexed with Y

        elif (3 <= count and count <= 4):
            if rest == "":
                addressing_mode = [1] # Absolute
            elif rest == ", X":
                addressing_mode = [3] # Absolute Indexed with X
            elif rest == ", Y":
                addressing_mode = [4] # Absolute Indexed with Y

    elif argument[0] == "$":
        count = valid_hex(argument[1:])
        hex = argument[1:count+1]
        rest = argument[count+1:]

        if (1 <= count and count <= 2):
            if rest == "":
                addressing_mode = [9, 11] # Program Counter Relative / Zero Page
            elif rest == ", X":
                addressing_mode = [13] # Zero Page Indexed with X
            elif rest == ", Y":
                addressing_mode = [14] # Zero Page Indexed with Y

        elif (3 <= count and count <= 4):
            if rest == "":
                addressing_mode = [1] # Absolute
            elif rest == ", X":
                addressing_mode = [3] # Absolute Indexed with X
            elif rest == ", Y":
                addressing_mode = [4] # Absolute Indexed with Y

    elif argument[0] == "(":
        if valid_dec_char(argument[1]):
            count = valid_dec(argument[1:])
            hex = dec_to_hex(argument[1:count+1])
            rest = argument[count+1:]
            count = len(hex)

            if (1 <= count and count <= 2):
                if rest == ")":
                    addressing_mode = [15] # Zero Page Indirect
                elif rest == ", X)":
                    addressing_mode = [12] # Zero Page Indexed Indirect
                elif rest == "), Y":
                    addressing_mode = [16] # Zero Page Indirect with Indexed

            elif (3 <= count and count <= 4):
                if rest == ")":
                    addressing_mode = [5] # Absolute Indirect
                elif rest == ", X)":
                    addressing_mode = [2] # Absolute Indexed Indirect

        elif argument[1] == "$":
            count = valid_hex(argument[2:])
            hex = argument[2:count+2]
            rest = argument[count+2:]

            if (1 <= count and count <= 2):
                if rest == ")":
                    addressing_mode = [15] # Zero Page Indirect
                elif rest == ", X)":
                    addressing_mode = [12] # Zero Page Indexed Indirect
                elif rest == "), Y":
                    addressing_mode = [16] # Zero Page Indirect with Indexed

            elif (3 <= count and count <= 4):
                if rest == ")":
                    addressing_mode = [5] # Absolute Indirect
                elif rest == ", X)":
                    addressing_mode = [2] # Absolute Indexed Indirect

    elif argument[0] == "#":
        if valid_dec_char(argument[1]):
            count = valid_dec(argument[1:])
            hex = dec_to_hex(argument[1:count+1])
            rest = argument[count+1:]
            count = len(hex)

            if (1 <= count and count <= 2 and rest == ""):
                addressing_mode = [7] # Immediate Addressing

        elif argument[1] == "$":
            count = valid_hex(argument[2:])
            hex = argument[2:count+2]
            rest = argument[count+2:]

            if (1 <= count and count <= 2 and rest == ""):
                addressing_mode = [7] # Immediate Addressing
    return hex, addressing_mode


################################################################################################################################

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


# Process file
for line in file:
    line = clean_line(line)
    words = split_instruction(line)


    if len(words) != 0:

        # Check if the line is a define
        if words[0].__eq__("define"):
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
                jump_instruction = jump_dict[words[0]]
                jump_info = [words[0], words[1], jump_instruction]
                hexdump.append(jump_info)
                address += jump_instruction + 1

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

# Reiterate through hexdump to replace labels
address = starting_address
for i in range(len(hexdump)):
    
    if type(hexdump[i]) == list:
        for label in labels:
            if label in hexdump[i][1]:
                jump_address = labels[label]
                jump_instruction = hexdump[i][0]
                jump_argument = hexdump[i][1]
                jump_type = hexdump[i][2]
                hex = ""

                # Relative
                if jump_type == 1:
                    relative_address = ((jump_address - address - 2) % 256)
                    new_arg = jump_argument.replace(label, str(relative_address))
                    hex, addressing_mode = parse_argument(new_arg)
                    print(hex, addressing_mode)
                    address += 2

                # Absolute
                elif jump_type == 2:
                    pass
    else:
        
        address += 1

        

print(hexdump)
print(labels)
# Close file
file.close()
