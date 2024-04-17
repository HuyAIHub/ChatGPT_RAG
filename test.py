from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

class OCRRequest(BaseModel):
    id_request: str
    type_request: Optional[str] = None

@app.post("/check_face",response_class=HTMLResponse)
def check_face(data: OCRRequest):
    print(data.id_request)
    print(data.type_request)
    results = {
    "code": 0,
    "message": "",
    }
    score_face = 0.9
    try:
        if data.type_request == 'km_m':
            print('km_m')
        elif data.type_request == 'km_l':
            print('km_l')
        elif data.type_request == 'km_p':
            print('km_p')
        else:
            print('-----Verify Face------')
            
        
    except BaseException as error:
        print("Base error !", error)
        results = {
            "code": 400,
            "message": "Không lấy được ảnh!"
        }
        return JSONResponse(results)

if __name__ == '__main__':
    uvicorn.run(app,host = "0.0.0.0",port = 8017)


