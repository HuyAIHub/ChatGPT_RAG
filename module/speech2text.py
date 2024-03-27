
from transformers  import pipeline
import time

transcriber = pipeline("automatic-speech-recognition", model = "vinai/PhoWhisper-small", device = "cpu")

def speech_2_text(path_audio):
    t0 = time.time()
    text = transcriber(path_audio)["text"]
    print('speech_2_text time: ',time.time() - t0)
    return text
    