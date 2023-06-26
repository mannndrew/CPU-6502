argument = "123"
addressing_mode = [-1]
hex = -1

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

if addressing_mode[0] == [-1]:
    print("Invalid Argument")
else:
    print(addressing_mode)
    
print(hex)