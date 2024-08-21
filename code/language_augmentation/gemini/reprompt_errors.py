import vertexai
import asyncio
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.preview import generative_models
from chebi_prompt_template import chebi_template
from tqdm import tqdm
from config.system_config import SYSTEM_CONFIG
from message_service import prompt_and_write

# TODO(developer): Vertex AI SDK - uncomment below & run in terminal
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login


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
    with open('gemini/error_log.txt', 'r') as file:
        for line in file:
            errors.append(line.strip('\n'))

    print('Errors: ')
    print(errors)

    tasks = []
    pbar = tqdm(desc='Waiting for all tasks to complete', total=len(errors))

    # Initialize the Vertex AI client
    vertexai.init(project='fluted-harmony-414308', location='us-central1')
    gemini_pro_model = GenerativeModel("gemini-pro")

    for e in errors:
        cid = e
        i = cids_to_idx[e]
        prompt = chebi_template["S"].format(smiles[i], captions[i])
        t = asyncio.create_task(prompt_and_write(cid, prompt, pbar, gemini_pro_model))
        tasks.append((t, i))

    await asyncio.gather(*[task for task, _ in tasks])    

# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    asyncio.run(main())
