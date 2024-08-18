import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path
from source.DimondPricePrediction.logger import logging
from source.DimondPricePrediction.exception import customexception

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DataIngestionConfig:
    raw_data_path: str = os.path.abspath(os.path.join("artifacts", "raw.csv"))
    train_data_path: str = os.path.abspath(os.path.join("artifacts", "train.csv"))
    test_data_path: str = os.path.abspath(os.path.join("artifacts", "test.csv"))

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Data ingestion started")
        
        try:
            # Use absolute or correctly relative path
            data_file_path = r'E:\Ineuron_Project\notebooks\data\cubic_zirconia.csv'
            logging.info(f"Reading dataset from: {data_file_path}")
            
            if not os.path.isfile(data_file_path):
                logging.error(f"Data file does not exist at: {data_file_path}")
                return
            
            data = pd.read_csv(data_file_path)
            logging.info("Read dataset as a DataFrame")
            
            artifacts_dir = os.path.dirname(self.ingestion_config.raw_data_path)
            logging.info(f"Creating directory at: {artifacts_dir}")
            os.makedirs(artifacts_dir, exist_ok=True)
            
            # Verify if directory was created
            if os.path.exists(artifacts_dir):
                logging.info(f"Directory successfully created or already exists at: {artifacts_dir}")
            else:
                logging.error(f"Failed to create directory at: {artifacts_dir}")
            
            data.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info(f"Saved the raw dataset to {self.ingestion_config.raw_data_path}")
            
            logging.info("Performing train-test split")
            
            train_data, test_data = train_test_split(data, test_size=0.25)
            logging.info("Train-test split completed")
            
            train_data.to_csv(self.ingestion_config.train_data_path, index=False)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            
            logging.info("Data ingestion part completed")
            
            return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)
        
        except Exception as e:
            logging.error(f"Exception occurred during data ingestion: {e}")
            raise customexception(e, sys)

if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion.initiate_data_ingestion()
