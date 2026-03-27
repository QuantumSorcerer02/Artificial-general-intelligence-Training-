import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
print(f"Loading model from: {model_path}")

try:
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    print("Model and tokenizer loaded successfully.")
    
    # Simple inference test
    input_text = "Hello, Chloe!"
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=20)
    print(f"Output: {tokenizer.decode(outputs[0], skip_special_tokens=True)}")

except Exception as e:
    print(f"Error: {e}")
