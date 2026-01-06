import json

def clean_jsonl_solutions(input_file, output_file):
    """
    Cleans the `solution` field in a JSONL file by removing ```{language}``` and ``` markers.
    
    :param input_file: Path to the input JSONL file.
    :param output_file: Path to the output JSONL file with cleaned content.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            entry = json.loads(line)
            if "solution" in entry:
                # Remove markdown code block markers
                entry["solution"] = entry["solution"].replace("```cpp\n", "").replace("```java\n", "").replace("```c\n", "").replace("```python\n", "").replace("```", "").strip()
            outfile.write(json.dumps(entry) + '\n')

clean_jsonl_solutions("input.jsonl", "output.jsonl")
