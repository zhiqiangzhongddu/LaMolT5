import argparse

from os.path import join
from evaluation import text_translation_metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', type=str, default='predictions/')
    parser.add_argument('--log_fp', type=str, default='molt5-augmented-default-3-large-smiles2caption_eval.txt')
    parser.add_argument('--file_name', type=str, default='molt5-augmented-default-3-large-smiles2caption.txt')
    args = parser.parse_args()

    log_io = open(args.log_fp, 'w+')
    file_path = join('predictions', args.file_name)
    bleu2, bleu4, rouge_1, rouge_2, rouge_l, meteor_score = \
        text_translation_metrics.evaluate(
            'allenai/scibert_scivocab_uncased', file_path, 512
        )
    log_io.write(f'For {args.file_name}\n')
    log_io.write(f'bleu2: {round(bleu2, 3)}\n')
    log_io.write(f'bleu4: {round(bleu4, 3)}\n')
    log_io.write(f'rouge_1: {round(rouge_1, 3)}\n')
    log_io.write(f'rouge_2: {round(rouge_2, 3)}\n')
    log_io.write(f'rouge_l: {round(rouge_l, 3)}\n')
    log_io.write(f'meteor_score: {round(meteor_score, 3)}\n')
    log_io.write('\n')
    log_io.flush()
    log_io.close()
