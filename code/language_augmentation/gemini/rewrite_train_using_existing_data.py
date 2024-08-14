
def main():
    target_path = 'result/rewritten_train2.txt'
    source_path = 'data/chebi/train.txt'
    source_dir = 'chebi'

    # Read from source_path
    with open(source_path, 'r', encoding='utf-8') as train_file:
        train_file.readline()
        cids = []
        smiles = []
        captions = []
        while True:
            line=train_file.readline()
            if not line:
                break
            splits = line.split('	')
            cids.append(splits[0])
            smiles.append(splits[1])
            captions.append(splits[2].replace('\n', ''))

    with open(target_path, 'w+', encoding='utf-8') as target_file:
        target_file.write('CID' + '\t' + 'SMILES' + '\t' + 'CAPTION' + '\t' + 'REWRITTEN_CAPTION\n')
        for i in range(len(cids)):
            with open(source_dir + '/{}.txt'.format(cids[i]), 'r', encoding='utf-8') as source_file:
                rewritten_caption = source_file.read()
                if rewritten_caption is None or rewritten_caption == '':
                    print('Error: empty file at ' + cids[i])
                    return
                target_file.write(cids[i] + '	' + smiles[i] + '	' + captions[i] + '	' + rewritten_caption + '\n')
    print('Done')

if __name__ == '__main__':
    main()