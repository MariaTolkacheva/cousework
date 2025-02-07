from transformers import pipeline
import torch
from huggingface_hub import login

# Authenticate with Hugging Face


model_id = "meta-llama/Meta-Llama-3-8B"
print('I am here')

pipeline = pipeline(
    "text-generation", 
    model=model_id, 
    model_kwargs={"torch_dtype": torch.bfloat16}, 
    device_map="auto"
)

print(pipeline("Hey, how are you doing today?"))
