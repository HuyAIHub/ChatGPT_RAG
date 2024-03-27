from typing import List
from fastapi import FastAPI, Request
import uvicorn
import os
import time
from fastapi import FastAPI, Request, File, UploadFile
from module.predict import predict_llm
from config_app.config import get_config
from utils.logging import Logger_Days
from fastapi import FastAPI, Request
from pydantic import BaseModel
from module.search_product import product_seeking ,get_products_by_group
from module.yolov8_prediction import yolov8_predictor

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
    image: str

numberrequest = 0
@app.post('/llm')
async def post(data: InputData, request: Request = None):
    start_time = time.time()
    global numberrequest
    numberrequest = numberrequest + 1
    print("numberrequest", numberrequest)
    
    results = {
    "products" : [],
    "terms" : [],
    "content" : "",
    "status" : 200,
    "message": "",
    "time_processing":''
    }
    log_obj.info("-------------------------NEW_SESSION----------------------------------")
    log_obj.info("GuildID  = :" + " " + str(data.IdRequest)) 
    log_obj.info("User  = :" + " " + str(data.User))
    log_obj.info("NameBot  = :" + " " + str(data.NameBot))
    log_obj.info("InputText:" + " " + str(data.InputText)) # cau hoi
    log_obj.info("IP_Client: " + str(request.client.host))
    log_obj.info("NumberRequest: " + str(numberrequest))

    if data.image:
        #phan loai theo hinh anh
        text1 = "Sản phẩm bạn đang quan tâm là {}? Một số thông tin về sản phẩm bạn đang quan tâm:\n{}"
        text2 = "Hiện tôi không có thông tin về sản phẩm bạn đang quan tâm."

        out_put = yolov8_predictor(data.image)
        if out_put != 0:
            quantity, products = get_products_by_group(results,out_put)
            result_string = f"Số lượng sản phẩm: {quantity}\n"
            for index, (code, name,link) in enumerate(products, start=1):
                result_string += f"{index}. {code}: {name}\n"
            results["content"] = text1.format(out_put,result_string)
        else:
            results["content"] = text2
    else:
        # predict llm
        result = predict_llm(data.InputText, data.IdRequest, data.NameBot, data.User, log_obj)
        log_obj.info("Answer: " + str(result))

        results["content"] = result
        # tim san pham
        results = product_seeking(results = results, texts=result)
    results['time_processing'] = str(time.time() - start_time)
    # print(results)
    return results

uvicorn.run(app, host=config_app['server']['ip_address'], port=int(config_app['server']['port']))