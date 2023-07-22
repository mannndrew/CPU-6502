import sys
from helper import *

# open file
try:
    file_hex = open('hex.txt', 'r')
    file_dcs = open('dcs.txt', 'r')
except IOError:
    print("Failed to open file")
    sys.exit()

cur = [[] for _ in range(9)]
temp = [[] for _ in range(8)]
res = []

# read hex file
dup = set()
for line in file_hex:
    hex = line.strip()
    # Check if empty
    if hex == '': continue
    # Check if duplicate
    if hex in dup: continue
    else: dup.add(hex)
    binary_val = bin(int(hex, 16))[2:].zfill(8)
    binary_list = [bit for bit in binary_val]  # Split binary string into a list of bits
    binary_list.append('n')
    count = count_ones(binary_list)
    cur[count].append(binary_list)

# read dcs file
dup = set()
for line in file_dcs:
    hex = line.strip()
    # Check if empty
    if hex == '': continue
    # Check if duplicate
    if hex in dup: continue
    else: dup.add(hex)
    binary_val = bin(int(hex, 16))[2:].zfill(8)
    binary_list = [bit for bit in binary_val]  # Split binary string into a list of bits
    binary_list.append('n')
    count = count_ones(binary_list)
    cur[count].append(binary_list)

# close file
file_hex.close()
file_dcs.close()




for loop in range(8):
    
    dup = set()
    for group in range(len(cur)-1):
        if cur[group] == []: continue

        # Loop through all binary lists in start group

        for i in range(len(cur[group])):
            found_match = False
            
            # Loop through all binary lists in target group
            for j in range(len(cur[group+1])):
                # Iterate through all 8 bits
                same, bit_idx = compare(cur[group][i], cur[group+1][j])

                if same == 7:
                    found_match = True
                    cur[group+1][j][8] = 'y'
                    match = cur[group][i][:]
                    match[bit_idx] = 'X'
                    match[8] = 'n'
                    match_str = ''.join(match)
                    
                    # Check if duplicate
                    if match_str in dup: 
                        continue
                    else: 
                        count = count_ones(match)
                        temp[count].append(match)
                        dup.add(match_str)
                        
            # Add to result if no match
            if not found_match and cur[group][i][8] == 'n':
                res.append(cur[group][i])


    cur = temp
    temp = [[] for _ in range(7 - loop)]

    
    print(f"Loop {loop}-----------------------------------------------------------------")
    print(cur)
    


print_res(res)




