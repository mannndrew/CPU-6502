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
addressing_mode = 0
addressing_dict = {}
opcode = ""

instructions = {"ADC", "AND", "ASL", "BBR", "BBS", "BCC", "BCS", "BEQ", "BIT", "BMI", "BNE", "BPL", "BRA", "BRK", "BVC", 
                "BVS", "CLC", "CLD", "CLI", "CLV", "CMP", "CPX", "CPY", "DEC", "DEX", "DEY", "EOR", "INC", "INX", "INY",
                "JMP", "JSR", "LDA", "LDX", "LDY", "LSR", "NOP", "ORA", "PHA", "PHP", "PHX", "PHY", "PLA", "PLP", "PLX",
                "PLY", "RMB", "ROL", "ROR", "RTI", "RTS", "SBC", "SEC", "SED", "SEI", "SMB", "STA", "STP", "STX", "STY",
                "STZ", "TAX", "TAY", "TRB", "TSB", "TSX", "TXA", "TXS", "TYA", "WAI"}



instruction_dict = {
    "ADC": {1: "6D", 3: "7D", 4: "79", 7: "69", 11: "65", 12: "61", 13: "75", 15: "72", 16: "71"}
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

def valid_hex_char(letter):
    if '0' <= letter and letter <= '9':
        return True
    elif 'A' <= letter and letter <= 'F':
        return True
    else:
        return False
    
def valid_hex(operand):
    for letter in operand:
        if not valid_hex_char(letter):
            return False
    return True
    
def valid_dec_char(operand):
    if '0' <= operand and operand <= '9':
        return True
    else:
        return False
    
def valid_dec(operand):
    for letter in operand:
        if not valid_dec_char(letter):
            return False
    return True
    
def dec_to_2hex(operand):
    conversion_table = ['0', '1', '2', '3', 
                        '4', '5', '6', '7', 
                        '8', '9','A', 'B', 
                        'C', 'D', 'E', 'F']
    
    dec = int(operand)
    remainder = 0
    hex = ""
    
    while 0 < dec:
        remainder = dec % 16
        hex = conversion_table[remainder] + hex
        dec = dec // 16

    while len(hex) < 2:
        hex = "0" + hex

    return hex

def dec_to_4hex(operand):
    conversion_table = ['0', '1', '2', '3', 
                        '4', '5', '6', '7', 
                        '8', '9','A', 'B', 
                        'C', 'D', 'E', 'F']
    
    dec = int(operand)
    remainder = 0
    hex = ""
    
    while 0 < dec:
        remainder = dec % 16
        hex = conversion_table[remainder] + hex
        dec = dec // 16

    while len(hex) < 4:
        hex = "0" + hex

    return hex

def check_length(dec, hex, num, line, linenum):
    if len(hex) != num:
        print(f"**Syntax Error Line ({linenum}): ({line})**\nInvalid operand ({dec})")
        exit(2)






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

            if (words.__len__() == 2):
                argument = words[1]
                
            elif (words.__len__() == 3):
                argument = words[1] + " " + words[2]

            else:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nInvalid number of arguments")
                exit(2)










            # Parse argument

            # Immediate
            if (argument[0] == "#"):
                
                # Immediate Hex
                if (argument[1] == "$"):
                    
                    if (len(argument) == 4):
                        if (valid_hex(argument[2:])):
                            hex = argument[2:]
                            addressing_mode = 7 # Immediate Addressing
                            print(f"Immediate Hex: {hex}")
                        else:
                            print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                            exit(2)
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                # Immediate Dec
                elif (len(argument) == 4):
                    
                    if valid_dec(argument[1:]):
                        dec = argument[1:]
                        hex = dec_to_2hex(dec)
                        check_length(dec, hex, 2, line, linenum)
                        addressing_mode = 7 # Immediate Addressing
                        print(f"Immediate Dec: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                else:
                    print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                    exit(2)


            # Direct Addressing Hex
            elif (argument[0] == "$"):
                if (len(argument) == 3):
                    if (valid_hex(argument[1:3])):
                        hex = argument[1:3]
                        addressing_mode = 11 # Zero Page
                        print(f"Zero Page: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                elif (len(argument) == 6):
                    if (valid_hex(argument[1:3]) and argument[3:6].__eq__(", X")):
                        hex = argument[1:3]
                        addressing_mode = 13 # Zero Page Indexed with X
                        print(f"Zero Page, X: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                elif (len(argument) == 5):
                    if (valid_hex(argument[1:5])):
                        hex = argument[1:5]
                        addressing_mode = 1 # Absolute
                        print(f"Absolute: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                elif (len(argument) == 8):
                    if valid_hex(argument[1:5]):
                        if argument[5:8].__eq__(", X"):
                            hex = argument[1:5]
                            addressing_mode = 3 # Absolute Indexed with X
                            print(f"Absolute, X: {hex}") 
                        elif argument[5:8].__eq__(", Y"):
                            hex = argument[1:5]
                            addressing_mode = 4 # Absolute Indexed with Y
                            print(f"Absolute, Y: {hex}")
                        else:
                            print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                            exit(2)
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)
                
                else:
                    print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                    exit(2)
            
            # Indirect Addressing
            elif (argument[0] == "("):

                # Indirect Addressing Hex
                if (argument[1] == "$"):
                    if (len(argument[2:]) == 3):
                        if (valid_hex(argument[2:4]) and argument[4] == ")"):
                            hex = argument[2:4]
                            addressing_mode = 15 # Zero Page Indirect
                            print(f"Zero Page Indirect: {hex}")
                        else:
                            print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                            exit(2)

                    elif (len(argument[2:]) == 6):
                        if (valid_hex(argument[2:4]) and argument[4:].__eq__(", X)")):
                            hex = argument[2:4]
                            addressing_mode = 12 # Zero Page Indexed Indirect
                            print(f"Zero Page Indirect, X: {hex}")
                        elif (valid_hex(argument[2:4]) and argument[4:].__eq__("), Y")):
                            hex = argument[2:4]
                            addressing_mode = 16 # Zero Page Indirect with Indexed
                            print(f"Zero Page Indirect, Y: {hex}")
                        else:
                            print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                            exit(2)

                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                # Indirect Addressing Dec
                elif (len(argument)== 5):
                    if (valid_dec(argument[1:4]) and argument[4] == ")"):
                        dec = argument[1:4]
                        hex = dec_to_2hex(dec)
                        check_length(dec, hex, 2, line, linenum)
                        addressing_mode = 15 # Zero Page Indirect
                        print(f"Zero Page Indirect: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                elif (len(argument) == 8):
                    if (valid_dec(argument[1:4]) and argument[4:].__eq__(", X)")):
                        dec = argument[1:4]
                        hex = dec_to_2hex(dec)
                        check_length(dec, hex, 2, line, linenum)
                        addressing_mode = 12 # Zero Page Indexed Indirect
                        print(f"Zero Page Indirect, X: {hex}")
                    elif (valid_dec(argument[1:4]) and argument[4:].__eq__("), Y")):
                        dec = argument[1:4]
                        hex = dec_to_2hex(dec)
                        check_length(dec, hex, 2, line, linenum)
                        addressing_mode = 16 # Zero Page Indirect with Indexed
                        print(f"Zero Page Indirect, Y: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)
                else:
                    print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                    exit(2)


            ###########################################################################################################
            
            # Zero Page Dec
            elif (len(argument) == 3):
                if (valid_dec(argument)):
                    dec = argument
                    hex = dec_to_2hex(dec)
                    check_length(dec, hex, 2, line, linenum)
                    addressing_mode = 11 # Zero Page
                    print(f"Zero Page: {hex}")
                else:
                    print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                    exit(2)

            # Zero Page, X Dec
            elif (len(argument) == 6):
                if (valid_dec(argument[0:3]) and argument[3:].__eq__(", X")):
                    dec = argument[0:3]
                    hex = dec_to_2hex(dec)
                    check_length(dec, hex, 2, line, linenum)
                    addressing_mode = 13 # Zero Page Indexed with X
                    print(f"Zero Page, X: {hex}")
                else:
                    print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                    exit(2)
            
            # Absolute Dec
            elif (len(argument) == 5):
                if (valid_dec(argument)):
                    dec = argument
                    hex = dec_to_4hex(dec)
                    check_length(dec, hex, 4, line, linenum)
                    addressing_mode = 1 # Absolute
                    print(f"Absolute: {hex}")
                else:
                    print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                    exit(2)
            
            # Absolute, X and Y Dec
            elif (len(argument) == 8):
                if (valid_dec(argument[0:5])):
                    if (argument[5:].__eq__(", X")):
                        dec = argument[0:5]
                        hex = dec_to_4hex(dec)
                        check_length(dec, hex, 4, line, linenum)
                        addressing_mode = 3 # Absolute Indexed with X
                        print(f"Absolute, X: {hex}")
                    elif (argument[5:].__eq__(", Y")):
                        dec = argument[0:5]
                        hex = dec_to_4hex(dec)
                        check_length(dec, hex, 4, line, linenum)
                        addressing_mode = 4 # Absolute Indexed with Y
                        print(f"Absolute, Y: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)
                else:
                    print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                    exit(2)

            else:
                print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                exit(2)

            # Check if addressing mode exists in addressing_dict
            if (addressing_mode in addressing_dict):
                opcode = addressing_dict[addressing_mode]

            else:
                print(f"**Syntax Error Line ({linenum}): {line}**\nInstruction {words[0]} does not support addressing mode {addressing_mode}")
                exit(2)

            # Print opcode and hex in little-endian
            if (len(hex) == 2):
                print(f"{opcode} {hex}")
            elif (len(hex) == 4):
                print(f"{opcode} {hex[2:4]} {hex[0:2]}")
            
            


                    


                

                        

            

            
                
                    































        
    
    linenum += 1


# Close file
file.close()
