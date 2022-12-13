from . import crud, models
from .database import SessionLocal, engine
import pandas as pd

models.Base.metadata.create_all(bind=engine)

class ManagerPostgres:    
    def __init__(self):
        self.db = SessionLocal()
        self.columns = ["fixed acidity", "volatile acidity",
                        "citric acid", "total sulfur dioxide",
                        "pH", "alcohol"]
        
    def get_prediction(self, time: int):
        predictions = crud.get_predictions(self.db, time)
        return pd.DataFrame(predictions, columns=self.columns)
    
    def get_data_between_time(self, from_date: int, to_date: int):
        data = crud.get_data_between_time(self.db, from_date, to_date)
        return pd.DataFrame(data, columns=self.columns + ["quality", "time"])
        
    def close(self):
        self.db.close()