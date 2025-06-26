import pandas as pd
import numpy as np
import os
import sys
from DimondPricePrediction.logger import logging
from DimondPricePrediction.exception import customexception
from dataclasses import dataclass
from DimondPricePrediction.utils.utils import save_object, evaluate_model

from sklearn.linear_model import LinearRegression, Ridge,Lasso,ElasticNet
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')
    
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initate_model_training(self,train_array,test_array):
        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            # Define column names (assuming order from CSV)
            columns = [
                'carat', 'cut', 'color', 'clarity', 'depth', 'table', 'x', 'y', 'z'
            ]
            num_features = ['carat', 'depth', 'table', 'x', 'y', 'z']
            cat_features = ['cut', 'color', 'clarity']

            X_train_df = pd.DataFrame(X_train, columns=columns)
            X_test_df = pd.DataFrame(X_test, columns=columns)

            # Preprocessing pipeline with imputation
            num_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])
            cat_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder(handle_unknown='ignore'))
            ])
            preprocessor = ColumnTransformer([
                ('num', num_pipeline, num_features),
                ('cat', cat_pipeline, cat_features)
            ])

            preprocessor.fit(X_train_df)
            X_train_processed = preprocessor.transform(X_train_df)
            X_test_processed = preprocessor.transform(X_test_df)

            # Save the preprocessor
            save_object(
                file_path=os.path.join('artifacts','preprocessor.pkl'),
                obj=preprocessor
            )

            models={
            'LinearRegression':LinearRegression(),
            'Lasso':Lasso(),
            'Ridge':Ridge(),
            'Elasticnet':ElasticNet()
        }
            model_report:dict=evaluate_model(X_train_processed,y_train,X_test_processed,y_test,models)
            print(model_report)
            print('\n====================================================================================\n')
            logging.info(f'Model Report : {model_report}')

            # To get best model score from dictionary 
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[\
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]

            print(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')

            save_object(
                 file_path=self.model_trainer_config.trained_model_file_path,
                 obj=best_model
            )
          

        except Exception as e:
            logging.info('Exception occured at Model Training')
            raise customexception(e,sys)

        
    