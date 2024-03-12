# Hardware requirements:
Tries on `Tesla T4` but can run any GPU beyond T4. 

# Requirements:

After installing `autotrain-advance`, we must update the torch and other dependencies. It can be done using following command:

```
autotrain setup --update-torch
```

# To upload model to HF Hub (optional):
```
huggingface-cli login
```

# Login to HF:
Run following command to start the training, 

```
autotrain llm --train --project_name nonymus-llm --model abhishek/llama-2-7b-hf-small-shards --data_path . --use_peft --use_int4 --learning_rate 2e-4 --train_batch_size 4 --num_train_epochs 3 --trainer sft --push_to_hub --repo_id tomdeore/nonymus-llm --merge-adapter
```
