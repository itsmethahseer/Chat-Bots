import torch
from transformers import BertForQuestionAnswering, BertTokenizer
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
import json

# Define your dataset
class QADataset(Dataset):
    def __init__(self, contexts, questions, answers, tokenizer, max_length):
        self.contexts = contexts
        self.questions = questions
        self.answers = answers
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.contexts)

    def __getitem__(self, idx):
        context = str(self.contexts[idx])
        question = str(self.questions[idx])
        answer = str(self.answers[idx])

        # Tokenize with dynamic padding
        inputs = self.tokenizer.encode_plus(
            question,
            context,
            truncation=True,
            max_length=self.max_length,
            padding='max_length',
            return_tensors='pt'
        )

        # Update max_length based on the actual lengths in the batch
        self.max_length = max(len(inputs['input_ids'][0]), self.max_length)

        target = self.tokenizer.encode(answer, add_special_tokens=False)

        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'start_positions': torch.tensor([target[0]]),
            'end_positions': torch.tensor([target[-1]])
        }


with open('/home/c847/Desktop/Bert_Finetuned/data/data.json', 'r') as f:
    data = json.load(f)

# Extract contexts, questions, and answers from the loaded data
contexts = [entry['context'] for entry in data]
questions = [qa['question'] for entry in data for qa in entry['questions']]
answers = [qa['answer'] for entry in data for qa in entry['questions']]

# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

# Create a dataset instance
max_length = 256  # You can adjust this based on your specific needs
dataset = QADataset(contexts, questions, answers, tokenizer, max_length)

# Split the dataset into training and validation sets
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])


# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)

# Set up optimizer and scheduler
optimizer = AdamW(model.parameters(), lr=5e-5, weight_decay=0.01)
epochs = 50  # You can adjust this based on your specific needs
device = torch.device("cpu")
# Fine-tuning loop
for epoch in range(epochs):
    model.train()
    for batch in train_loader:
        inputs = {key: value.to(device) for key, value in batch.items()}
        outputs = model(**inputs)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    # Validation
    model.eval()
    with torch.no_grad():
        for batch in val_loader:
            inputs = {key: value.to(device) for key, value in batch.items()}
            outputs = model(**inputs)
            # Evaluate your validation metrics here

# Save the fine-tuned model
model.save_pretrained('fine_tuned_bert_model')
tokenizer.save_pretrained('fine_tuned_bert_model')
