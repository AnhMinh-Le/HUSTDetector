import logging
from openai import OpenAI
import google.generativeai as genai
import dotenv

def get_deepseek_response(system_prompt = None, user_prompt = None, 
                       api_key=deepseek_api_key, 
                       base_url="https://api.deepseek.com", retries=5, timeout=45):
    client = OpenAI(api_key=api_key, base_url=base_url)
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=False,
                timeout=timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"[get_llama_response] Attempt {attempt+1}/{retries} failed: {e}")
    return ""



def get_gemini_response(system_prompt=None, user_prompt=None, api_key=gemini_api_key, retries=3):
    api_key = gemini_api_key
    genai.configure(api_key=api_key)
    for attempt in range(retries):
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            chat = model.start_chat(history=[{"role": "model", "parts": system_prompt}])
            response = chat.send_message(user_prompt)
            return response.text
        except Exception as e:
            logging.error(f"[get_gemini_response] Attempt {attempt+1}/{retries} failed: {e}")
    return None


def get_llama_response(system_prompt = None, user_prompt = None, 
                       api_key=llama_api_key, 
                       base_url="https://api.together.xyz/v1", retries=3, timeout=30):
    client = OpenAI(api_key=api_key, base_url=base_url)
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=False,
                timeout=timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"[get_llama_response] Attempt {attempt+1}/{retries} failed: {e}")
    return ""


def get_gpt4omini_response(system_message=None, query=None, retries=3, timeout=30, api_key=gpt_api_key):
    client = OpenAI(api_key=api_key, timeout=timeout)
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  
                temperature=0 + attempt * 0.1,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": query},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"[get_gpt4o_response] Attempt {attempt+1}/{retries} failed: {e}")
    return ""


