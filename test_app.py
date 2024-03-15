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
from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
import openpyxl

config_app = get_config()

if not os.path.exists("./logs"):
    os.makedirs("./logs")
file_name = './logs/logs'
log_obj = Logger_Days(file_name)

app = FastAPI()

class InputData(BaseModel):
    InputText: str
    IdRequest: str
    NameBot: str
    User: str

numberrequest = 0
@app.post('/llm')
async def post(data: InputData, request: Request = None):
    global numberrequest
    numberrequest = numberrequest + 1
    print("numberrequest", numberrequest)
    
    results = {
    "products" : [],
    "terms" : [],
    "content" : "",
    "status" : 200,
    "message": ""
    }
    print(results)
    log_obj.info("-------------------------NEW_SESSION----------------------------------")
    log_obj.info("GuildID  = :" + " " + str(data.IdRequest)) 
    log_obj.info("User  = :" + " " + str(data.User))
    log_obj.info("NameBot  = :" + " " + str(data.NameBot))
    log_obj.info("InputText:" + " " + str(data.InputText)) # cau hoi
    log_obj.info("IP_Client: " +str(request.client.host))
    log_obj.info("NumberRequest: " +str(numberrequest))
    result = predict_llm(data.InputText, data.IdRequest, data.NameBot, data.User, log_obj)

    results["content"] = result

    dataframe = openpyxl.load_workbook("./data/product_info.xlsx")
    wb = dataframe.active
    for row in range(1, wb.max_row):
        x = wb[row+1][3].value
        if wb[row+1][3].value != None and wb[row+1][3].value in result:
            product =  {
                "code" : "",
                "name" : "",
                "link" : ""
            }
            product['code'] = wb[row+1][2].value
            product['name'] = wb[row+1][3].value
            product['link'] = wb[row+1][10].value
            results["products"].append(product)
    return results

uvicorn.run(app, host=config_app['server']['ip_address'], port=8003)

# str(User) + "/" + str(NameBot) + "/" + str(IdRequest)