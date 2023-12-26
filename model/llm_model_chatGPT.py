import os
from openai import OpenAI


# API Key
OPENAI_API_KEY = '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' #4.0

# Define the OpenAI moldel algorithm
# GPT_MODEL = "gpt-3.5-turbo-1106" #"gpt-3.5-turbo-1106" 
# gpt-3.5-turbo
GPT_MODEL = "gpt-3.5-turbo-1106"


def initPrompt(text_input:str,new_prompt=None):
    
    if new_prompt is None:
        prompt_default = f"""
            You will be provided with text delimited by triple quotes. 
            Can you provide the summary of the text in 1500 words approximately?And  identify the primary emotion expressed:  
            [\"\"\"{text_input}\"\"\"]. 
            The answer is divided into 2 parts: summary and emotion by English language
            """
        return prompt_default
    else:
        new_prompt_version = new_prompt.format(text_input=text_input)
        return new_prompt_version


def llm_summary_chatGPT(user_input:str,openAIKey=None, model_llm=None, prompt_model=None,custom_messages=None):
    if openAIKey is None:
        openAIKey = OPENAI_API_KEY
    if model_llm is None:
        model_llm = GPT_MODEL
    
    prompt_model = initPrompt(user_input,prompt_model)
    # Use custom messages if provided, otherwise use the default structure
    if custom_messages is None:
        messages = [{"role": "system", "content": prompt_model}]
    else:
        messages = [{"role": "system", "content": prompt_model}] + custom_messages
    client = OpenAI(api_key=openAIKey) # Init OpenAI with OpenAI API key
    # Action models
    response = client.chat.completions.create(
        model=model_llm,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content