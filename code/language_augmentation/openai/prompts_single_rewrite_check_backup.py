import openai
import time
import asyncio
import os
from tqdm import tqdm


from chebi_prompt_template import chebi_template

semaphore = asyncio.Semaphore(1)
# Set up OpenAI API key
api_key = "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"
openai.api_key = api_key

system_config = "You are now a chemical specialist in rewritting captions for a molecule in SMILES format, make sure those captions describe the given molecule correctly and precisely based your two inputs (SMILES and Caption of it).Also make sure your rewritting captions does not include the input SMILES. Write the response without using linebreaks, newlines, or special characters such as '\t' or '\n'."

# Function to send a message to the OpenAI chatbot model and return its response
async def send_message(message_log, cid):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    async with semaphore:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",          # The name of the OpenAI chatbot model to use
                messages=message_log,   # The conversation history up to this point, as a list of dictionaries
                max_tokens=4096,        # The maximum number of tokens (words or subwords) in the generated response
                stop=None,              # The stopping sequence for the generated response, if any (not used here)
                temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
            )
            # Find the first response from the chatbot that has text in it (some responses may not have text)
            for choice in response.choices:
                if "text" in choice and choice.text is not None:
                    return choice.text
            # If no response with text is found, return the first response's content (which may be empty)
            return response.choices[0].message.content
        except Exception as e:
            with open('openai/error_log.txt', 'a+') as file:
                file.write(cid + '\t' + str(e) + '\n')
            with open('openai/error_cids.txt', 'a+') as file:
                file.write(cid + '\n')
        

async def prompt_and_write(cid,prompt, pbar):
    message_log = []
    # Send the prompt to the chatbot and get its response
    # Add system instructions before prompting
    message_log.append({"role": "user", "content": system_config + prompt})
    try:
        response = await send_message(message_log, cid)
    except asyncio.TimeoutError as e:
        with open('openai/error_log.txt', 'a+') as file:
            file.write(cid + '\t' + str(e) + '\n')
        response = None
        pass
    pbar.update(1)

    if response is None:
        return
    
    with open('rewritings_openai/openai_result_single/{}.txt'.format(cid), 'w+', encoding="utf-8") as file:
        file.write(response)


# Main function that runs the chatbot
async def main():
    # Initialize the conversation history with a message from the chatbot
        
    path = 'data/chebi'
    file_names = ['train.txt'] #, 'test.txt', 'validation.txt']

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

    # caculate the number of files generated
    path = 'rewritings_openai/openai_result_single'
    file_names = os.listdir(path)
    num_files = len(file_names)

    prompts = []

    for e in range(len(smiles)):
        prompts.append(chebi_template["S"].format(smiles[e], captions[e]));

    # continue from the last file
    start = num_files
    end = len(prompts)
    tasks = []
    pbar = tqdm(desc='Waiting for all tasks to complete', total=(end-start))

    for i in tqdm(desc='Creating tasks', iterable=range(start, end)):
        # print(i)
        t = asyncio.create_task(asyncio.wait_for(prompt_and_write(cids[i], prompts[i], pbar), timeout=5))
        tasks.append((t,i))

    await asyncio.gather(*[task for task, _ in tasks])

 # Check that all the rewritings exist and the files are not empty       
def prompts_files_check():

    success = True

    path = 'rewritings_openai/openai_result_single'
    file_names = os.listdir(path)
    cids = []
    file_cids = [file_name.split('.')[0] for file_name in file_names]
    not_found = []
    empty = []

    with open('data/chebi/train.txt', 'r', encoding='utf-8') as file:
        file.readline() # Skip the header
        cids = [split[0] for split in [line.split('	') for line in file.readlines()]]
    
    # cids = cids[:1010]   

    print('Checking files')
    for cid in tqdm(cids):
        if cid not in file_cids:
            not_found.append(cid)
            with open('openai/error_cids.txt', 'a+', encoding='utf-8') as file:
                file.write(cid + '\n')
            success = False
        else:
            with open(path + '/' + cid + '.txt', 'r', encoding='utf-8') as file:
                if file.read().strip() == '':
                    with open('openai/error_cids.txt', 'a+', encoding='utf-8') as file:
                        file.write(cid + '\n')
                    empty.append(cid)
                    success = False
            file.close()
    print('Check complete')
    print('Success:', success)
    print('-' * 10)
    print('\nNot found:\n', len(not_found))
    print('-' * 10)
    print('\nEmpty:\n', len(empty))
# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    asyncio.run(main())
    print("All rewriting tasks have been completed!")
    prompts_files_check()
