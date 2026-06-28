import cv2
import numpy as np
import pandas as pd
import matplotlib
import albumentations as A
from ultralytics import YOLO
import fastapi
import uvicorn

print("All libraries installed successfully!")
print("OpenCV Version:", cv2.__version__)
print("NumPy Version:", np.__version__)
print("Pandas Version:", pd.__version__)
print("Matplotlib Version:", matplotlib.__version__)
print("Albumentations Version:", A.__version__)
print("FastAPI Version:", fastapi.__version__)