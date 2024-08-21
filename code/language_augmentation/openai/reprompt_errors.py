import openai
import time
import asyncio
import os
from tqdm import tqdm
from prompts_single_rewrite_check_backup import prompt_and_write

from chebi_prompt_template import chebi_template


# Main function that runs the chatbot
async def main():
    # Initialize the conversation history with a message from the chatbot
    # Unfortunately, you can not specify the system instructions in Gemini, so you have to add it in your requests, as in `system_config`
    path = 'data/chebi'
    file_names = ['train.txt']

    cids = []
    smiles = []
    captions = []
    cids_to_idx = {}

    for file_name in file_names:
        file_name_path = path + '/' + file_name

        # read from file file_name_path
        file = open(file_name_path, 'r', encoding='utf-8')
        file.readline()
        i = 0
        while True:
            line=file.readline()
            if not line:
                break
            splits = line.split('	')
            cids.append(splits[0])
            smiles.append(splits[1])
            captions.append(splits[2].replace('\n', ''))
            cids_to_idx[splits[0]] = i
            i += 1
        file.close()

    errors = []
    with open('openai/error_cids.txt', 'r') as file:
        for line in file:
            errors.append(line.strip('\n'))

    print('Errors: ')
    print(errors)

    tasks = []
    pbar = tqdm(desc='Waiting for all tasks to complete', total=len(errors))

    for e in errors:
        cid = e
        print("CID: ", cid)
        i = cids_to_idx[e]
        print(i, smiles[i], captions[i])
        prompt = chebi_template["S"].format(smiles[i], captions[i])
        t = asyncio.create_task(asyncio.wait_for(prompt_and_write(cid, prompt, pbar), timeout=5))
        tasks.append((t, i))

    await asyncio.gather(*[task for task, _ in tasks])    

# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    asyncio.run(main())
