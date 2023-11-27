import re
import joblib
import json
import logging
import os
import sys
import urllib
from datetime import datetime
from pathlib import Path
from typing import (
    Dict,
    List,
)
import scripts.predict as predict

import requests
from fastapi import FastAPI, Response, Header, UploadFile, File
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from starlette_prometheus import (
    PrometheusMiddleware,
    metrics,
)

import numpy as np
import pandas as pd

app = FastAPI(title="digital_proryv")
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)


api_version = "1.0"
model_version = "1.0"
model_desc = "digital_proryv"
data_path = "data"


@app.get("/health_check")
def health_check():
    data = """{
  "status": "Healthy"
}"""
    return Response(content=data, media_type="application/json")

@app.post("/uploadfile/")
def create_upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"/app/data/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    prediction = predict.predict(file_location)
    
    #delete file
    myfile = "/tmp/foo.txt"
    # If file exists, delete it.
    if os.path.isfile(file_location):
        os.remove(file_location)
        print("Succes: %s file deleted" % file_location)
    else:
        # If it fails, inform the user.
        print("Error: %s file not found" % file_location)

    return {"info": f"file '{uploaded_file.filename}' ",
            "prediction": prediction}