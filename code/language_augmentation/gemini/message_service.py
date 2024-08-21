from config.system_config import SYSTEM_CONFIG
from vertexai.preview import generative_models

# Function to send a message to Gemini pro and return its response
async def send_message(message_log, cid, gemini_pro_model):
    # Safety config
    safety_config = {
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    }

    # Generation config
    config = {"max_output_tokens": 8192, "temperature": 0.7, "top_p": 1, "top_k": 32}
    try:
        response = gemini_pro_model.generate_content(
            message_log,
            generation_config=config,
            safety_settings=safety_config
        )
        # Find the first response from the chatbot that has text in it (some responses may not have text)
        for choice in response.candidates:
            if choice.text != None:
                return choice.text
        # If no response with text is found, return the first response's content (which may be empty)

        return response.candidates[0].content
    except Exception as e:
        with open('gemini/error_log.txt', 'a+') as file:
            file.write(cid + '\n')
        with open('gemini/error_responses.txt', 'a+') as file:
            file.write(str(e) + '\n')


async def prompt_and_write(cid, prompt, pbar, gemini_pro_model):
    # Send the prompt to the chatbot and get its response
    # Add system instructions before prompting
    message_log = [{"role": "user", "parts" : [{"text": SYSTEM_CONFIG + prompt}]}]
    response = await send_message(message_log, cid, gemini_pro_model)
    pbar.update(1)

    if response is None:
        return
    
    with open('chebi/{}.txt'.format(cid), 'w+', encoding="utf-8") as file:
        file.write(response)
