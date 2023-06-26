import sys
import re



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
filename = ""
defines = {}
checkpoints = {}
checkpoint_count = 0
addressing_mode = [0]
addressing_dict = {}
opcode = ""

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
    words = line.split(" ")
    words = list(filter(None, words))
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


# Process file
for line in file:
    line = clean_line(line)
    words = clean_words(line)

    if len(words) != 0:

        # Check if the line is a define
        if words[0].__eq__("define"):
            if len(words) != 3:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nDefine only takes 2 arguments")
                exit(2)
            elif words[1] in defines:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nDefine ({words[1]}) already exists")
                exit(2)
            else:
                defines[words[1]] = words[2]

        # Check if the line is a checkpoint
        elif words[0][-1:] == ":":
            if words[0][:-1] in checkpoints:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nCheckpoint ({words[0][:-1]}) already exists")
                exit(2)
            else:
                checkpoints[words[0][:-1]] = checkpoint_count
                checkpoint_count += 1

        # Check if the line is in instruction dictionary
        elif words[0] in instruction_dict:
            
            addressing_dict = instruction_dict[words[0]]
            argument = ""

            if words.__len__() == 1:
                argument = ""

            if (words.__len__() == 2):
                argument = words[1]
                
            elif (words.__len__() == 3):
                argument = words[1] + " " + words[2]

            else:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nInvalid number of arguments")
                exit(2)










            # Parse argument

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

                    if (1 <= count and count <= 2):
                        addressing_mode = [7] # Immediate Addressing

                elif argument[1] == "$":
                    count = valid_hex(argument[2:])
                    hex = argument[2:count+2]
                    rest = argument[count+2:]

                    if (1 <= count and count <= 2):
                        addressing_mode = [7] # Immediate Addressing

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
            if (len(hex) == 2):
                print(f"{opcode} {hex}")
            elif (len(hex) == 4):
                print(f"{opcode} {hex[2:4]} {hex[0:2]}")
            

    linenum += 1

# Close file
file.close()
