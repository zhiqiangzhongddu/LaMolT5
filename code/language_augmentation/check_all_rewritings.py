
# Check that all the rewritings exist and the files are not empty
import os
import time

path = 'chebl'
file_names = os.listdir(path)
cids = []

success = True

with open('data/chembl/train.txt', 'r', encoding='utf-8') as file:
    file.readline() # Skip the header
    cids = [split[0] for split in [line.split('	') for line in file.readlines()]]

for file_name in file_names:
    cid = file_name.split('.')[0]
    if cid in cids:
        with open(path + '/' + file_name, 'r', encoding='utf-8') as file:
            if file.read().strip() == '':
                print('Empty file:', file_name)
    else:
        print('File not found:', file_name)
        with open('error_log.txt', 'a+') as file:
            file.write(cid + '\n')
        success = False

print('Success:', success)

