import sys

# open file
try:
    file_hex = open('hex.txt', 'r')
    file_dcs = open('dcs.txt', 'r')
except IOError:
    print("Failed to open file")
    sys.exit()


def count_ones(binary_list):
    count = 0
    for bit in range(8):
        if binary_list[bit] == '1':
            count += 1
    return count

cur = [[] for _ in range(9)]
temp = [[] for _ in range(9)]
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

def compare(a, b):
    same = 8
    bit_idx = 0
    for i in range(8):
        if a[i] != b[i]:
            same -= 1
            bit_idx = i
    return same, bit_idx




def print_groups(cur):
    for i in range(len(cur)):
        print("Group", i, ":")
        for j in range(len(cur[i])):
            print(''.join(cur[i][j]))
        print()







for loop in range(8):
    
    dup = set()
    for group in range(8 - loop):
        if cur[group] == []: continue

        # Loop through all binary lists in start group
        i = 0
        while i < len(cur[group]):
            found_match = False
            
            # Loop through all binary lists in target group
            j = 0
            while j < len(cur[group+1]):
                # Iterate through all 8 bits
                same, bit_idx = compare(cur[group][i], cur[group+1][j])

                if same == 7:
                    found_match = True
                    match = cur[group][i][:]
                    match[bit_idx] = 'X'
                    match[8] = 'n'
                    count = count_ones(match)
                    match_str = ''.join(match)
                    cur[group+1][j][8] = 'y'
                    # Check if duplicate
                    if match_str in dup: 
                        j += 1
                        continue
                    else: 
                        temp[count].append(match)
                        dup.add(match_str)
                        

                j += 1
                        

            # Add to result if no match
            if not found_match and cur[group][i][8] == 'n':
                res.append(cur[group][i])

            

            i += 1

    cur = temp
    temp = [[] for _ in range(7 - loop)]

    if loop == 0 or loop == 1 or loop==2:
        print("Loop", loop)
        print("-----------------------------------------------------------------")
        print_groups(cur)
    


print(res)




