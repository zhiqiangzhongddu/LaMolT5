from tqdm import tqdm
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test_file_path', type=str, default='data/sample.csv')
    parser.add_argument('--output_dir', type=str, default='predictions/')
    parser.add_argument('--output_file_name', type=str, default='sample_predictions_smiles.txt')
    args = parser.parse_args()
    gt = "ground truth"
    baseline = "laituan245/molt5-small-caption2smiles"
    new = "harveybro/molt5-augmented-default-1500-small-caption2smiles"
    model_names = [gt, baseline, new]
    predictions = {}
    smiles = []
    captions = []

    test_df = pd.read_csv(args.test_file_path)
    for model_name in model_names:
        predictions[model_name] = []
        if model_name != gt:
            tokenizer = T5Tokenizer.from_pretrained(model_name, model_max_length=512)
            model = T5ForConditionalGeneration.from_pretrained(model_name)
        for i in tqdm(range(len(test_df))):
            caption = test_df['description'][i]
            if model_name == gt:
                smile = test_df['SMILES'][i]
                smiles.append(smile)
                predictions[model_name].append(smile)
                captions.append(caption)
                continue

            encoding = tokenizer(caption, return_tensors='pt')
            input_ids = encoding.input_ids
            outputs = model.generate(input_ids, num_beams=5, max_length=512)
            smiles = tokenizer.decode(outputs[0], skip_special_tokens=True)
            predictions[model_name].append(smiles)
    print(predictions)
            
    log_io = open(f'{args.output_dir}/{args.output_file_name}', 'w+')
    log_io.write('SMILES & Ground Truth & Molt5-small & LaMolt5-small\n')
    for i in range(len(test_df)):
        print(i)
        print("caption:", captions[i])
        print("gt:", predictions[gt][i])
        print("baseline:", predictions[baseline][i])
        print("new:", predictions[new][i])
        log_io.write(f"{captions[i]} & {predictions[gt][i]} & {predictions[baseline][i]} & {predictions[new][i]}\\\\\n")
    log_io.close()
