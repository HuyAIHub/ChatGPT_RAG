import uvicorn
import os
import time
# from module.predict import predict_llm
from module.predict_tools import predict_llm
from config_app.config import get_config
from utils.logging import Logger_Days
from fastapi import FastAPI
from pydantic import BaseModel
from module.search_product import product_seeking ,get_products_by_group
from module.yolov8_prediction import yolov8_predictor
from module.speech2text import speech_2_text,downsampleWav
from extract_price_info import take_product
from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI, UploadFile, Form, File

config_app = get_config()

if not os.path.exists("./logs"):
    os.makedirs("./logs")
file_name = './logs/logs'
log_obj = Logger_Days(file_name)

app = FastAPI()

numberrequest = 0
@app.post('/llm')
async def post(InputText: str = Form(...),
                IdRequest: str = Form(...),
                NameBot: str = Form(...),
                User: str = Form(...),
                Image: str = Form(None),
                Voice: UploadFile = File(None)):
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
    log_obj.info("GuildID  = :" + " " + str(IdRequest)) 
    log_obj.info("User  = :" + " " + str(User))
    log_obj.info("NameBot  = :" + " " + str(NameBot))
    log_obj.info("InputText:" + " " + str(InputText)) # cau hoi
    # log_obj.info("IP_Client: " + str(request.client.host))
    log_obj.info("NumberRequest: " + str(numberrequest))

    if Voice:
        src_output = './data/test_voice/test.wav'
        with open(src_output, "wb+") as file_object:
            file_object.write(Voice.file.read())
        downsampleWav(src_output, src_output)

        out_put = speech_2_text(src_output)
        print('speech_2_text:',out_put)
        # predict llm
        result = predict_llm(out_put, IdRequest, NameBot, User, log_obj)
        print('result:',result)
        log_obj.info("Answer: " + str(result))

        results["content"] = result
        # tim san pham
        results = product_seeking(results = results, texts=result)
        print('results:',results)
    if Image:
        #phan loai theo hinh anh
        text1 = "Sản phẩm bạn đang quan tâm là {}? Một số thông tin về sản phẩm bạn đang quan tâm:\n{}"
        text2 = "Hiện tôi không có thông tin về sản phẩm bạn đang quan tâm."

        out_put = yolov8_predictor(Image)
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
        result = predict_llm(InputText, IdRequest, NameBot, User, log_obj)
        log_obj.info("Answer: " + str(result))

        results["content"] = result
        # tim san pham
        results = product_seeking(results = results, texts=result)
    results['time_processing'] = str(time.time() - start_time)
    # print(results)
    return results

uvicorn.run(app, host=config_app['server']['ip_address'], port=int(config_app['server']['port']))