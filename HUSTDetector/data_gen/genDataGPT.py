import json
import logging
from libs.config import settings
from chatter import Chatter  

# L1: Fully LLM-generated abstract
chatter_l1 = Chatter(
    system_message=(
        "You are an academic researcher writing a scientific abstract. "
        "Your task is to write a formal 200-word scientific abstract based on the methodology and objectives described in a paper introduction. "
        "Use professional academic vocabulary. Avoid starting with 'In this paper'. Start directly with the problem statement."
    )
)

# L2: Human-LLM Collaborative abstract
chatter_l2 = Chatter(
    system_message=(
        "You are a professional academic editor refining a scientific abstract. "
        "Your task is to rewrite an abstract to improve its stylistic flow and technical clarity. "
        "Change the sentence structures while preserving all original data and findings. "
        "Modify at least 30% of the text to sound like a refined version for a top-tier conference."
    )
)

inputfile = r"input.jsonl"
output_jsonl = r"output.jsonl"

dataset = []
failed_generation = []
count = 0

with open(inputfile, 'r', encoding='utf-8') as file:
    for line in file:
        paper_data = json.loads(line.strip())
        paper_id = paper_data.get('id', f'paper-{count}')
        introduction = paper_data.get('introduction', '')
        original_abstract = paper_data.get('abstract', '')

        # Generate L1: Fully LLM-generated abstract
        if introduction:
            prompt_l1 = f"""Context: {introduction}

Task: Based on the methodology and objectives described in this introduction, write a formal 200-word scientific abstract.
Constraint: Use professional academic vocabulary; avoid 'In this paper', start directly with the problem statement."""

            generated_text_l1 = chatter_l1.chat(prompt_l1)
            
            if not generated_text_l1.strip():
                logging.error(f"L1 Generation failed - Paper ID: {paper_id}")
                failed_generation.append({
                    "paper_id": paper_id,
                    "type": "L1",
                    "count": count,
                })
            else:
                entry_l1 = {
                    "text": generated_text_l1.strip(),
                    "label": "AI",
                    "label_detailed": "gpt-text",
                    "paper_id": paper_id,
                    "type": "L1",
                    "model": "gpt-4o-mini",
                }
                dataset.append(entry_l1)
                count += 1
                print(f"Generated L1 record {count}, Paper ID: {paper_id}")

        # Generate L2: Human-LLM Collaborative abstract
        if original_abstract:
            prompt_l2 = f"""Context: {original_abstract}

Task: Rewrite the following abstract to improve its stylistic flow and technical clarity. Change the sentence structures while preserving all original data and findings. Modify at least 30% of the text to sound like a refined version for a top-tier conference."""

            generated_text_l2 = chatter_l2.chat(prompt_l2)
            
            if not generated_text_l2.strip():
                logging.error(f"L2 Generation failed - Paper ID: {paper_id}")
                failed_generation.append({
                    "paper_id": paper_id,
                    "type": "L2",
                    "count": count,
                })
            else:
                entry_l2 = {
                    "text": generated_text_l2.strip(),
                    "label": "human+AI",
                    "label_detailed": "human---gpt-text",
                    "paper_id": paper_id,
                    "type": "L2",
                    "model": "gpt-4o-mini",
                }
                dataset.append(entry_l2)
                count += 1
                print(f"Generated L2 record {count}, Paper ID: {paper_id}")

if failed_generation:
    logging.error("Summary of failed generations:")
    for fail in failed_generation:
        logging.error(f"Failed - Paper ID: {fail['paper_id']}, Type: {fail['type']}, Count: {fail['count']}")

# Lưu tất cả kết quả thành công vào tệp JSONL
with open(output_jsonl, 'w', encoding='utf-8') as jsonlfile:
    for data in dataset:
        jsonlfile.write(json.dumps(data) + "\n")

print(f"Dataset saved to {output_jsonl}")

