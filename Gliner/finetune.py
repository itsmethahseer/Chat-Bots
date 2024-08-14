"""Functions for finetune Gliner NER model on custome data. 
1. clone the Gliner git code 
2. create a file named finetune.py in the gliner directory where model.py , trainer.py exists.
3. copy the code below in the finetune.py file and train , save the pretrained model weights. then load the model to predict
4. and create a dataset like input.json which is in this path.
"""

import json
import torch
from gliner.model import GLiNER
from gliner.trainer import GlinerTrainer
import gc
# Load your training data from JSON
train_path = r"/home/thahseer/Desktop/Gliner_git_cloned/GLiNER_trainer/gliner/input.json"
with open(train_path, "r",encoding="utf-8") as f:
    data = json.load(f)
print(data[:4])
# from gliner import GLiNER

# model = GLiNER.from_pretrained(r"C:\Users\abhir\Desktop\pixl\working\gliner\send\finetunemulti1")
from gliner import GLiNER
torch.cuda.empty_cache()

# model = GLiNER.from_pretrained(r"urchade/gliner_small-v1")
# # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")
# model = model.to(device)

# # Define evaluation data
# eval_data = {
#     "entity_types": ["National", "SURNAME", "FIRST NAME", "MIDDLE NAME", "DOB",
#                      "GENDER", "NATIONALITY", "HEIGHT",
#                      "IDENTITYCARD NO", "DOCUMENT TYPE"],
#     "samples": data[:4]
# }

# # Configure the trainer with adjusted learning rates and other parameters
# trainer = GlinerTrainer(
#     model,
#     train_data=data[4:],  # Assuming data is properly split
#     batch_size=2,  # Experiment with different batch sizes
#     grad_accum_every=32,
#     lr_encoder=3e-5,  # Lowering learning rate for encoder
#     lr_others=1e-5,   # Adjusted learning rate for other parts of the model
#     freeze_token_rep=False,
#     val_every_step=1000,
#     val_data=eval_data,
#     checkpoint_every_epoch=10,
#     max_types=10,
# )

# # Train the model
# trainer.train(num_epochs=50)  # You can also use num_steps instead of num_epochs

# # Save the trained model
output_dir = "./finetuned2"
# trainer.model.save_pretrained(output_dir)
# print("model saved")
model = GLiNER.from_pretrained(output_dir, local_files_only=True)

# Example text for entity prediction
text = """
FEDERAL REPUBLIC OF NIGERIA National Identity Card SURNAME ABRAHAM FIRSTNAME OBINNA KINGSLEY EXPIRY 13 MAR 34 DOCUMENTNUMBER Nimc NGA
"""
# Labels for entity prediction
labels = ["National", "SURNAME", "FIRST NAME", "MIDDLE NAME", "DOB",
                     "GENDER", "NATIONALITY", "HEIGHT",
                     "IDENTITYCARD NO"]

# Perform entity prediction
entities = model.predict_entities(text, labels, threshold=0.5)
print("entities",entities)
# Display predicted entities and their labels
for entity in entities:
    print(entity["text"], "=>", entity["label"])

torch.cuda.empty_cache()
gc.collect()