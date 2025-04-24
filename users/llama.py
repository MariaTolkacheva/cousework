import torch
from huggingface_hub import login
from transformers import pipeline

# Authenticate with Hugging Face


model_id = "meta-llama/Meta-Llama-3-8B"

pipeline = pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto"
)

print(pipeline("Hey, how are you doing today?"))
