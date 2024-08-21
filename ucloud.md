# How to run the training scripts on Ucloud

## Starting a new job on Ucloud

- Include the following 3 folders under `/work`:
    - `/work/tools`: miniconda3 for everyone to use.
    - `/work/LLMaSyn`: a public folder.
    - `/work/{your_name}`: your own folder.

- Connect Ucloud using the command line provided: `ssh ucloud@ssh.cloud.sdu.dk -p xxxx`

## Initialize conda
- Go to your own folder:  `/work/{your_name}`.
- `source /work/tools/miniconda3/bin/activate`
- `conda init`
- check if conda is installed: `conda --version`

## Git clone our repository in your folder
`git clone https://github.com/satansju/Synthetic.git`

## Create a new environment for your project
*Note: conda environment myenv has already created. So please skip this step*
- Go to the folder: `Synthetic/train`
- Create a new environment with the yaml file: `conda env create -f environment.yml`
- Configure accelerate: `accelerate config`
- Log in your huggingface: `huggingface-cli login`

## Run the training scripts
*Note: please configure accelerate and log in huggingface before running the training script.*

- default training script: `bash Synthetic/train/trainer.sh`
- contrastive encoders: `bash Synthetic/contrastive_train/trainer_encoders.sh`
- fine tune decoder: `bash Synthetic/contrastive_train/trainer_decoder.sh`

## Remarks on bash and finetune scripts

The bash script is supposed to automatically and continiously run `finetune.py` for several times according to `epochs` array in `train/trainer.sh`.

If you want to run the training scripts of default molecule captioning and molecule generation, the number of epochs, learning rate, weight_decay, batch_size, grad_accumulation_steps need to be specified in `fine_tune() of finetune.py` first!

**Note: please change the `epochs` array along with the number of epochs specified in `finetune.py`!!** 

For example, if you want to specify the number of epochs as 10:

```python
def fine_tune(path_to_train, path_to_validation, path_to_test, checkpoint_path, path_to_pretrained, output_dir, save_path, huggingface_repo, log_file, batch_size=20, num_epoch=10, learning_rate=5e-5, weight_decay=0.01, grad_accumulation_steps=4):
```
The stride of `epochs` in `train/trainer.sh` has also to be 10:

```bash
current_epoch="0"
epochs=('10' '20' '30')
```
if you start with epoch 0 and want to save and upload the model at epoch 10, 20 and 30.

But if the script crashes, you can just reset `current_epoch` to be the last epoch number before it crashes (we can make sure you will have you model saved locally at `train/saved_{last epoch number before it crashes}`). For example, if the script crashes at 10 and it was saved at `train/saved_10`, you can just set:
```bash
current_epoch="10"
epochs=('20' '30')
```
to restart training.

### path_to_pretrained
`path_to_pretrained` specifies the path to the pretrained model before each execution of `finetune.py` launched by `train/trainer.sh`.

If you want to fine tune the model from scratch (from the original MolT5 models), there are some extra prerequisites before launching the bash script:

Download the original MolT5 model from the huggingface and save and rename it at `train/saved_0`. Then your `path_to_pretrained` in this case should be specified as `path_to_pretrained=train/saved{current_epoch}`, which means that for each execution, we load the previous model from the local folder.

*Note: in bash script `train/trainer.sh`, we also have the snippet to upload the model to huggingface right after one execution of traininig script is done. But since in this case, we load the model locally, so if there is something wrong with uploading script, we are still safe to continue training.*
