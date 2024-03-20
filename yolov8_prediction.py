from ultralytics import YOLO
from PIL import Image
import numpy as np
import os
from config_app.config import get_config

config_app = get_config()
# Load a model
def yolov8_predictor(path,threshold = 0.85):
    model = YOLO(config_app['yolo_params']['weight_path'])  # load a custom model

    results = model(path,verbose=False)
    if float(results[0].probs.top1conf) <= threshold:
        return 0
    print('yolov8 check:',results[0].probs)
    return config_app['yolo_params']['classes'][results[0].probs.top1]


