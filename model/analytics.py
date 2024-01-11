import os
from openai import OpenAI
import pandas as pd
from openpyxl import Workbook
import json
import requests
from utils import OPENAI_API_KEY_BB

# Load the CSV file
file_path = './data/CrispConvoTracking - Sheet13 (4).csv'
df = pd.read_csv(file_path)
# API Key
# OPENAI_API_KEY = "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"  # 4.0
GPT_MODEL = "gpt-3.5-turbo-1106"
OPENAI_API_KEY= OPENAI_API_KEY_BB

# def api_analytics(user_input: str):
#     prompt_model = f"""
#         Analyze for me the conversation [\"\"\"{user_input}\"\"\"] And tell me what is the "Bug", "Feature" and "UX/UI. as json format "Bug", "Feature" and "UX/UI
#             """   
#     messages = [{"role": "system", "content": prompt_model}]

#     client = OpenAI(api_key=OPENAI_API_KEY)  # Init OpenAI with OpenAI API key
#     # Action models
#     response = client.chat.completions.create(
#         model=GPT_MODEL, messages=messages, temperature=0
#     )
#     final = response.choices[0].message.content
#     return json.loads(final)


def api_analytics(user_input:str):
    prompt_model = f"""
        Analyze for me the conversation [\"\"\"{user_input}\"\"\"] And tell me what is the "Bug", "Feature" and "UX/UI. as json format "Bug", "Feature" and "UX/UI
            """
    requests_body = {
    "messages": [{"role": "system", "content": prompt_model}],
    "max_tokens": 2500,
    "temperature": 0.7,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "top_p": 0.95,
    "stop": None,
    "stream": True
  }
    headers = {
      "Content-Type": "application/json",
      "Api-Key": OPENAI_API_KEY,
    }
    host = 'https://bb-ai.openai.azure.com/openai/deployments/generative_text/chat/completions?api-version=2023-07-01-preview'
    inp_post_response = requests.post(host, json=requests_body,headers=headers);
    if inp_post_response.status_code == 200:
        data = inp_post_response.content
        data_str = data.decode('utf-8')
        json_objects = []
        for line in data_str.split('\n'):
            if line.startswith('data:'):
                line = line.replace("data: ", "")
                try:
                    json_object = json.loads(line)
                    json_objects.append(json_object)
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON line: {e}")
        contentObj = ''
        for json_obj in json_objects:
            if 'choices' in json_obj:
                # Check if 'choices' list exists and is not empty
                if 'choices' in json_obj and len(json_obj['choices']) > 0:
                    # Check if 'delta' and 'content' keys exist
                    if 'delta' in json_obj['choices'][0] and 'content' in json_obj['choices'][0]['delta']:
                        # Access the 'content' value
                        content = json_obj['choices'][0]['delta']['content']
                        contentObj += content
                        
                    else:
                        print("No 'content' key in 'delta'")
                else:
                    print("No 'choices' found or 'choices' list is empty")
        data = json.loads(contentObj)
        return data
        
    




# Apply the mock API function to the 'Content' column
# Note: In a real-world scenario, you would replace this with actual API calls
analyzed_content = df['Content'].apply(api_analytics)

# print(analyzed_content.tolist())

# Convert the results to a DataFrame
analyzed_df = pd.DataFrame(analyzed_content.tolist())
# print(analyzed_df)
# Combining the analyzed content with the original DataFrame
df_combined = pd.concat([df, analyzed_df], axis=1)
# Selecting and renaming the required columns for the new Excel file
output_columns = ['Ticket URL', 'Bug', 'Feature', 'UX/UI']
output_df = df_combined[output_columns].copy()

output_df.insert(0, 'No.', range(1, 1 + len(output_df)))

# Save the output dataframe to an Excel file
output_file_path = './result/analyzed_content.xlsx'
output_df.to_excel(output_file_path, index=False)
print("created output file")