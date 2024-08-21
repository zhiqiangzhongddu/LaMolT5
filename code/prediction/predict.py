from tqdm import tqdm
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='sataayu/molt5-augmented-default-1500-base-smiles2caption')
    parser.add_argument('--test_file_path', type=str, default='data/augmented_chebi/test.csv')
    parser.add_argument('--output_dir', type=str, default='predictions/')
    parser.add_argument('--output_file_name', type=str, default='molt5-augmented-default-1500-base-smiles2caption.txt')
    args = parser.parse_args()

    tokenizer = T5Tokenizer.from_pretrained(args.model_name)
    model = T5ForConditionalGeneration.from_pretrained(args.model_name)
    test_df = pd.read_csv(args.test_file_path)

    log_io = open(f'{args.output_dir}/{args.output_file_name}', 'w+')
    log_io.write('SMILES	ground truth	output\n')
    print(f"Model Name:{args.model_name}")
  
    for i in tqdm(range(len(test_df))):
        smiles_enc = tokenizer.encode(test_df['SMILES'][i], return_tensors="pt", padding='max_length', truncation=True, max_length=512)
        output_ids = model.generate(smiles_enc, max_length = 512)
        captions_dec = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        log_io.write(f"{test_df['SMILES'][i]}\t{test_df['CAPTION'][i]}\t{captions_dec}\n")
    log_io.close()
