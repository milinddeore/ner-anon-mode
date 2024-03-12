# -*- coding:utf8 -*-
# !/usr/bin/env python
# Written by Milind Deore <tomdeore@gmail.com>, Aug 2023

import json
from llama_cpp import Llama
from nn_logging import get_logger

nn_log = get_logger("Nonymizer Subsystem")


class LLAMAnn():
    def __init__(self, n_gpu_layers = 35, n_batch = 512):

        # Change this value based on your model and your GPU VRAM pool.
        self.n_gpu_layers = n_gpu_layers
        # n_batch has to be calculated for production server, otherwise the GPU is under utilized.
        # Example: ml.g5.2xLarger has total memory = 23G
        self.n_batch = n_batch

        # Make sure the model path is correct for your system!
        self.llm = Llama(
            model_path="nonymus-7b-q8_0-v0.1.gguf",
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            verbose=True,
            n_ctx=2048              # As you add more examples this should increase too.
        )
        nn_log.info("Model loaded successfully, ready to go!!!")

        # Make sure the model path is correct for your system!
        self.llm_syn = Llama(
            model_path="nonymus_llm.bin",
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            verbose=True,
            n_ctx=2048              # As you add more examples this should increase too.
        )
        nn_log.info("Model loaded successfully, ready to go!!!")


    def ner_inference(self, txt):

        prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

        ### Instruction:

        Find the Named Entity Recongnition for a given input and return the output, for the following classes: PERSON, PERSON, LOCATION, PHONE, ACCOUNT_NUMBER, ID, EMAIL, URL, AGE, COMPANY, JOB_TITLE, GENDER, ADDRESS, COUNTY, IP_ADDRESS, CREDIT_CARD_NUMBER, USERNAME, PASSWORD, PIN. Output should be in JSON format only. Do not include any other text.

        ### Input:
        {}

        ### Response: [""".strip()

        output = self.llm(
                prompt.format(txt),
                #max_token=256,
                stop=["]", "\n"],
                echo=False,
                temperature=0.2,
        )
        nn_log.debug(f"OUTPUT: {output}")
        data = json.loads("[" + output["choices"][0]["text"].replace("'", "\"") + "]")

        for ent in data:
            txt = txt.replace(ent['text'], '[' + ent['entity'] + ']')

        return txt


    def synthetic_inference(self, text):

        prompt = """Find the realted synthetic text for a given Named Entity Recognition input and return the output, for the following classes: PERSON, PERSON, LOCATION, PHONE, ACCOUNT_NUMBER, ID, EMAIL, URL, AGE, COMPANY, JOB_TITLE, GENDER, ADDRESS, COUNTY, IP_ADDRESS, CREDIT_CARD_NUMBER, USERNAME, PASSWORD, PIN. The synthetic data should be in context with the text. Output should be in JSON format only. Here are some examples:
        USER: The conference call is scheduled for [TIME].
        ASSISTANT: The conference call is scheduled for 1.45 PM.

        USER: [PERSON_1], [PERSON_2] and [PERSON_3] went for vacations to [LOCATION].
        ASSISTANT: Amit, John, and Emily went for vacations to Japan.

        USER: Yesturday, [PERSON] visited the [LOCATION] at [TIME].
        ASSISTANT: Yesturday, Mohan visited the Italy at 1.00am.

        USER: [PERSON]'s phone number is [PHONE].
        ASSISTANT: Ram's phone number is +1 (555) 123-4567.

        USER: Send me mail on [EMAIL] or reach out to [URL].
        ASSISTANT: Send me mail on amitgupta@gmail.com or reach out to https://nonym.us.

        USER: [PERSON_1] and [PERSON_2] both got COVID vaccine.
        ASSISTANT: Ram and Amit both got COVID vaccine.

        USER: {}
        ASSISTANT:
        """.strip()

        output = self.llm_syn(
                prompt.format(text),
                #max_token=256,
                #stop=["}", "\n"],
                echo=False,
                temperature=0.2,
        )


        print("\n")
        print(output)
        print("\n")
        data = output["choices"][0]["text"]
        return data


