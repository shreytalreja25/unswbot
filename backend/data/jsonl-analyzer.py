import json
import tiktoken  # Assuming tiktoken is properly installed and set up
from collections import defaultdict
import numpy as np

def load_dataset(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

def validate_format(dataset):
    errors = defaultdict(int)
    for ex in dataset:
        if not isinstance(ex, dict):
            errors['data_type'] += 1
            continue
        
        messages = ex.get("messages")
        if not messages:
            errors["missing_messages_list"] += 1
            continue
        
        for message in messages:
            if "role" not in message or "content" not in message:
                errors["message_missing_key"] += 1
            if any(k not in ("role", "content", "weight", "function_call", "name") for k in message):
                errors["message_unrecognized_key"] += 1
            if message.get("role") not in ("system", "user", "assistant", "function"):
                errors["unrecognized_role"] += 1
            if not isinstance(message.get("content", ""), str):
                errors["invalid_content"] += 1
    return errors

def print_errors(errors):
    if errors:
        print("Found format errors:")
        for k, v in errors.items():
            print(f"{k}: {v}")
    else:
        print("No format errors found.")

def token_statistics(dataset, encoding):
    message_counts = []
    token_counts = []
    
    for ex in dataset:
        num_tokens = 0
        messages = ex.get("messages", [])
        for message in messages:
            num_tokens += len(encoding.encode(message['content']))
        message_counts.append(len(messages))
        token_counts.append(num_tokens)
    
    return message_counts, token_counts

def print_distribution(values, name):
    print(f"\n#### Distribution of {name}:")
    print(f"Min / Max: {min(values)}, {max(values)}")
    print(f"Mean / Median: {np.mean(values):.2f}, {np.median(values)}")
    print(f"P5 / P95: {np.percentile(values, 5)}, {np.percentile(values, 95)}")

def main(data_path):
    dataset = load_dataset(data_path)
    errors = validate_format(dataset)
    print_errors(errors)
    
    encoding = tiktoken.get_encoding("cl100k_base")
    message_counts, token_counts = token_statistics(dataset, encoding)
    
    print_distribution(message_counts, "messages per example")
    print_distribution(token_counts, "tokens per example")

# Replace 'your_data_file.jsonl' with the path to your JSONL file
main('unsw_conversations.jsonl')
