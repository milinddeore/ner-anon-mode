# -*- coding:utf8 -*-
# !/usr/bin/env python
# Written by Milind Deore <tomdeore@gmail.com>, Aug 2023

from nonymizer import LLAMAnn
from fastapi import FastAPI, Form, Request, status, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from typing import Union
import uvicorn
import os
import aiofiles
import json
from nn_logging import get_logger

app = FastAPI()
nn_log = get_logger("nonymus REST APIs")
nn_log.info("nonymus application started!!!")

# Bootstrap the model.
nonymizer = LLAMAnn()

@app.get("/")
async def root():
    return {"message": "Welcome to nonymus container service"}


@app.post('/anon_str')
async def anon_a_string(text: str = Form(...)):
    """This endpoint accepts string(s), based on the context size currently its limited to 2K.
    and returns a string with embedded NER entities in it.
    """
    response = nonymizer.ner_inference(text)
    nn_log.info(f'NER output: {response}')
    return json.dumps(response)


@app.get('/substitute_str')
async def substitute_a_string(text: str):
    """This endpoint accepts string(s), based on the context size currently its limited to 2K.
    and returns a string substitute string back.
    """
    response = nonymizer.synthetic_inference(text)
    nn_log.info(f'Substitute output: {response}')
    return response


@app.post('/anon_subs_str')
async def anon_subs_a_string(text: str):
    """This endpoint accepts string(s), based on the context size currently its limited to 2K.
    and returns a string with anon + substitution.
    """
    ner = nonymizer.ner_inference(text)
    response = nonymizer.synthetic_inference(ner)
    nn_log.info(f'Substitute output: {response}')
    return response


@app.post('/anonfile')
async def anon_a_file(text: str, file: Union[UploadFile, None] = None):
    """This endpoint accepts a file. The max size of the file is restricted to 512*1k=512MB
    and returns a string with embedded NER entities in it.
    """

    if not file:
        nn_log.error('file not found')
        return {"message": "No upload file sent"}
    else:
        print(f'Current directory path: {os.path.dirname(os.path.realpath(__file__))}')
        """
        async with aiofiles.open(file.filename, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write

        print(f'file {file.filename} received on python side. Content-type {file.content_type}')
        anonmode.anon_mode(file.filename, "anon_" + file.filename)
        os.remove(file.filename)
        """
        return "Not implemented yet."


