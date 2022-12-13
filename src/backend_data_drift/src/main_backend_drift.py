from data_drift import DataDriftManager
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pandas as pd
from typing import List

TRANING_DATA = "/data/training/wine.pkl"
DRIFTING = "/data/drift/drifting_wine.csv"

class Item(BaseModel):
    data: List 

data_drift = DataDriftManager(DRIFTING, TRANING_DATA)
sched = BackgroundScheduler()

sched.add_job(data_drift.check, 'interval', minutes=60)
sched.start()

app = FastAPI()

@app.get("/drift")
async def response():
   try:
      data = pd.read_csv(DRIFTING).to_json()
      return {
         "status": 1,
         "message": "",
         "data": data
      }
   except Exception as _:
        return {
            "status": 0,
            "message": "Data Drift Internal Error",
            "data": None
        }

@app.get("/forcedirft")
async def response_force():
   try:
      data_drift.check()
      data = pd.read_csv(DRIFTING).to_json()
      return {
         "status": 1,
         "message": "",
         "data": data
      }
   except Exception as _:
        return {
            "status": 0,
            "message": "Data Drift Internal Error",
            "data": None
        }
        
@app.post("/downloader")
async def data_dowloader(value: Item):
   try:
      data = data_drift.get_data_from_sql(value.data)
      return {
         "status": 1,
         "message": "",
         "data": data.to_json()
      }
   except Exception as _:
      return {
         "status": 0,
         "message": "Data Drift Internal Error",
         "data": None
      }

if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=90) 