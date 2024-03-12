# -*- coding:utf8 -*-
# !/usr/bin/env python
# Written by Milind Deore <tomdeore@gmail.com>, Aug 2023
# This script test freshly fine-tunned HF model from hub.

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

model_id = "tomdeore/nonymus-llm"
quantization_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_compute_dtype=torch.float16
)

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=quantization_config,
    device_map="auto",
)

print("Model and Tokenizer are loaded")

prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:

Find the Named Entity Recongnition for a given input and return the output, for the following classes: PERSON, LOCATION, PHONE, ACCOUNTNUMBER, EMAIL, URL, AGE, COMPANY, JOB_TITLE, GENDER, ADDRESS, COUNTY. Use the following output format (fill in everything in between curly brackets). Do not include any other text.

### Input:
Jagan and Milind Madhukar Deore are both good friends and going to start their own company soon by name nonymus.

### Response: """

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

output = model.generate(
    inputs["input_ids"],
    max_new_tokens=1024,
    do_sample=True,
    top_p=0.6,
    temperature=0.4,
)
output = output[0].to("cpu")
print(tokenizer.decode(output))

