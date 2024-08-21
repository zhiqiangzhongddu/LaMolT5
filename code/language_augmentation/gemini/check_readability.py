
path = 'result/rewritten_train2.txt'
with open(path, 'r', encoding='utf-8') as file:
    file.readline() # Skip the header
    i = 1
    for line in file.readlines():
        split = line.split('	')
        i += 1
        if len(split) != 4:
            print(str(i) + ':')
            print('Error:', split)
            break
    