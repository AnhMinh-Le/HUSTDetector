import os

def split_jsonl_file(input_file, output_dir, lines_per_file=2000):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        file_count = 0
        lines = []
        
        for line_number, line in enumerate(infile, start=1):
            lines.append(line)
            
            if line_number % lines_per_file == 0:
                output_file = os.path.join(output_dir, f"part_{file_count}.jsonl")
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    outfile.writelines(lines)
                file_count += 1
                lines = []
        
        if lines:
            output_file = os.path.join(output_dir, f"part_{file_count}.jsonl")
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.writelines(lines)

input_file = 'input.jsonl'
output_dir = 'output'
lines_per_file = 100

split_jsonl_file(input_file, output_dir, lines_per_file)
