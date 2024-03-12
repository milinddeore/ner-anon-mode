# -*- coding:utf8 -*-
# !/usr/bin/env python
# Written by Milind Deore <tomdeore@gmail.com>, Aug 2023
# This script test freshly fine-tunned HF model from hub.
# Alpaca prompt format is following:

```
text = prompt + “### Instruction:\n” + instruction + “\n ### Input:\n” + input_query  + “\n### Response:\n” + response
```

```
### Instruction:
Write a story about llamas
### Response:"
```

with open('/content/data.txt', 'w', encoding='UTF8') as wf:
  with open("/content/nonymus_ner_dataset") as rf:
      for line in rf:
        if line.startswith("USER: "):
          tmp_line = line.replace("USER:", "Instruction:")
          wf.write(tmp_line)
        elif line.startswith("ASSISTANT: "):
          tmp_line = line.replace("ASSISTANT:", "Response:")
          tmp_line = tmp_line.replace("{{", "{")
          tmp_line = tmp_line.replace("}}", "}")
          #tmp_line = tmp_line.replace('\"', '\\"')
          wf.write(tmp_line)
          wf.write("\n")

import csv

header = ['instruction', 'input', 'output', 'text']
prompt = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n"
instruction = "Find the Named Entity Recongnition for a given input and return the output, for the following classes: PERSON, LOCATION, PHONE, ACCOUNTNUMBER, EMAIL, URL, AGE, COMPANY, JOB_TITLE, GENDER, ADDRESS, COUNTY. Use the following output format (fill in everything in between curly brackets). Do not include any other text."

with open('/content/train.csv', 'w', encoding='UTF8') as wf:
  writer = csv.writer(wf, delimiter=',', quoting=csv.QUOTE_ALL, quotechar='\"')
  writer.writerow(header)
  with open("data.txt", "r", encoding='UTF8') as rf:
    for line in rf:
      if line.startswith("Instruction"):
        input_query = line.rstrip().replace('"', "").replace('Instruction: ', '')
        text = prompt + "### Instruction: \n" + instruction.rstrip().replace('"', "") + "\n### Input: \n" + input_query
      elif line.startswith("Response"):
        if text == '':
          print(f"Something gone Wrong, bailout!")
          continue
        else:
          output = line.rstrip().replace('"', "'").replace('Response: ','')
          text += "\n### Response: \n" + output
          #print(text)
          data = [instruction, input_query, output, text]
          writer.writerow(data)
        text = ''


