from sqlalchemy.orm import Session
from . import models 

def get_predictions(db: Session, time: int):
    return db.query(models.Prediction)\
        .with_entities(models.Prediction.fixed_acidity,
                       models.Prediction.volatile_acidity,
                       models.Prediction.citric_acid,
                       models.Prediction.sulfur_dioxide,
                       models.Prediction.pH,
                       models.Prediction.alcohol)\
        .filter(models.Prediction.heure >= time).all()

def get_data_between_time(db: Session, from_date: int, to_date: int):
    return db.query(models.Prediction)\
        .with_entities(models.Prediction.fixed_acidity,
                       models.Prediction.volatile_acidity,
                       models.Prediction.citric_acid,
                       models.Prediction.sulfur_dioxide,
                       models.Prediction.pH,
                       models.Prediction.alcohol,
                       models.Prediction.quality,
                       models.Prediction.heure)\
        .filter(models.Prediction.heure >= from_date, models.Prediction.heure <= to_date).all()