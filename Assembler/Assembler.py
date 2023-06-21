import sys

# Variables
linenum = 1
filename = ""
defines = {}
checkpoints = {}
checkpoint_count = 0
instructions = ["ADC", "AND", "ASL", "BBR", "BBS", "BCC", "BCS", "BEQ", "BIT", "BMI", "BNE", "BPL", "BRA", "BRK", "BVC", 
                "BVS", "CLC", "CLD", "CLI", "CLV", "CMP", "CPX", "CPY", "DEC", "DEX", "DEY", "EOR", "INC", "INX", "INY",
                "JMP", "JSR", "LDA", "LDX", "LDY", "LSR", "NOP", "ORA", "PHA", "PHP", "PHX", "PHY", "PLA", "PLP", "PLX",
                "PLY", "RMB", "ROL", "ROR", "RTI", "RTS", "SBC", "SEC", "SED", "SEI", "SMB", "STA", "STP", "STX", "STY",
                "STZ", "TAX", "TAY", "TRB", "TSB", "TSX", "TXA", "TXS", "TYA", "WAI"]

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

# Process file
for line in file:
    line = clean_line(line)
    words = clean_words(line)

    if len(words) != 0:
        if words[0].__eq__("define"):
            if len(words) != 3:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nDefine only takes 2 arguments")
                exit(2)
            elif words[1] in defines:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nDefine ({words[1]}) already exists")
                exit(2)
            else:
                defines[words[1]] = words[2]

        elif words[0][-1:] == ":":
            if words[0][:-1] in checkpoints:
                print(f"**Syntax Error Line ({linenum}): ({line})**\nCheckpoint ({words[0][:-1]}) already exists")
                exit(2)
            else:
                checkpoints[words[0][:-1]] = checkpoint_count
                checkpoint_count += 1

        
        
    print(words)
    linenum += 1

print(f'{defines}\n\n')
print(checkpoints)


# Close file
file.close()
