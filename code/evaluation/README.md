## Text2mol Evaluation Steps

### Installation

The requirement for evaluation code is as follows:

```
python -m spacy download en_core_web_sm
pip install git+https://github.com/samoturk/mol2vec
```

### Downloads

* [test_outputfinal_weights.320.pt](https://uofi.box.com/s/es16alnhzfy1hpagf55fu48k49f8n29x) should be placed in "evaluation/t2m_output". It can be downloaded using `curl -L  https://uofi.box.com/shared/static/es16alnhzfy1hpagf55fu48k49f8n29x --output test_outputfinal_weights.320.pt`

### Evaluation Commends

```
python text_text2mol_metric.py --input_file generative_file.txt
```
