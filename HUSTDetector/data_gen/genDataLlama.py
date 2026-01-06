import os
from openai import OpenAI
import jsonlines

# L1: Fully LLM-generated abstract
system_content_l1 = "You are an academic researcher writing a scientific abstract. Your task is to write a formal 200-word scientific abstract based on the methodology and objectives described in a paper introduction. Use professional academic vocabulary. Avoid starting with 'In this paper'. Start directly with the problem statement."

# L2: Human-LLM Collaborative abstract
system_content_l2 = "You are a professional academic editor refining a scientific abstract. Your task is to rewrite an abstract to improve its stylistic flow and technical clarity. Change the sentence structures while preserving all original data and findings. Modify at least 30% of the text to sound like a refined version for a top-tier conference."
languages = ['C', 'C++', 'Python', 'Java']
model_ai = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
input_file = "data/original/code_problems.jsonl"
output_file = "data/generated/new/uncleaned/solution_llama3.1_first500.jsonl"

client = OpenAI(
  #change token_api 
  api_key=os.environ.get("TOGETHER_API_KEY_2"),
  base_url="https://api.together.xyz/v1",
)

data = []
with jsonlines.open(input_file) as file:
    for line in file:
       data.append(line)

def get_user_content_l1(introduction):
    return f"""Context: {introduction}

Task: Based on the methodology and objectives described in this introduction, write a formal 200-word scientific abstract.
Constraint: Use professional academic vocabulary; avoid 'In this paper', start directly with the problem statement."""

def get_user_content_l2(original_abstract):
    return f"""Context: {original_abstract}

Task: Rewrite the following abstract to improve its stylistic flow and technical clarity. Change the sentence structures while preserving all original data and findings. Modify at least 30% of the text to sound like a refined version for a top-tier conference."""

count=0
stop_process = False
for item in data[:500]:
  process = []
  if stop_process:
    break
  paper_id = item.get('id', f'paper-{count}')
  introduction = item.get('introduction', '')
  original_abstract = item.get('abstract', '')
  
  # Generate L1: Fully LLM-generated abstract
  if introduction:
    user_content_l1 = get_user_content_l1(introduction)
    try:
      response = client.chat.completions.create(
        model=model_ai,
        messages=[
          {"role": "system", "content": system_content_l1},
          {"role": "user", "content": user_content_l1},
        ]
      )
      count+=1
      process.append({
        "text": response.choices[0].message.content,
        "label": "AI",
        "label_detailed": "llama-text",
        "paper_id": paper_id,
        "type": "L1",
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
      })
    except Exception as e:
      print(e)
      print(f"L1 Error in {paper_id}")
      stop_process = True
      break
  
  # Generate L2: Human-LLM Collaborative abstract
  if original_abstract:
    user_content_l2 = get_user_content_l2(original_abstract)
    try:
      response = client.chat.completions.create(
        model=model_ai,
        messages=[
          {"role": "system", "content": system_content_l2},
          {"role": "user", "content": user_content_l2},
        ]
      )
      count+=1
      process.append({
        "text": response.choices[0].message.content,
        "label": "human+AI",
        "label_detailed": "human---llama-text",
        "paper_id": paper_id,
        "type": "L2",
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
      })
    except Exception as e:
      print(e)
      print(f"L2 Error in {paper_id}")
      stop_process = True
      break
      
  if process:
    with jsonlines.open(output_file, mode="a") as  file:
      file.write_all(process)

