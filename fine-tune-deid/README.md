# fine-tune-deid
Dataset is collected using GPT3.5 prompt engineering. You can experiement with different prompts but following is one such example: 

```
Generate 30 examples of Named Entity Recognition input and output, for the following classes : PERSON, PERSON, LOCATION, PHONE, ACCOUNT_NUMBER, ID, EMAIL, URL, AGE, COMPANY, JOB_TITLE, GENDER, ADDRESS, COUNTY, IP_ADDRESS, CREDIT_CARD_NUMBER, USERNAME, PASSWORD, PIN. Use the following format (fill in everything in between angled brackets). Do not include any other text. The data should be form region India. The data should be in english language. If there are multiple entities of same type, classify them as <entity>_<number>. Use different Indian names.

USER:<sentence>
ASSISTANT:[{“entity":<entity>_<number>,"text":<text>},{“entity":<entity>_<number>,"text":<text>}]
===
```
