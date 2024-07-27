import os
import pandas as pd
import numpy as np
from src.DimondPricePrediction.logger import logging
from src.DimondPricePrediction.logger import customexception

from sklearn.model_selection import train_test_split
from dataclasses import dataclasses
from pathlib import Path

class DataIngestionConfig:
    raw_data_path:str = os.path.join("artifacts","raw.csv")
    train_data_path:str = os.path.join("artifacts","train.csv")
    test_data_path:str = os.path.join("artifacts","test.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()


    def initiate_data_ingestion(self):
        logging.info("data ingestion started")

        try:
            data = pd.read_csv(Path(os.path.join("notebook/data","cubic_zirconia.csv")))
            logging.info("i have read dataset as a df")

            os.mkdir(os.path.join(self.ingestion_config.raw_data_path),exists = True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False)

            train_data,test_data = train_test_split(data,test_size=0.25)
            logging.info("train test split completed")


            
        except Exception as e:
            pass