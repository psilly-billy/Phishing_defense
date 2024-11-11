import json
import random

# Load the larger training dataset
input_file_path = 'data\phishing_training_data.jsonl'  # Update with the path where your original JSONL file is saved
output_file_path = 'phishing_training_data_reduced_8000.jsonl'

# Load the data
with open(input_file_path, 'r') as f:
    data = [json.loads(line) for line in f]

# Randomly sample 8000 examples
sampled_data = random.sample(data, 8000)

# Save the reduced dataset
with open(output_file_path, 'w') as f:
    for entry in sampled_data:
        json.dump(entry, f)
        f.write('\n')

print(f"Reduced dataset saved to {output_file_path}")
