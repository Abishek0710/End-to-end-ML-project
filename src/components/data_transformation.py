import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')
    # setting up a path for pkl file with file name as preprocessor.pkl


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    # Here we will create pipeline and column transformer
    # Pipeline will define the steps
    # with Column transformer we can pass imputs to follow the steps
    def get_transformer_object(self):

        """"
        Performing Data Transformations like 
        Handling missing values,
        One hot encoding (categorical to numerical)
        Standardization
        """

        try:
            numerical_features = ['writing_score','reading_score']

            categorical_features = [
                'gender',
                'race_ethnicity', 
                'parental_level_of_education', 
                'lunch', 
                'test_preparation_course',
            ]
            
            # Steps to be passed on for numerical features
            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')), 
                    #Simple imputer used to Handling missing values median is used to replace missing values since data have outliers
                    
                    ('scaler',StandardScaler())
                    # Standardization of numerical Data
                ]
            )

            # Steps to be passed on for categorical features
            cat_pipeline = Pipeline(
                                    
                steps= [
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    # For handling issing values

                    ('one_hot_encoder',OneHotEncoder()),
                    # For changing categorical to numerical value
                    # Since we have less categories in features we are using one hot encoding

                    ('scaler',StandardScaler(with_mean=False))
                    # Standardization of all the data
                ]
            )

            logging.info("Numerical Columns standard scaling Completed")
            logging.info("Categorical column encoding completed")


            preprocessor = ColumnTransformer(
                [
                ('num_pipeline', num_pipeline, numerical_features ),
                # this composes numerical features with the numerical pipeline
                ('cat_pipeline', cat_pipeline, categorical_features)
                # this composes categorical features with the categorical pipeline

                ]
            )

            return preprocessor
        

        except Exception as e:
            raise CustomException(e,sys)
        
            
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading train and test data completed")

            logging.info("Obtaining Preprocessor Onject")

            preprocessor_obj = self.get_transformer_object()

            target_column_name = 'math_score'
            numerical_columns = ['writing_score','reading_score']


            #train test split
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            # creating X_train
            target_feature_train_df = train_df[target_column_name]
            # creating y train

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            # creating X_test
            target_feature_test_df = test_df[target_column_name]
            # creating y test

            logging.info('Applying Preprocessor object on training and testing Dataframe')

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df) ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df) ]

            logging.info('Saved Preprocessing Object...')


            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )
            # Saving into the created pickle file 

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e,sys)
