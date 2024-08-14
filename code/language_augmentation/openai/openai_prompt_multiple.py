import openai
import time
from tqdm import tqdm

from gemini.chebi_prompt_template import chebi_template


# Set up OpenAI API key
api_key = "[INSERT API KEY HERE]"
openai.api_key = api_key

# Function to send a message to the OpenAI chatbot model and return its response
def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",          # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=8192,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

def prompt_and_write(cid,prompt):
    message_log = []
    # for p in prompts:
        # Send the prompt to the chatbot and get its response
    time.sleep(1)
    message_log.append({"role": "user", "content": prompt})
    response = send_message(message_log)
    with open('openai_result_multiple/{}.txt'.format(cid), 'w+', encoding="utf-8") as file:
        file.write(response)

# Main function that runs the chatbot
def main():
    # Initialize the conversation history with a message from the chatbot
    message_log = [
        {"role": "system", "content": "You are a helpful assistant with a speciality in chemistry."}
    ]

        
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
            captions.append(splits[2])
        file.close()

    prompts = []
    for e in range(1, 22):
        prompts.append(chebi_template["IF"].format(smiles[e], captions[e]));

    for i in tqdm(range(1, 22)):
        prompt_and_write(cids[i], prompts[i])


# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()
