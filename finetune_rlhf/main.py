import torch
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    TextDataset,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
    BitsAndBytesConfig,
    AutoTokenizer,
    AutoModelForCausalLM,
)
import torch
from peft import LoraConfig

# Load model directly

model_name = "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T"
tokenizer = AutoTokenizer.from_pretrained(model_name)  #
# Quantisation
# Configure the model for 8-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,  # For 8-bit quantization
    load_in_4bit=False,  # Set to True if you want 4-bit quantization
)
# Configure the model for 8-bit quantization
# bnb_config = BitsAndBytesConfig.from_pretrained(model_name, load_in_8bit=True)

# Load the quantized model
model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
##Adding trainable quantised peft adapter which will help in transfer learning through layer freezing

peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=64,
    bias="none",
    task_type="CAUSAL_LM",
)
model.add_adapter(peft_config)
# # Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)


# Function to load dataset
def load_dataset(file_path, tokenizer, block_size=128):
    dataset = TextDataset(
        tokenizer=tokenizer, file_path=file_path, block_size=block_size
    )
    return dataset


# Function to create data collator
def create_data_collator(tokenizer):
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # Masked Language Modeling (MLM) is false for autoregressive models like GPT-2
    )
    return data_collator


# Load dataset
train_dataset = load_dataset("/kaggle/working/new_file.txt", tokenizer)

# Create data collator
data_collator = create_data_collator(tokenizer)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=20,
    per_device_train_batch_size=8,
    save_steps=10_000,
    save_total_limit=2,
    prediction_loss_only=True,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)
# Train the base model
trainer.train()