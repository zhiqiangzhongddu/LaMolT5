# Synthetic
Data synthesization as a part of data augmentation for improving Graph Machine Learning
Work in progress for master thesis @ Aarhus University

# Training
- You need to install all the dependencies from the `requirements.txt`.
- You need to login to the huggingface-cli with a write token and that you have set up the correct paths for the train/finetune.py file either change the default values or give them as arguments. 
- Use the bash script: `bash training/train.sh` from the root directory to train and save intermediate steps on huggingface.
- To load the tensorboard use the following commands:
  - `tensorboard --logdir <LOG_DIR> --port 6006 --bind_all`
  - `ssh -N -f -L localhost:16006:localhost:6006 <USER>@<SERVER>`

# Models
The models for this project can be found at huggingface [here](https://huggingface.co/sataayu).
For now there are a checkpoint for each 100 epochs.

# Results
Todo ...
