from transformers import BertForQuestionAnswering, BertTokenizer
import torch

# Load the fine-tuned model and tokenizer
model = BertForQuestionAnswering.from_pretrained('fine_tuned_bert_model')
tokenizer = BertTokenizer.from_pretrained('fine_tuned_bert_model')

context = "Common symptoms of the flu include fever, cough, and body aches."
question = "What are common symptoms of the flu"

# Tokenize input
inputs = tokenizer.encode_plus(question, context, return_tensors='pt')

# Ensure the 'input_ids' and 'attention_mask' keys are present
input_ids = inputs['input_ids']
attention_mask = inputs['attention_mask']

# Perform inference
with torch.no_grad():
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)

# Initialize variables to store the best start and end indices
best_start_index = 0
best_end_index = 0
best_score = float('-inf')

# Find the pair of start and end indices with the highest sum of scores
for i in range(len(outputs.start_logits[0])):
    for j in range(i, len(outputs.end_logits[0])):
        if outputs.start_logits[0][i] + outputs.end_logits[0][j] > best_score:
            best_start_index = i
            best_end_index = j
            best_score = outputs.start_logits[0][i] + outputs.end_logits[0][j]

# Get the answer span using 'tokenizer.decode'
answer_span_tokens = input_ids[0][best_start_index:best_end_index + 1]
answer_span = tokenizer.decode(answer_span_tokens, skip_special_tokens=True)

# Print additional information
print("Best Start Index:", best_start_index)
print("Best End Index:", best_end_index)
print("Best Score:", best_score)
print("Answer Span Tokens:", tokenizer.convert_ids_to_tokens(answer_span_tokens))

# Print the results
print("Question:", question)
print("Answer:", answer_span)
