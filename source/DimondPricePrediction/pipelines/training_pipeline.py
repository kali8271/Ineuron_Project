from source.DimondPricePrediction.components.data_ingestion import DataIngestion
from source.DimondPricePrediction.components.data_transformation import DataTransformation
from source.DimondPricePrediction.components.model_trainer import ModelTrainer
from source.DimondPricePrediction.components.model_evaluation import ModelEvaluation
import os
import sys
from source.DimondPricePrediction.logger import logging
from source.DimondPricePrediction.exception import customexception
import pandas as pd

class TrainingPipeline:
    def start_data_ingestion(self):
        try:
            logging.info('Starting data ingestion...')
            data_ingestion = DataIngestion()
            train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
            logging.info('Data ingestion completed successfully.')
            return train_data_path, test_data_path
        except Exception as e:
            logging.error(f"Exception occurred in data ingestion: {str(e)}")
            raise customexception(e, sys)
        
    def start_data_transformation(self, train_data_path, test_data_path):
        try:
            logging.info('Starting data transformation...')
            data_transformation = DataTransformation()
            train_arr, test_arr = data_transformation.initialize_data_transformation(train_data_path, test_data_path)
            logging.info('Data transformation completed successfully.')
            return train_arr, test_arr
        except Exception as e:
            logging.error(f"Exception occurred in data transformation: {str(e)}")
            raise customexception(e, sys)
    
    def start_model_training(self, train_arr, test_arr):
        try:
            logging.info('Starting model training...')
            model_trainer = ModelTrainer()
            model_trainer.initate_model_training(train_arr, test_arr)
            logging.info('Model training completed successfully.')
        except Exception as e:
            logging.error(f"Exception occurred in model training: {str(e)}")
            raise customexception(e, sys)
                
    def start_trainig(self):
        try:
            logging.info('Starting training pipeline...')
            train_data_path, test_data_path = self.start_data_ingestion()
            train_arr, test_arr = self.start_data_transformation(train_data_path, test_data_path)
            self.start_model_training(train_arr, test_arr)
            logging.info('Training pipeline completed successfully.')
        except Exception as e:
            logging.error(f"Exception occurred in training pipeline: {str(e)}")
            raise customexception(e, sys)
