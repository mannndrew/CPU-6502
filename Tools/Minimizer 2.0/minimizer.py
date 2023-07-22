import sys

# open file
try:
    file_hex = open('hex.txt', 'r')
    file_space = open('space.txt', 'r')
except IOError:
    print("Failed to open file")
    sys.exit()

dup = set()

cur = []
temp = []
res = []

# read file
for line in file_hex:
    hex = line.strip()
    # Check if empty
    if hex == '': continue
    # Check if duplicate
    if hex in dup: continue
    else: dup.add(hex)
    binary_val = bin(int(hex, 16))[2:].zfill(8)
    binary_list = [bit for bit in binary_val]  # Split binary string into a list of bits
    cur.append([binary_list])

# close file
file_hex.close()
file_space.close()

def compare(a, b):
    same = 8
    bit_idx = 0
    for i in range(8):
        if a[i] != b[i]:
            same -= 1
            bit_idx = i
    return same, bit_idx



print("Start:")
for i in range(len(cur)):
    for j in range(len(cur[i])):
        print(''.join(cur[i][j]))



while cur != [] or temp != []:
    for a in range(len(cur)):
        found_match = False
        matches = []
        dup = set()
        for b in range(len(cur[a])):
            for i in range(len(cur)):
                for j in range(len(cur[i])):
                    # Iterate through all 8 bits
                    same, bit_idx = compare(cur[a][b], cur[i][j])

                    if same == 7:
                        found_match = True
                        match = cur[a][b][:]
                        match[bit_idx] = 'X'
                        match_str = ''.join(match)
                        # Check if duplicate
                        if match_str in dup: 
                            continue
                        else: 
                            dup.add(match_str)
                            matches.append(match)

        # Save matches if found
        if found_match:
            temp.append(matches)

        # Add to result if no match
        else:
            res.append(cur[a])

    cur = temp
    temp = []

dup = set()
final = []


# Iterate over res list
for i in range(len(res)):
    found_dup = False
    for j in range(len(res[i])):
        str = ''.join(res[i][j])
        if str in dup: 
            found_dup = True
            break
    if not found_dup:
        str = ''.join(res[i][0])
        dup.add(str)
        final.append(str)
    








print("Cur:")
for i in range(len(cur)):
    for j in range(len(cur[i])):
        print(''.join(cur[i][j]))
    print()


print("Res:")
for i in range(len(res)):
    for j in range(len(res[i])):
        print(''.join(res[i][j]))
    print()

print("Final:")
print(final)






