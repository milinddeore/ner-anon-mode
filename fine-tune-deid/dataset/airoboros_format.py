# -*- coding:utf8 -*-
# !/usr/bin/env python
# Written by Milind Deore <tomdeore@gmail.com>, Aug 2023
# This script test freshly fine-tunned HF model from hub.
# Airoboros prompt format is following:

```
"""A chat.
USER: Can you explain the difference between vector and dequeue in C++?
ASSISTANT: """
```

# Or the prompt should look like one of these:

```
{system_instruction}\nUSER: {user_instruction} PLAINFORMAT\nASSISTANT:
{system_instruction}\nUSER: {user_instruction}\nPLAINFORMAT ASSISTANT:
{system_instruction}\nUSER: {user_instruction} \nASSISTANT:
{system_instruction}\nUSER: {user_instruction}\nASSISTANT:
```

#Reference:
# [1](https://chat.openai.com/share/8e98059c-723a-460f-88f4-f010ec996925)
# [2](https://huggingface.co/jondurbin/airoboros-c34b-2.1)


import json

# validate the dataset, if it has a valid pair of 'USER: ' and 'ASSISTANT: '
with open("/content/nonymus_ner_dataset") as rf:
    count = 0
    flag = ""
    for line in rf:
      if line.startswith("USER: "):
        flag = "U"
        count += 1
      elif line.startswith("ASSISTANT: "):
        if flag != "U":
          flag = "U"
          print("Something got screwed up!!!")

    print(f"count: {count}")

# Convertion starts here, in steps:
with open('/content/data.txt', 'w') as wf:
  with open("/content/nonymus_ner_dataset") as rf:
      for line in rf:
        if line.startswith("USER: "):
          wf.write(line)
        elif line.startswith("ASSISTANT: "):
          tmp_line = line.replace("{{", "{")
          tmp_line = tmp_line.replace("}}", "}")
          #tmp_line = tmp_line.replace('"', '\\"')
          wf.write(tmp_line)
          wf.write("\n")
      print(f"count: {count}")


prompt = "Find the Named Entity Recongnition for a given input and return the output, for the following classes: PERSON, LOCATION, PHONE, ACCOUNTNUMBER, EMAIL, URL, AGE, COMPANY, JOB_TITLE, GENDER, ADDRESS, COUNTY. Use the following output format (fill in everything in between curly brackets). Do not include any other text."

with open('/content/train.jsonl', 'w') as wf:
  with open("/content/data.txt") as rf:
    for line in rf:
      if line.startswith("USER"):
        text = '{"instruction": "' + prompt + ' ' + line.rstrip().replace('"', "") + '", '
      elif line.startswith("ASSISTANT"):
        if text == '':
          print(f"Something gone Wrong, bailout!")
          continue
        else:
          text += '"response": "' + line.rstrip().replace('"', "'") + '"}'
          #print(text)
          wf.write(json.dumps(text) + "\n")
        text = ''

