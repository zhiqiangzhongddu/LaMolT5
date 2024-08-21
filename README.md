# LaMolT5


# Training
- You need to install all the dependencies from the `requirements.txt`.
- You need to login to the huggingface-cli with a write token and that you have set up the correct paths for the train/finetune.py file either change the default values or give them as arguments. 
- Use the bash script: `bash training/train.sh` from the root directory to train and save intermediate steps on huggingface.
- To load the tensorboard use the following commands:
  - `tensorboard --logdir <LOG_DIR> --port 6006 --bind_all`
  - `ssh -N -f -L localhost:16006:localhost:6006 <USER>@<SERVER>`

# Models
The models for this project can be found at huggingface [here](https://huggingface.co/PATH_TO_REPOSITORY) (update path to new huggingface repo).
For now there are a checkpoint for each 100 epochs.

# Predict
- You can generate predictions with a trained model using the `prediction/predict.py` script.


# Evaluation
- You can evaluate trained models with the two scripts `evaluation/evaluate_caption2smiles.py` and `evaluation/evaluate_smiles2caption` based on predictions generated on the previous step.

# Results
The results from the evaluation step will be saved as a file under the `evalauation` folder.
