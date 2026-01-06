from openai import OpenAI
import time

client = OpenAI(
    api_key="YOUR_API_KEY",
)

file_names = [f"{i}.jsonl" for i in range(108)]
batch_ids = []
for file_name in file_names:
    try:
        print(f"Uploading {file_name}...")
        with open(file_name, "rb") as file:
            upload_response = client.files.create(
                file=file,
                purpose="batch"
            )
            file_id = upload_response.id
            print(f"Uploaded {file_name}: File ID = {file_id}")
        
        print(f"Creating batch job for {file_name}...")
        batch_response = client.batches.create(
            input_file_id=file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h"
        )
        batch_id = batch_response.id
        print(f"Batch job created: Batch ID = {batch_id}")
        batch_ids.append(batch_id)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

while True:
    for i in range(108):
        print(f"Monitoring batch job for {file_names[i]}...")
        while True:
            batch_status = client.batches.retrieve(batch_ids[i])
            print(f"{file_name} Batch Status: {batch_status.status}")
            if batch_status.status in ['completed', 'failed']:
                break
        
        if batch_status['status'] == 'completed':
            print(f"Downloading output for {file_name}...")
            output_file_id = batch_status.output_file_id
            output_file = client.files.retrieve(output_file_id)
            output_content = client.files.download(output_file['id'])
            output_path = f"gpt-4o/output/{file_name}.jsonl"
            with open(output_path, "wb") as file:
                file.write(output_content)
            print(f"Results for {file_name} saved to {output_path}")
        else:
            print(f"Batch processing failed for {file_name}.")
    time.sleep(30)
