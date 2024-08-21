import tqdm
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd
import torch
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='train/saved_300')
    parser.add_argument('--destination', type=str, default='sataayu/molt5-augmented-default-300-base-smiles2caption')
    args = parser.parse_args()

    tokenizer = T5Tokenizer.from_pretrained(args.model_name)
    model = T5ForConditionalGeneration.from_pretrained(args.model_name)
    model.push_to_hub(args.destination)
    tokenizer.push_to_hub(args.destination)