import os
from openai import OpenAI


# API Key


# Define the OpenAI moldel algorithm
# GPT_MODEL = "gpt-3.5-turbo-1106" #"gpt-3.5-turbo-1106" 
# gpt-3.5-turbo
GPT_MODEL = "gpt-3.5-turbo-1106"




def initPrompt(text_input:str,new_prompt=None):
    
    if new_prompt is None:
        prompt_default = f"""
            You will receive a text enclosed within triple quotes. Please summarize this text in approximately 1500 words, 
            focusing on the main issue presented. Additionally, identify the primary emotion expressed in the text. 
            The response should be structured into two sections: a summary, and an analysis of the main issue and emotion, all in English.
            Prompt format:
            [\"\"\"{text_input}\"\"\"]. 
            """
        return prompt_default
    else:
        new_prompt_version = new_prompt.format(text_input=text_input)
        return new_prompt_version


def prompt_solution(text_input):
    prompt_default_solution = f"""
        Find the solution [\"\"\"{text_input}\"\"\"]. 
    """
    return prompt_default_solution

def llm_summary_chatGPT(user_input:str,openAIKey=None, model_llm=None, prompt_model=None,custom_messages=None,condition=True):
    # define the command
    if openAIKey is None:
        openAIKey = OPENAI_API_KEY
    if model_llm is None:
        model_llm = GPT_MODEL
    if condition is True:
        # init prompt model
        prompt_model = initPrompt(user_input,prompt_model)
    else:
        prompt_model = prompt_solution(user_input)
    # Use custom messages if provided, otherwise use the default structure
    if custom_messages is None:
        messages = [{"role": "system", "content": prompt_model}]
    else:
        messages = [{"role": "system", "content": prompt_model}] + custom_messages
        
    print("prompt_model:",prompt_model)    
    client = OpenAI(api_key=openAIKey) # Init OpenAI with OpenAI API key
    # Action models
    response = client.chat.completions.create(
            model=model_llm,
            messages=messages,
            temperature=0
        )
    return response.choices[0].message.content