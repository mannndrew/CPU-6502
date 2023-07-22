def count_ones(binary_list):
    count = 0
    for bit in range(8):
        if binary_list[bit] == '1':
            count += 1
    return count

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
        print(f"Group {i}:")
        for j in range(len(cur[i])):
            print(''.join(cur[i][j]))
        print()

def print_res(res):
    print("--------------------Result--------------------")
    for i in range(len(res)):
        res[i].pop()
        print(''.join(res[i]))