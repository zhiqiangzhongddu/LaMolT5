import os

from vllm import LLM, SamplingParams

from gemini.chebi_prompt_template import chebi_template

# Set cuda visible devices dependent on the machine running
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "1,2,3,4"

path = './data/chebi/'
file_names = ['train.txt']#, 'test.txt', 'validation.txt']

smiles = []
captions = []

for file_name in file_names: 
    file_name_path = path + file_name
    # read from file file_name_path
    file = open(file_name_path, 'r')
    while True:
        line=file.readline()
        if not line:
            break
        splits = line.split('	')
        smiles.append(splits[1])
        captions.append(splits[2])
    file.close()



# Create a sampling params object.
# There are Sampling parameters for text generation.
# temperature: float = 1.0 that controls the randomness of the sampling.
#       Lower values make the model more deterministic, while higher values make
#       the model more random. Zero means greedy sampling.
# top_p: float = 1.0 that controls the cumulative probability of the top tokens to consider.
#       Must be in (0, 1]. Set to 1 to consider all tokens.
# top_k: int = -1 Integer that controls the number of top tokens to consider.
#       Set to -1 to consider all tokens.
# max_tokens: int = 16 Maximum number of tokens to generate per output sequence.
sampling_params = SamplingParams(
    temperature=0.2,
    top_p=0.9,
    max_tokens=512,
)


# Create an LLM.
# tensor_parallel_size: The number of GPUs to use for distributed execution with tensor parallelism.
# llm = LLM(
#     model="facebook/opt-125m",
#     tensor_parallel_size=os.environ["CUDA_VISIBLE_DEVICES"].count(",")+1,
# )
# Not working well
# llm = LLM(
#     model="mistralai/Mistral-7B-Instruct-v0.1",
#     tensor_parallel_size=2,
#     download_dir='models',
#     dtype='float16'
# )
# Not working well
# llm = LLM(
#     model="meta-llama/Llama-2-7b-chat-hf",
#     tensor_parallel_size=os.environ["CUDA_VISIBLE_DEVICES"].count(",")+1,
#     download_dir='models'
# )
# Not working well
llm = LLM(
    model="meta-llama/Llama-2-13b-chat-hf",
    tensor_parallel_size=os.environ["CUDA_VISIBLE_DEVICES"].count(",")+1,
    download_dir='models',
    dtype='float16'
)
# llm = LLM(
#     model="meta-llama/Llama-2-70b-chat-hf",
#     tensor_parallel_size=os.environ["CUDA_VISIBLE_DEVICES"].count(",")+1,
# )

# Generate texts from the prompts. The output is a list of RequestOutput objects
# that contain the prompt, generated text, and other information.


# Sample prompts.
prompts = [
    chebi_template["IF"].format(smiles[2], captions[2]),
    chebi_template["IF"].format(smiles[3], captions[3]),
    chebi_template["IF"].format(smiles[4], captions[4]),
]


outputs = llm.generate(
    prompts=prompts,
    sampling_params=sampling_params,
)

# Print the outputs.
for idx, output in enumerate(outputs):
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(idx+1)
    print("Prompt:\n%s\nGenerated text:\n%s\n" % (prompt, generated_text))
