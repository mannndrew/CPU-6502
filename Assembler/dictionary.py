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

# print values in dictionary
for key, value in instruction_dict.items():
    for key2, value2 in value.items():
        if key2 == 1 or key2 == 3 or key2 == 4:
            print(value2)
    