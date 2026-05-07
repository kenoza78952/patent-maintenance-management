import os
import json
import time
import pandas as pd
from openai import OpenAI
import threading
from .exceptions import GPTInvalidColumnsError 

def load_config():
   
    current_directory = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(current_directory, 'config.json')

    if not os.path.exists(config_path):
        raise FileNotFoundError("Configuration file not found. Please ensure that config.json is in the gpt_utils directory.")
    
    with open(config_path, 'r') as file:
        return json.load(file)

def call_gpt_model(model, prompt, input_text):
   
    config = load_config()
    api_key = config.get('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("API key is not set in the configuration file.")

    client = OpenAI(api_key=api_key)

    try:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"{prompt} {input_text}"
                },
                {
                    "role": "user",
                    "content": input_text
                }
            ]
        )
      
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"API request failed: {str(e)}"

def handle_multiple_requests(model, prompt, inputs, rate_limit_per_second=1):
   
    config = load_config()
    api_key = config.get('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("API key is not set in the configuration file.")

    threads = []
    responses = [None] * len(inputs)

    def request_with_delay(i):
        time.sleep(i / rate_limit_per_second) 
        call_gpt_model(model, prompt, inputs[i])

    for i in range(len(inputs)):
        thread = threading.Thread(target=request_with_delay, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return responses

    
def clean_and_extract_relevant_columns(excel_file_path, selected_columns):
    try:
        df = pd.read_excel(excel_file_path)
        
        required_columns = ['Patent/ Publication Number'] + selected_columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise GPTInvalidColumnsError(missing_columns, required_columns)

        df = df[required_columns]
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"The specified Excel file was not found: {excel_file_path}")
    except GPTInvalidColumnsError as e:
        raise e 
    except Exception as e:
        raise Exception(f"Failed to process the Excel file: {str(e)}")


def categorize_claims(df, model, prompt, selected_columns):
    gpt_results = []

    column_labels = {
        'First Claim': 'First Claim: ',
        'Title': 'Title: ',
        'Abstract': 'Abstract: ',
    }

    for i, row in df.iterrows():
        try:
            input_text = ' '.join([f"{column_labels[col]}{str(row[col])}" for col in selected_columns if col in row])
            
            full_input = f"{prompt}\n\n{input_text}"

            gpt_category = call_gpt_model(model, prompt, full_input)
            gpt_results.append(gpt_category)
        except Exception as e:
            gpt_results.append(f"Error categorizing: {str(e)}")

    df['GPT Category'] = gpt_results
    return df


def save_to_excel(df, output_file_path):
    
    try:
        df.to_excel(output_file_path, index=False)
    except Exception as e:
        raise Exception(f"Failed to save the DataFrame to Excel: {str(e)}")
