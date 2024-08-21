import asyncio

import vertexai
from vertexai.preview.generative_models import GenerativeModel

from chebi_prompt_template import chebi_template 
from tqdm import tqdm
from gemini.message_service import prompt_and_write

# Main function that runs the chatbot
async def main():
    # Initialize the conversation history with a message from the chatbot
    # Unfortunately, you can not specify the system instructions in Gemini, so you have to add it in your requests, as in `system_config`
    path = '../data/chebi'
    file_names = ['train.txt']

    cids = []
    smiles = []
    captions = []

    for file_name in file_names:
        file_name_path = path + '/' + file_name

        # read from file file_name_path
        file = open(file_name_path, 'r', encoding='utf-8')
        file.readline()
        while True:
            line=file.readline()
            if not line:
                break
            splits = line.split('	')
            cids.append(splits[0])
            smiles.append(splits[1])
            captions.append(splits[2].replace('\n', ''))
        file.close()

    prompts = []

    for e in range(len(smiles)):
        prompts.append(chebi_template["S"].format(smiles[e], captions[e]))
    
    tasks = []
    pbar = tqdm(desc='Waiting for all tasks to complete', total=len(prompts))

    # Initialize the Vertex AI client
    vertexai.init(project='fluted-harmony-414308', location='us-central1')
    gemini_pro_model = GenerativeModel("gemini-pro")

    for i in tqdm(desc='Creating tasks', iterable=range(0, len(prompts))):
        t = asyncio.create_task(prompt_and_write(cids[i], prompts[i], pbar, gemini_pro_model))
        tasks.append((t, i))

    # Wait for all tasks to complete
    await asyncio.gather(*[task for task, _ in tasks])    

# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    asyncio.run(main())
