from ultralytics import YOLO
from PIL import Image
import numpy as np
import time
from config_app.config import get_config
import base64
from io import BytesIO
from PIL import Image

config_app = get_config()
# Load a model
def yolov8_predictor(image_base64,threshold = 0.85):
    t0 = time.time()
    # Giải mã dữ liệu base64
    image_content = base64.b64decode(image_base64)
    # Chuyển dữ liệu thành ảnh PIL
    image_pil = Image.open(BytesIO(image_content))

    model = YOLO(config_app['yolo_params']['weight_path'])  # load a custom model

    results = model(image_pil,verbose=False)
    if float(results[0].probs.top1conf) <= threshold:
        return 0
    # print('yolov8 check:',results[0].probs)

    print('yolov8_predictor time: ',time.time() - t0)
    return config_app['yolo_params']['classes'][results[0].probs.top1]


