import pandas as pd
import csv

def main():

    # Path to rewritings 1, 2 and output file

    path_1 = '/rewritings_openai/rewritten_train.txt'
    path_output = '/data/augmented_chebi/train.csv'

    rewritings = pd.read_csv(path_1, sep='\t')
    # Split these 3 captions into different rows, i.e. one SIMES -> 3 captions, so 3 different training samples
    data = rewritings.drop(columns=['CAPTION'])
    print(type(data))

    with open(path_output, 'a',newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for index, row in data.iterrows():
            writer.writerow(row)
        
print("writing is done")

if __name__ == '__main__':
    main()