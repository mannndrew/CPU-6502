import sys
import time
import readchar


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

# Print welcome message
print(f"Welcome to the W65C02S simulator!\n")

# Store hex file in memory
memory = []

# Print loading message
print("Loading in hexdump...")

for line in file:
    clean_line = line[6:].strip()
    for i in range(0, len(clean_line), 3):
        memory.append(clean_line[i:i+2])

# Close file
file.close()

# Convert char to int
for i in range(len(memory)):
    memory[i] = int(memory[i], 16)

# Print loading message
print(f"Hexdump loaded successfully!\n")


########################################################### Functions #########################################################


def cycle():
    readchar.readkey()

def hex_value(dec):
    conversion_table = ['0', '1', '2', '3',
                        '4', '5', '6', '7',
                        '8', '9','A', 'B',
                        'C', 'D', 'E', 'F']
    
    remainder = 0
    hex = ""

    if dec == 0:
        return "00"

    while 0 < dec:
        remainder = dec % 16
        hex = conversion_table[remainder] + hex
        dec = dec // 16

    if len(hex) == 1:
        hex = "0" + hex
    
    return hex

def print_registers(message, offset, reg):

    print(f"{message:<{offset}}"
          f"A: {hex_value(reg['reg_a'])}\t"
          f"X: {hex_value(reg['reg_x'])}\t"
          f"Y: {hex_value(reg['reg_y'])}\t"
          f"SP: {hex_value(reg['reg_sp'])}\t"
          f"PC: {hex_value(reg['reg_pch'])}{hex_value(reg['reg_pcl'])}")

def inc_pc(reg):
    if reg["reg_pch"] == 0xFF and reg["reg_pcl"] == 0xFF:
        reg["reg_pch"] = 0x00
        reg["reg_pcl"] = 0x00

    elif reg["reg_pcl"] == 0xFF:
        reg["reg_pch"] += 0x01
        reg["reg_pcl"] = 0x00
    
    else:
        reg["reg_pcl"] += 0x01

    return reg

def add(a, b):
    return (a + b) & 0xFF


########################################################### Simulation ########################################################


# Default addresses
zero_page_begin = 0x0000
zero_page_end = 0x00FF
stack_pointer_end = 0x0100
stack_pointer_begin = 0x01FF
data_begin = 0x0200
data_end = 0x07FF
program_begin = 0x8000
program_end = 0xFFFF

# Default vectors
nonmaskable_interupt_vector_high = 0xFFFA
nonmaskable_interupt_vector_low = 0xFFFB
reset_vector_high = 0xFFFC
reset_vector_low = 0xFFFD
interupt_vector_high = 0xFFFE
interupt_vector_low = 0xFFFF

# Registers
reg = {
    "reg_x": 0x00,
    "reg_y": 0x00,
    "reg_sp": 0xFF,
    "reg_a": 0x00,
    "reg_pch": 0x00,
    "reg_pcl": 0x00,
    "reg_indirh": 0x00,
    "reg_indirl": 0x00,
    "reg_dirh": 0x00,
    "reg_dirl": 0x00,
    "reg_flags": 0x00,
    "reg_inst": 0x00,
    "reg_data": 0x00
}

print(f"Beginning simulation...\n")

# Fetch instruction: 1 cycle

reg["reg_pch"] = program_begin >> 8
reg["reg_pcl"] = program_begin & 0xFF
address = (reg["reg_pch"] << 8) | reg["reg_pcl"]

while True:
    match memory[address]:
        case 0x00:
            # BRK: 7 cycles
            print(f"---BRK s Instruction at address {hex(address)}---")

            # Fetch instruction: 1 cycle
            print_registers("1. Fetching instruction BRK", 50, reg)
            cycle()
            reg = inc_pc(reg)

            # Push PCH to stack
            print_registers("2. Pushing PCH to stack", 50, reg)
            cycle()
            memory[reg["reg_sp"]] = reg["reg_pch"]
            reg["reg_sp"] -= 0x01

            # Push PCL to stack
            print_registers("3. Pushing PCL to stack", 50, reg)
            cycle()
            memory[reg["reg_sp"]] = reg["reg_pcl"]
            reg["reg_sp"] -= 0x01

            # Push flags to stack with break set
            print_registers("4. Pushing flags to stack with break set", 50, reg)
            cycle()
            reg["reg_flags"] |= 0b00010000
            memory[reg["reg_sp"]] = reg["reg_flags"]
            reg["reg_sp"] -= 0x01

            # Set interrupt disable flag
            print_registers("5. Setting interrupt disable flag", 50, reg)
            cycle()
            reg["reg_flags"] |= 0b00000100

            # Load interrupt vector low byte
            print_registers("6. Loading interrupt vector low byte", 50, reg)
            cycle()
            reg["reg_pcl"] = memory[nonmaskable_interupt_vector_low]

            # Load interrupt vector high byte
            print_registers(f"7. Loading interrupt vector high byte", 50, reg)
            cycle()
            reg["reg_pch"] = memory[nonmaskable_interupt_vector_high]
            print()

        case 0x01:
            # ORA (zp, x): 5 cycles
            print(f"---ORA (zp, x) Instruction at address {hex(address)}---")

            # Fetch instruction: 1 cycle
            print_registers("1. Fetching instruction ORA", 50, reg)
            cycle()
            reg = inc_pc(reg)

            # Fetch operand indir low byte: 1 cycle
            print_registers("2. Fetching operand indir low byte", 50, reg)
            cycle()
            reg["reg_indirl"] = memory[add(reg["reg_pcl"], reg["reg_x"])]
            reg = inc_pc(reg)

            # Fetch real address low byte: 1 cycle
            print_registers("3. Fetching real address low byte", 50, reg)
            cycle()
            reg["reg_dirl"] = memory[reg["reg_indirl"]]

            # Fetch real address high byte: 1 cycle
            print_registers("4. Fetching real address high byte", 50, reg)
            cycle()
            reg["reg_dirh"] = memory[add(reg["reg_indirl"], 0x01)]

            # Execute instruction: 1 cycle
            print_registers("5. Executing instruction", 50, reg)
            cycle()
            reg["reg_a"] |= memory[reg["reg_dirh"]] << 8 | memory[reg["reg_dirl"]]

        case 0x04:
            # TSB zp: 4 cycles
            print(f"---TSB zp Instruction at address {hex(address)}---")

            # Fetch instruction: 1 cycle
            print_registers("1. Fetching instruction TSB", 50, reg)
            cycle()
            reg = inc_pc(reg)

            # Fetch operand: 1 cycle
            print_registers("2. Fetching operand", 50, reg)
            cycle()
            reg["reg_dirl"] = memory[reg["reg_pcl"]]
            reg = inc_pc(reg)

            # Execute instruction: 1 cycle
            print_registers("3. Executing instruction", 50, reg)
            cycle()
            reg["reg_data"] |= memory[reg["reg_dirl"]]

            # Store data: 1 cycle
            print_registers("4. Storing result", 50, reg)
            cycle()
            memory[reg["reg_dirl"]] = reg["reg_data"]

        case 0x05:
            # ORA zp: ? cycles
            print(f"---ORA zp Instruction at address {hex(address)}---")
            pass
        case 0x06:
            # ASL zp: ? cycles
            print(f"---ASL zp Instruction at address {hex(address)}---")
            pass
        case 0x07:
            # RMB0 zp: ? cycles
            print(f"---RMB0 zp Instruction at address {hex(address)}---")
            pass
        case 0x08:
            # PHP s: ? cycles
            print(f"---PHP s Instruction at address {hex(address)}---")
            pass
        case 0x09:
            # ORA #: ? cycles
            print(f"---ORA # Instruction at address {hex(address)}---")
            pass
        case 0x0A:
            # ASL A: ? cycles
            print(f"---ASL A Instruction at address {hex(address)}---")
            pass
        case 0x0C:
            # TSB a: ? cycles
            print(f"---TSB a Instruction at address {hex(address)}---")
            pass
        case 0x0D:
            # ORA a: ? cycles
            print(f"---ORA a Instruction at address {hex(address)}---")
            pass
        case 0x0E:
            # ASL a: ? cycles
            print(f"---ASL a Instruction at address {hex(address)}---")
            pass
        case 0x0F:
            # BBR0 r: ? cycles
            print(f"---BBR0 r Instruction at address {hex(address)}---")
            pass
        case 0x10:
            # BPL r: ? cycles
            print(f"---BPL r Instruction at address {hex(address)}---")
            pass
        case 0x11:
            # ORA (zp), y: ? cycles
            print(f"---ORA (zp), y Instruction at address {hex(address)}---")
            pass
        case 0x12:
            # ORA (zp): ? cycles
            print(f"---ORA (zp) Instruction at address {hex(address)}---")
            pass
        case 0x14:
            # TRB zp: ? cycles
            print(f"---TRB zp Instruction at address {hex(address)}---")
            pass
        case 0x15:
            # ORA zp, x: ? cycles
            print(f"---ORA zp, x Instruction at address {hex(address)}---")
            pass
        case 0x16:
            # ASL zp, x: ? cycles
            print(f"---ASL zp, x Instruction at address {hex(address)}---")
            pass
        case 0x17:
            # RMB1 zp: ? cycles
            print(f"---RMB1 zp Instruction at address {hex(address)}---")
            pass
        case 0x18:
            # CLC i: ? cycles
            print(f"---CLC i Instruction at address {hex(address)}---")
            pass
        case 0x19:
            # ORA a, y: ? cycles
            print(f"---ORA a, y Instruction at address {hex(address)}---")
            pass
        case 0x1A:
            # INC A: ? cycles
            print(f"---INC A Instruction at address {hex(address)}---")
            pass
        case 0x1C:
            # TRB a: ? cycles
            print(f"---TRB a Instruction at address {hex(address)}---")
            pass
        case 0x1D:
            # ORA a, x: ? cycles
            print(f"---ORA a, x Instruction at address {hex(address)}---")
            pass
        case 0x1E:
            # ASL a, x: ? cycles
            print(f"---ASL a, x Instruction at address {hex(address)}---")
            pass
        case 0x1F:
            # BBR1 r: ? cycles
            print(f"---BBR1 r Instruction at address {hex(address)}---")
            pass
        case 0x20:
            # JSR a: ? cycles
            print(f"---JSR a Instruction at address {hex(address)}---")
            pass
        case 0x21:
            # AND (zp, x): ? cycles
            print(f"---AND (zp, x) Instruction at address {hex(address)}---")
            pass
        case 0x24:
            # BIT zp: ? cycles
            print(f"---BIT zp Instruction at address {hex(address)}---")
            pass
        case 0x25:
            # AND zp: ? cycles
            print(f"---AND zp Instruction at address {hex(address)}---")
            pass
        case 0x26:
            # ROL zp: ? cycles
            print(f"---ROL zp Instruction at address {hex(address)}---")
            pass
        case 0x27:
            # RMB2 zp: ? cycles
            print(f"---RMB2 zp Instruction at address {hex(address)}---")
            pass
        case 0x28:
            # PLP s: ? cycles
            print(f"---PLP s Instruction at address {hex(address)}---")
            pass
        case 0x29:
            # AND #: ? cycles
            print(f"---AND # Instruction at address {hex(address)}---")
            pass
        case 0x2A:
            # ROL A: ? cycles
            print(f"---ROL A Instruction at address {hex(address)}---")
            pass
        case 0x2C:
            # BIT a: ? cycles
            print(f"---BIT a Instruction at address {hex(address)}---")
            pass
        case 0x2D:
            # AND a: ? cycles
            print(f"---AND a Instruction at address {hex(address)}---")
            pass
        case 0x2E:
            # ROL a: ? cycles
            print(f"---ROL a Instruction at address {hex(address)}---")
            pass
        case 0x2F:
            # BBR2 r: ? cycles
            print(f"---BBR2 r Instruction at address {hex(address)}---")
            pass
        case 0x30:
            # BMI r: ? cycles
            print(f"---BMI r Instruction at address {hex(address)}---")
            pass
        case 0x31:
            # AND (zp), y: ? cycles
            print(f"---AND (zp), y Instruction at address {hex(address)}---")
            pass
        case 0x32:
            # AND (zp): ? cycles
            print(f"---AND (zp) Instruction at address {hex(address)}---")
            pass
        case 0x34:
            # BIT zp, x: ? cycles
            print(f"---BIT zp, x Instruction at address {hex(address)}---")
            pass
        case 0x35:
            # AND zp, x: ? cycles
            print(f"---AND zp, x Instruction at address {hex(address)}---")
            pass
        case 0x36:
            # ROL zp, x: ? cycles
            print(f"---ROL zp, x Instruction at address {hex(address)}---")
            pass
        case 0x37:
            # RMB3 zp: ? cycles
            print(f"---RMB3 zp Instruction at address {hex(address)}---")
            pass
        case 0x38:
            # SEC i: ? cycles
            print(f"---SEC i Instruction at address {hex(address)}---")
            pass
        case 0x39:
            # AND a, y: ? cycles
            print(f"---AND a, y Instruction at address {hex(address)}---")
            pass
        case 0x3A:
            # DEC A: ? cycles
            print(f"---DEC A Instruction at address {hex(address)}---")
            pass
        case 0x3C:
            # BIT a, x: ? cycles
            print(f"---BIT a, x Instruction at address {hex(address)}---")
            pass
        case 0x3D:
            # AND a, x: ? cycles
            print(f"---AND a, x Instruction at address {hex(address)}---")
            pass
        case 0x3E:
            # ROL a, x: ? cycles
            print(f"---ROL a, x Instruction at address {hex(address)}---")
            pass
        case 0x3F:
            # BBR3 r: ? cycles
            print(f"---BBR3 r Instruction at address {hex(address)}---")
            pass
        case 0x40:
            # RTI s: ? cycles
            print(f"---RTI s Instruction at address {hex(address)}---")
            pass
        case 0x41:
            # EOR (zp, x): ? cycles
            print(f"---EOR (zp, x) Instruction at address {hex(address)}---")
            pass
        case 0x45:
            # EOR zp: ? cycles
            print(f"---EOR zp Instruction at address {hex(address)}---")
            pass
        case 0x46:
            # LSR zp: ? cycles
            print(f"---LSR zp Instruction at address {hex(address)}---")
            pass
        case 0x47:
            # RMB4 zp: ? cycles
            print(f"---RMB4 zp Instruction at address {hex(address)}---")
            pass
        case 0x48:
            # PHA s: ? cycles
            print(f"---PHA s Instruction at address {hex(address)}---")
            pass
        case 0x49:
            # EOR #: ? cycles
            print(f"---EOR # Instruction at address {hex(address)}---")
            pass
        case 0x4A:
            # LSR A: ? cycles
            print(f"---LSR A Instruction at address {hex(address)}---")
            pass
        case 0x4C:
            # JMP a: ? cycles
            print(f"---JMP a Instruction at address {hex(address)}---")
            pass
        case 0x4D:
            # EOR a: ? cycles
            print(f"---EOR a Instruction at address {hex(address)}---")
            pass
        case 0x4E:
            # LSR a: ? cycles
            print(f"---LSR a Instruction at address {hex(address)}---")
            pass
        case 0x4F:
            # BBR4 r: ? cycles
            print(f"---BBR4 r Instruction at address {hex(address)}---")
            pass
        case 0x50:
            # BVC r: ? cycles
            print(f"---BVC r Instruction at address {hex(address)}---")
            pass
        case 0x51:
            # EOR (zp), y: ? cycles
            print(f"---EOR (zp), y Instruction at address {hex(address)}---")
            pass
        case 0x52:
            # EOR (zp): ? cycles
            print(f"---EOR (zp) Instruction at address {hex(address)}---")
            pass
        case 0x55:
            # EOR zp, x: ? cycles
            print(f"---EOR zp, x Instruction at address {hex(address)}---")
            pass
        case 0x56:
            # LSR zp, x: ? cycles
            print(f"---LSR zp, x Instruction at address {hex(address)}---")
            pass
        case 0x57:
            # RMB5 zp: ? cycles
            print(f"---RMB5 zp Instruction at address {hex(address)}---")
            pass
        case 0x58:
            # CLI i: ? cycles
            print(f"---CLI i Instruction at address {hex(address)}---")
            pass
        case 0x59:
            # EOR a, y: ? cycles
            print(f"---EOR a, y Instruction at address {hex(address)}---")
            pass
        case 0x5A:
            # PHY s: ? cycles
            print(f"---PHY s Instruction at address {hex(address)}---")
            pass
        case 0x5D:
            # EOR a, x: ? cycles
            print(f"---EOR a, x Instruction at address {hex(address)}---")
            pass
        case 0x5E:
            # LSR a, x: ? cycles
            print(f"---LSR a, x Instruction at address {hex(address)}---")
            pass
        case 0x5F:
            # BBR5 r: ? cycles
            print(f"---BBR5 r Instruction at address {hex(address)}---")
            pass
        case 0x60:
            # RTS s: ? cycles
            print(f"---RTS s Instruction at address {hex(address)}---")
            pass
        case 0x61:
            # ADC (zp, x): ? cycles
            print(f"---ADC (zp, x) Instruction at address {hex(address)}---")
            pass
        case 0x64:
            # STZ zp: ? cycles
            print(f"---STZ zp Instruction at address {hex(address)}---")
            pass
        case 0x65:
            # ADC zp: ? cycles
            print(f"---ADC zp Instruction at address {hex(address)}---")
            pass
        case 0x66:
            # ROR zp: ? cycles
            print(f"---ROR zp Instruction at address {hex(address)}---")
            pass
        case 0x67:
            # RMB6 zp: ? cycles
            print(f"---RMB6 zp Instruction at address {hex(address)}---")
            pass
        case 0x68:
            # PLA s: ? cycles
            print(f"---PLA s Instruction at address {hex(address)}---")
            pass
        case 0x69:
            # ADC #: ? cycles
            print(f"---ADC # Instruction at address {hex(address)}---")
            pass
        case 0x6A:
            # ROR A: ? cycles
            print(f"---ROR A Instruction at address {hex(address)}---")
            pass
        case 0x6C:
            # JMP (a): ? cycles
            print(f"---JMP (a) Instruction at address {hex(address)}---")
            pass
        case 0x6D:
            # ADC a: ? cycles
            print(f"---ADC a Instruction at address {hex(address)}---")
            pass
        case 0x6E:
            # ROR a: ? cycles
            print(f"---ROR a Instruction at address {hex(address)}---")
            pass
        case 0x6F:
            # BBR6 r: ? cycles
            print(f"---BBR6 r Instruction at address {hex(address)}---")
            pass
        case 0x70:
            # BVS r: ? cycles
            print(f"---BVS r Instruction at address {hex(address)}---")
            pass
        case 0x71:
            # ADC (zp), y: ? cycles
            print(f"---ADC (zp), y Instruction at address {hex(address)}---")
            pass
        case 0x72:
            # ADC (zp): ? cycles
            print(f"---ADC (zp) Instruction at address {hex(address)}---")
            pass
        case 0x74:
            # STZ zp, x: ? cycles
            print(f"---STZ zp, x Instruction at address {hex(address)}---")
            pass
        case 0x75:
            # ADC zp, x: ? cycles
            print(f"---ADC zp, x Instruction at address {hex(address)}---")
            pass
        case 0x76:
            # ROR zp, x: ? cycles
            print(f"---ROR zp, x Instruction at address {hex(address)}---")
            pass
        case 0x77:
            # RMB7 zp: ? cycles
            print(f"---RMB7 zp Instruction at address {hex(address)}---")
            pass
        case 0x78:
            # SEI i: ? cycles
            print(f"---SEI i Instruction at address {hex(address)}---")
            pass
        case 0x79:
            # ADC a, y: ? cycles
            print(f"---ADC a, y Instruction at address {hex(address)}---")
            pass
        case 0x7A:
            # PLY s: ? cycles
            print(f"---PLY s Instruction at address {hex(address)}---")
            pass
        case 0x7C:
            # JMP (a, x): ? cycles
            print(f"---JMP (a, x) Instruction at address {hex(address)}---")
            pass
        case 0x7D:
            # ADC a, x: ? cycles
            print(f"---ADC a, x Instruction at address {hex(address)}---")
            pass
        case 0x7E:
            # ROR a, x: ? cycles
            print(f"---ROR a, x Instruction at address {hex(address)}---")
            pass
        case 0x7F:
            # BBR7 r: ? cycles
            print(f"---BBR7 r Instruction at address {hex(address)}---")
            pass
        case 0x80:
            # BRA r: ? cycles
            print(f"---BRA r Instruction at address {hex(address)}---")
            pass
        case 0x81:
            # STA (zp, x): ? cycles
            print(f"---STA (zp, x) Instruction at address {hex(address)}---")
            pass
        case 0x84:
            # STY zp: ? cycles
            print(f"---STY zp Instruction at address {hex(address)}---")
            pass
        case 0x85:
            # STA zp: ? cycles
            print(f"---STA zp Instruction at address {hex(address)}---")
            pass
        case 0x86:
            # STX zp: ? cycles
            print(f"---STX zp Instruction at address {hex(address)}---")
            pass
        case 0x87:
            # SMB0 zp: ? cycles
            print(f"---SMB0 zp Instruction at address {hex(address)}---")
            pass
        case 0x88:
            # DEY i: ? cycles
            print(f"---DEY i Instruction at address {hex(address)}---")
            pass
        case 0x89:
            # BIT #: ? cycles
            print(f"---BIT # Instruction at address {hex(address)}---")
            pass
        case 0x8A:
            # TXA i: ? cycles
            print(f"---TXA i Instruction at address {hex(address)}---")
            pass
        case 0x8C:
            # STY a: ? cycles
            print(f"---STY a Instruction at address {hex(address)}---")
            pass
        case 0x8D:
            # STA a: ? cycles
            print(f"---STA a Instruction at address {hex(address)}---")
            pass
        case 0x8E:
            # STX a: ? cycles
            print(f"---STX a Instruction at address {hex(address)}---")
            pass
        case 0x8F:
            # BBS0 r: ? cycles
            print(f"---BBS0 r Instruction at address {hex(address)}---")
            pass
        case 0x90:
            # BCC r: ? cycles
            print(f"---BCC r Instruction at address {hex(address)}---")
            pass
        case 0x91:
            # STA (zp), y: ? cycles
            print(f"---STA (zp), y Instruction at address {hex(address)}---")
            pass
        case 0x92:
            # STA (zp): ? cycles
            print(f"---STA (zp) Instruction at address {hex(address)}---")
            pass
        case 0x94:
            # STY zp, x: ? cycles
            print(f"---STY zp, x Instruction at address {hex(address)}---")
            pass
        case 0x95:
            # STA zp, x: ? cycles
            print(f"---STA zp, x Instruction at address {hex(address)}---")
            pass
        case 0x96:
            # STX zp, y: ? cycles
            print(f"---STX zp, y Instruction at address {hex(address)}---")
            pass
        case 0x97:
            # SMB1 zp: ? cycles
            print(f"---SMB1 zp Instruction at address {hex(address)}---")
            pass
        case 0x98:
            # TYA i: ? cycles
            print(f"---TYA i Instruction at address {hex(address)}---")
            pass
        case 0x99:
            # STA a, y: ? cycles
            print(f"---STA a, y Instruction at address {hex(address)}---")
            pass
        case 0x9A:
            # TXS i: ? cycles
            print(f"---TXS i Instruction at address {hex(address)}---")
            pass
        case 0x9C:
            # STZ a: ? cycles
            print(f"---STZ a Instruction at address {hex(address)}---")
            pass
        case 0x9D:
            # STA a, x: ? cycles
            print(f"---STA a, x Instruction at address {hex(address)}---")
            pass
        case 0x9E:
            # STZ a, x: ? cycles
            print(f"---STZ a, x Instruction at address {hex(address)}---")
            pass
        case 0x9F:
            # BBS1 r: ? cycles
            print(f"---BBS1 r Instruction at address {hex(address)}---")
            pass
        case 0xA0:
            # LDY #: ? cycles
            print(f"---LDY # Instruction at address {hex(address)}---")
            pass
        case 0xA1:
            # LDA (zp, x): ? cycles
            print(f"---LDA (zp, x) Instruction at address {hex(address)}---")
            pass
        case 0xA2:
            # LDX #: ? cycles
            print(f"---LDX # Instruction at address {hex(address)}---")
            pass
        case 0xA4:
            # LDY zp: ? cycles
            print(f"---LDY zp Instruction at address {hex(address)}---")
            pass
        case 0xA5:
            # LDA zp: ? cycles
            print(f"---LDA zp Instruction at address {hex(address)}---")
            pass
        case 0xA6:
            # LDX zp: ? cycles
            print(f"---LDX zp Instruction at address {hex(address)}---")
            pass
        case 0xA7:
            # SMB2 zp: ? cycles
            print(f"---SMB2 zp Instruction at address {hex(address)}---")
            pass
        case 0xA8:
            # TAY i: ? cycles
            print(f"---TAY i Instruction at address {hex(address)}---")
            pass
        case 0xA9:
            # LDA #: ? cycles
            print(f"---LDA # Instruction at address {hex(address)}---")
            pass
        case 0xAA:
            # TAX i: ? cycles
            print(f"---TAX i Instruction at address {hex(address)}---")
            pass
        case 0xAC:
            # LDY a: ? cycles
            print(f"---LDY a Instruction at address {hex(address)}---")
            pass
        case 0xAD:
            # LDA a: ? cycles
            print(f"---LDA a Instruction at address {hex(address)}---")
            pass
        case 0xAE:
            # LDX a: ? cycles
            print(f"---LDX a Instruction at address {hex(address)}---")
            pass
        case 0xAF:
            # BBS2 r: ? cycles
            print(f"---BBS2 r Instruction at address {hex(address)}---")
            pass
        case 0xB0:
            # BCS r: ? cycles
            print(f"---BCS r Instruction at address {hex(address)}---")
            pass
        case 0xB1:
            # LDA (zp), y: ? cycles
            print(f"---LDA (zp), y Instruction at address {hex(address)}---")
            pass
        case 0xB2:
            # LDA (zp): ? cycles
            print(f"---LDA (zp) Instruction at address {hex(address)}---")
            pass
        case 0xB4:
            # LDY zp, x: ? cycles
            print(f"---LDY zp, x Instruction at address {hex(address)}---")
            pass
        case 0xB5:
            # LDA zp, x: ? cycles
            print(f"---LDA zp, x Instruction at address {hex(address)}---")
            pass
        case 0xB6:
            # LDX zp, y: ? cycles
            print(f"---LDX zp, y Instruction at address {hex(address)}---")
            pass
        case 0xB7:
            # SMB3 zp: ? cycles
            print(f"---SMB3 zp Instruction at address {hex(address)}---")
            pass
        case 0xB8:
            # CLV i: ? cycles
            print(f"---CLV i Instruction at address {hex(address)}---")
            pass
        case 0xB9:
            # LDA a, y: ? cycles
            print(f"---LDA a, y Instruction at address {hex(address)}---")
            pass
        case 0xBA:
            # TSX i: ? cycles
            print(f"---TSX i Instruction at address {hex(address)}---")
            pass
        case 0xBC:
            # LDY a, x: ? cycles
            print(f"---LDY a, x Instruction at address {hex(address)}---")
            pass
        case 0xBD:
            # LDA a, x: ? cycles
            print(f"---LDA a, x Instruction at address {hex(address)}---")
            pass
        case 0xBE:
            # LDX a, y: ? cycles
            print(f"---LDX a, y Instruction at address {hex(address)}---")
            pass
        case 0xBF:
            # BBS3 r: ? cycles
            print(f"---BBS3 r Instruction at address {hex(address)}---")
            pass
        case 0xC0:
            # CPY #: ? cycles
            print(f"---CPY # Instruction at address {hex(address)}---")
            pass
        case 0xC1:
            # CMP (zp, x): ? cycles
            print(f"---CMP (zp, x) Instruction at address {hex(address)}---")
            pass
        case 0xC4:
            # CPY zp: ? cycles
            print(f"---CPY zp Instruction at address {hex(address)}---")
            pass
        case 0xC5:
            # CMP zp: ? cycles
            print(f"---CMP zp Instruction at address {hex(address)}---")
            pass
        case 0xC6:
            # DEC zp: ? cycles
            print(f"---DEC zp Instruction at address {hex(address)}---")
            pass
        case 0xC7:
            # SMB4 zp: ? cycles
            print(f"---SMB4 zp Instruction at address {hex(address)}---")
            pass
        case 0xC8:
            # INY i: ? cycles
            print(f"---INY i Instruction at address {hex(address)}---")
            pass
        case 0xC9:
            # CMP #: ? cycles
            print(f"---CMP # Instruction at address {hex(address)}---")
            pass
        case 0xCA:
            # DEX i: ? cycles
            print(f"---DEX i Instruction at address {hex(address)}---")
            pass
        case 0xCB:
            # WAI i: ? cycles
            print(f"---WAI i Instruction at address {hex(address)}---")
            pass
        case 0xCC:
            # CPY a: ? cycles
            print(f"---CPY a Instruction at address {hex(address)}---")
            pass
        case 0xCD:
            # CMP a: ? cycles
            print(f"---CMP a Instruction at address {hex(address)}---")
            pass
        case 0xCE:
            # DEC a: ? cycles
            print(f"---DEC a Instruction at address {hex(address)}---")
            pass
        case 0xCF:
            # BBS4 r: ? cycles
            print(f"---BBS4 r Instruction at address {hex(address)}---")
            pass
        case 0xD0:
            # BNE r: ? cycles
            print(f"---BNE r Instruction at address {hex(address)}---")
            pass
        case 0xD1:
            # CMP (zp), y: ? cycles
            print(f"---CMP (zp), y Instruction at address {hex(address)}---")
            pass
        case 0xD2:
            # CMP (zp): ? cycles
            print(f"---CMP (zp) Instruction at address {hex(address)}---")
            pass
        case 0xD5:
            # CMP zp, x: ? cycles
            print(f"---CMP zp, x Instruction at address {hex(address)}---")
            pass
        case 0xD6:
            # DEC zp, x: ? cycles
            print(f"---DEC zp, x Instruction at address {hex(address)}---")
            pass
        case 0xD7:
            # SMB5 zp: ? cycles
            print(f"---SMB5 zp Instruction at address {hex(address)}---")
            pass
        case 0xD8:
            # CLD i: ? cycles
            print(f"---CLD i Instruction at address {hex(address)}---")
            pass
        case 0xD9:
            # CMP a, y: ? cycles
            print(f"---CMP a, y Instruction at address {hex(address)}---")
            pass
        case 0xDA:
            # PHX s: ? cycles
            print(f"---PHX s Instruction at address {hex(address)}---")
            pass
        case 0xDB:
            # STP i: ? cycles
            print(f"---STP i Instruction at address {hex(address)}---")
            pass
        case 0xDD:
            # CMP a, x: ? cycles
            print(f"---CMP a, x Instruction at address {hex(address)}---")
            pass
        case 0xDE:
            # DEC a, x: ? cycles
            print(f"---DEC a, x Instruction at address {hex(address)}---")
            pass
        case 0xDF:
            # BBS5 r: ? cycles
            print(f"---BBS5 r Instruction at address {hex(address)}---")
            pass
        case 0xE0:
            # CPX #: ? cycles
            print(f"---CPX # Instruction at address {hex(address)}---")
            pass
        case 0xE1:
            # SBC (zp, x): ? cycles
            print(f"---SBC (zp, x) Instruction at address {hex(address)}---")
            pass
        case 0xE4:
            # CPX zp: ? cycles
            print(f"---CPX zp Instruction at address {hex(address)}---")
            pass
        case 0xE5:
            # SBC zp: ? cycles
            print(f"---SBC zp Instruction at address {hex(address)}---")
            pass
        case 0xE6:
            # INC zp: ? cycles
            print(f"---INC zp Instruction at address {hex(address)}---")
            pass
        case 0xE7:
            # SMB6 zp: ? cycles
            print(f"---SMB6 zp Instruction at address {hex(address)}---")
            pass
        case 0xE8:
            # INX i: ? cycles
            print(f"---INX i Instruction at address {hex(address)}---")
            pass
        case 0xE9:
            # SBC #: ? cycles
            print(f"---SBC # Instruction at address {hex(address)}---")
            pass
        case 0xEA:
            # NOP i: ? cycles
            print(f"---NOP i Instruction at address {hex(address)}---")
            pass
        case 0xEC:
            # CPX a: ? cycles
            print(f"---CPX a Instruction at address {hex(address)}---")
            pass
        case 0xED:
            # SBC a: ? cycles
            print(f"---SBC a Instruction at address {hex(address)}---")
            pass
        case 0xEE:
            # INC a: ? cycles
            print(f"---INC a Instruction at address {hex(address)}---")
            pass
        case 0xEF:
            # BBS6 r: ? cycles
            print(f"---BBS6 r Instruction at address {hex(address)}---")
            pass
        case 0xF0:
            # BEQ r: ? cycles
            print(f"---BEQ r Instruction at address {hex(address)}---")
            pass
        case 0xF1:
            # SBC (zp), y: ? cycles
            print(f"---SBC (zp), y Instruction at address {hex(address)}---")
            pass
        case 0xF2:
            # SBC (zp): ? cycles
            print(f"---SBC (zp) Instruction at address {hex(address)}---")
            pass
        case 0xF5:
            # SBC zp, x: ? cycles
            print(f"---SBC zp, x Instruction at address {hex(address)}---")
            pass
        case 0xF6:
            # INC zp, x: ? cycles
            print(f"---INC zp, x Instruction at address {hex(address)}---")
            pass
        case 0xF7:
            # SMB7 zp: ? cycles
            print(f"---SMB7 zp Instruction at address {hex(address)}---")
            pass
        case 0xF8:
            # SED i: ? cycles
            print(f"---SED i Instruction at address {hex(address)}---")
            pass
        case 0xF9:
            # SBC a, y: ? cycles
            print(f"---SBC a, y Instruction at address {hex(address)}---")
            pass
        case 0xFA:
            # PLX s: ? cycles
            print(f"---PLX s Instruction at address {hex(address)}---")
            pass
        case 0xFD:
            # SBC a, x: ? cycles
            print(f"---SBC a, x Instruction at address {hex(address)}---")
            pass
        case 0xFE:
            # INC a, x: ? cycles
            print(f"---INC a, x Instruction at address {hex(address)}---")
            pass
        case 0xFF:
            # BBS7 r: ? cycles
            print(f"---BBS7 r Instruction at address {hex(address)}---")
            pass



    # Fetch next instruction
    address = (reg["reg_pch"] << 8) | reg["reg_pcl"]
