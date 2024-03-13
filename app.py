from typing import Callable, List
from fastapi import FastAPI, Request, Response, HTTPException, Form, File, UploadFile
from fastapi.routing import APIRoute
from fastapi.exceptions import FastAPIError
from fastapi.responses import JSONResponse
import uvicorn
from io import BytesIO
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import os
import time
import traceback
import torch
import ast
from predict import predict_llm
from config_app.config import get_config
from utils.logging import Logger_Days, Logger_maxBytes
from fastapi.middleware.cors import CORSMiddleware

config_app = get_config()

if not os.path.exists("./logs"):
    os.makedirs("./logs")
file_name = './logs/logs'
log_obj = Logger_Days(file_name)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

numberrequest = 0
@app.post('/llm')
async def post(InputText: str = Form(...), IdRequest: str = Form(...), NameBot: str = Form(...), User: str = Form(...), request: Request = None):
    global numberrequest
    numberrequest = numberrequest + 1
    print("numberrequest", numberrequest)
    log_obj.info("-------------------------NEW_SESSION----------------------------------")
    log_obj.info("GuildID  = :" + " " + str(IdRequest)) 
    log_obj.info("User  = :" + " " + str(User))
    log_obj.info("NameBot  = :" + " " + str(NameBot))
    log_obj.info("InputText:" + " " + str(InputText)) # cau hoi
    log_obj.info("IP_Client: " +str(request.client.host))
    log_obj.info("NumberRequest: " +str(numberrequest))
    result = predict_llm(InputText, IdRequest, NameBot, User, log_obj)
    return result

uvicorn.run(app, host=config_app['server']['ip_address'], port=int(config_app['server']['port']))