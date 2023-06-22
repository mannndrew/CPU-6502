import sys
import re

# Variables
linenum = 1
filename = ""
defines = {}
checkpoints = {}
checkpoint_count = 0

instructions = {"ADC", "AND", "ASL", "BBR", "BBS", "BCC", "BCS", "BEQ", "BIT", "BMI", "BNE", "BPL", "BRA", "BRK", "BVC", 
                "BVS", "CLC", "CLD", "CLI", "CLV", "CMP", "CPX", "CPY", "DEC", "DEX", "DEY", "EOR", "INC", "INX", "INY",
                "JMP", "JSR", "LDA", "LDX", "LDY", "LSR", "NOP", "ORA", "PHA", "PHP", "PHX", "PHY", "PLA", "PLP", "PLX",
                "PLY", "RMB", "ROL", "ROR", "RTI", "RTS", "SBC", "SEC", "SED", "SEI", "SMB", "STA", "STP", "STX", "STY",
                "STZ", "TAX", "TAY", "TRB", "TSB", "TSX", "TXA", "TXS", "TYA", "WAI"}



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

        # Check if the line is an instruction
        elif words[0] in instructions:

            argument = ""

            if (words.__len__() == 2):
                argument = words[1]
                
            elif (words.__len__() == 3):
                argument = words[1] + " " + words[2]

            else:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nInvalid number of arguments")
                exit(2)


            #print(argument)
            














            # Parse argument

            # Immediate
            if (argument[0] == "#"):
                
                # Immediate Hex
                if (argument[1] == "$"):
                    
                    if (len(argument[2:]) == 2):
                        if (valid_hex(argument[2:])):
                            hex = argument[2:]
                            print(f"Immediate Hex: {hex}")
                        else:
                            print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                            exit(2)
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                # Immediate Dec
                elif (len(argument[1:]) == 3):
                    
                    if valid_dec(argument[1:]):
                        dec = argument[1:]
                        hex = dec_to_2hex(dec)
                        check_length(dec, hex, 2, line, linenum)
                        print(f"Immediate Dec: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                else:
                    print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                    exit(2)


            # Direct Addressing Hex
            elif (argument[0] == "$"):
                if (len(argument[1:]) == 2):
                    if (valid_hex(argument[1:3])):
                        hex = argument[1:3]
                        print(f"Zero Page: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                elif (len(argument[1:]) == 5):
                    if (valid_hex(argument[1:3]) and argument[3:6].__eq__(", X")):
                        hex = argument[1:3]
                        print(f"Zero Page, X: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                elif (len(argument[1:]) == 4):
                    if (valid_hex(argument[1:5])):
                        hex = argument[1:5]
                        print(f"Absolute: {hex}")
                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                elif (len(argument[1:]) == 7):
                    if valid_hex(argument[1:5]):
                        if argument[5:8].__eq__(", X"):
                            hex = argument[1:5]
                            print(f"Absolute, X: {hex}") 
                        elif argument[5:8].__eq__(", Y"):
                            hex = argument[1:5]
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
                            print(f"Zero Page Indirect: {hex}")
                        else:
                            print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                            exit(2)

                    elif (len(argument[2:]) == 6):
                        if (valid_hex(argument[2:4]) and argument[4:].__eq__(", X)")):
                            hex = argument[2:4]
                            print(f"Zero Page Indirect, X: {hex}")
                        elif (valid_hex(argument[2:4]) and argument[4:].__eq__("), Y")):
                            hex = argument[2:4]
                            print(f"Zero Page Indirect, Y: {hex}")
                        else:
                            print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                            exit(2)

                    else:
                        print(f"**Syntax Error Line ({linenum}): {line}**\nInvalid operand {argument}")
                        exit(2)

                # Indirect Addressing Dec
                # elif (argument.__len__() == 6):

                    


                

                        

            

            
                
                    































        
    # print(words)
    linenum += 1

#print(f'{defines}\n\n')
#print(checkpoints)




# Close file
file.close()
