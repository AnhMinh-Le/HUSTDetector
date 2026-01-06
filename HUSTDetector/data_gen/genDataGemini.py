import json
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")
# L1: Fully LLM-generated abstract prompt
system_prompt_l1 = """
You are an academic researcher writing a scientific abstract. 
Your task is to write a formal 200-word scientific abstract based on the methodology and objectives described in a paper introduction.
Use professional academic vocabulary. Avoid starting with 'In this paper'. Start directly with the problem statement.
"""

# L2: Human-LLM Collaborative abstract prompt
system_prompt_l2 = """
You are a professional academic editor refining a scientific abstract.
Your task is to rewrite an abstract to improve its stylistic flow and technical clarity.
Change the sentence structures while preserving all original data and findings.
Modify at least 30% of the text to sound like a refined version for a top-tier conference.
"""
def generate_text_l1(introduction, paper_id):
    """Generate L1: Fully LLM-generated abstract from introduction"""
    try:
        user_prompt = f"""Context: {introduction}

Task: Based on the methodology and objectives described in this introduction, write a formal 200-word scientific abstract.
Constraint: Use professional academic vocabulary; avoid 'In this paper', start directly with the problem statement."""
        
        chat = model.start_chat(
            history=[
                {"role": "model", "parts": system_prompt_l1},
            ]
        )
        response = chat.send_message(user_prompt)
        return response.text
    except Exception as e:
        print(f"L1 Generation failed - Paper ID: {paper_id}, Error: {str(e)}")
        return ""

def generate_text_l2(original_abstract, paper_id):
    """Generate L2: Human-LLM Collaborative abstract from original abstract"""
    try:
        user_prompt = f"""Context: {original_abstract}

Task: Rewrite the following abstract to improve its stylistic flow and technical clarity. Change the sentence structures while preserving all original data and findings. Modify at least 30% of the text to sound like a refined version for a top-tier conference."""
        
        chat = model.start_chat(
            history=[
                {"role": "model", "parts": system_prompt_l2},
            ]
        )
        response = chat.send_message(user_prompt)
        return response.text
    except Exception as e:
        print(f"L2 Generation failed - Paper ID: {paper_id}, Error: {str(e)}")
        return ""

# read the input file
inputfile = "input.jsonl"
output_jsonl = "output.jsonl"

dataset = []
count = 0
failed_generation = []
with open(inputfile, 'r', encoding='utf-8') as file:
    for line in file:
        paper_data = json.loads(line)
        paper_id = paper_data.get('id', f'paper-{count}')
        introduction = paper_data.get('introduction', '')
        original_abstract = paper_data.get('abstract', '')
        
        # Generate L1: Fully LLM-generated abstract
        if introduction:
            generated_text_l1 = generate_text_l1(introduction, paper_id)
            if generated_text_l1:
                entry_l1 = {
                    "text": generated_text_l1,
                    "label": "AI",
                    "label_detailed": "gemini-text",
                    "paper_id": paper_id,
                    "type": "L1",
                    "model": "gemini-1.5-flash",
                }
                dataset.append(entry_l1)
                count += 1
                print(f"Generated L1 record {count}, Paper ID: {paper_id}")
            else:
                failed_generation.append({
                    "paper_id": paper_id,
                    "type": "L1",
                    "count": count,
                })
        
        # Generate L2: Human-LLM Collaborative abstract
        if original_abstract:
            generated_text_l2 = generate_text_l2(original_abstract, paper_id)
            if generated_text_l2:
                entry_l2 = {
                    "text": generated_text_l2,
                    "label": "human+AI",
                    "label_detailed": "human---gemini-text",
                    "paper_id": paper_id,
                    "type": "L2",
                    "model": "gemini-1.5-flash",
                }
                dataset.append(entry_l2)
                count += 1
                print(f"Generated L2 record {count}, Paper ID: {paper_id}")
            else:
                failed_generation.append({
                    "paper_id": paper_id,
                    "type": "L2",
                    "count": count,
                })

# log failed generations
if failed_generation:
    print("Summary of failed generations:\n")
    for fail in failed_generation:
        print(f"Failed - Paper ID: {fail['paper_id']}, Type: {fail['type']}, Count: {fail['count']}")

# Save all solutions to JSONL file
with open(output_jsonl, "w", encoding='utf-8') as f:
    for entry in dataset:
        f.write(json.dumps(entry) + "\n")
print(f"Dataset saved to {output_jsonl}")
