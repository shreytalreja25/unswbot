import json

def yes_no(value):
    return "Yes" if value == "true" else "No"

def generate_jsonl_from_json(json_file_path, jsonl_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    conversations = []
    
    for item in data['degrees']:
        degree_name = item['title']
        degree_summary = item['summary']
        part_time = yes_no(item['metaData'].get('degreePartTime', 'false'))
        full_time = yes_no(item['metaData'].get('degreeFullTime', 'false'))
        delivery_mode = item['metaData'].get('degreeDeliveryMode', 'not specified')
        degree_type = item['metaData'].get('degreeType', 'not specified')
        eligibility = item['metaData'].get('degreeEligibility', 'not specified')
        campus = item['metaData'].get('degreeCampus', 'not specified')
        duration = item['metaData'].get('degreeDuration', 'not specified')

        # Basic details about the degree
        conversations.append({
            "messages": [
                {"role": "user", "content": f"What can you tell me about {degree_name}?"},
                {"role": "assistant", "content": f"{degree_name} is a {degree_type} program offered at the {campus} campus. It is {part_time} part-time and {full_time} full-time, with a duration of {duration}. Delivery mode: {delivery_mode}. Eligibility: {eligibility}."}
            ]
        })

        # Detailed summary of the degree
        conversations.append({
            "messages": [
                {"role": "user", "content": f"Can I get more details about the {degree_name}?"},
                {"role": "assistant", "content": f"{degree_summary}"}
            ]
        })

        # Questions about part-time availability
        conversations.append({
            "messages": [
                {"role": "user", "content": f"Is {degree_name} available as a part-time program?"},
                {"role": "assistant", "content": f"{part_time}"}
            ]
        })

        # Questions about campus location
        conversations.append({
            "messages": [
                {"role": "user", "content": f"Where is {degree_name} taught?"},
                {"role": "assistant", "content": f"The program is taught at the {campus} campus."}
            ]
        })

    # Write to JSONL
    with open(jsonl_file_path, 'w') as outfile:
        for convo in conversations:
            json.dump(convo, outfile)
            outfile.write('\n')

# Example usage
generate_jsonl_from_json('clean_unsw_data.json', 'unsw_conversations.jsonl')
