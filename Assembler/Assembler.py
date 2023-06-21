import sys

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

def valid_operand(letter):
    if '0' <= letter or letter <= '9':
        return True
    elif 'A' <= letter or letter <= 'F':
        return True
    elif 'a' <= letter or letter <= 'f':
        return True
    else:
        return False
    
def dec_to_hex(operand):
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

    return hex





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
            # Create list of blank arguments
            args = [""] * 5
            operand_in = [""] * 100
            operand_hex = ""
            operand_count = 0
            
            hex = False

            operand_first = True
            operand_last = False

            # Read the instruction
            for word in range(1, len(words)):
                for letter in words[word]:

                    # Check if the operand is together

                    if letter == '#':
                        args[0] = '#'
                    elif letter == 'X':
                        args[1] = 'X'
                    elif letter == 'Y':
                        args[2] = 'Y'
                    elif letter == '(':
                        args[3] = '('
                    elif letter == ')':
                        args[4] = ')'
                    elif letter == '$':
                        hex = True
                    elif operand_last or operand_first:
                        operand_in[operand_count] = letter
                        operand_count += 1
                        operand_first = False
                        
                        

                    else:
                        print(f"**Syntax Error Line ({linenum}): ({line})**\nInvalid character ({letter})")
                        exit(2)

                    operand_last = valid_operand(letter)
            
            if (hex == False):
                # Convert operand to hex
                operand_hex = dec_to_hex(''.join(operand_in))
            else:
                operand_hex = ''.join(operand_in)

            
                
                    



            print(args)
            print(operand_hex)




        
        
    print(words)
    linenum += 1

#print(f'{defines}\n\n')
#print(checkpoints)




# Close file
file.close()
