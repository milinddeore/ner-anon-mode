# -*- coding:utf8 -*-
# !/usr/bin/env python
# Written by Milind Deore <tomdeore@gmail.com>, Aug 2023
# This script test freshly fine-tunned HF model from hub.
# Merge the adaptor layer with the base model and push it to the hub

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from transformers import Trainer
from transformers import TrainingArguments

base_model_path = "abhishek/llama-2-7b-hf-small-shards"
adapter_path = "/Users/milinddeore/PROJECTS/nonymus/merge_and_push_to_hub/nonymus-llm/"

model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True)

model = PeftModel.from_pretrained(model, adapter_path)
tokenizer = AutoTokenizer.from_pretrained(base_model_path)
model = model.merge_and_unload()

hf_repo = "tomdeore/nonymus-llm"
access_token = "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"

args = TrainingArguments(push_to_hub=True, learning_rate=2e-4, output_dir="nonymus-llm")
trainer = Trainer(model, args, tokenizer=tokenizer)
trainer.push_to_hub()

