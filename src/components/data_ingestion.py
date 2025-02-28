import os
import sys
import pandas as pd


from src.logger import logging
from sklearn.model_selection import train_test_split
from dataclasses import dataclass



@dataclass
class DataIngestionConfig:

    train_data_path : str = os.path.join('artifacts','train.csv')
    # training data will be saved in artifacts folder with file name train.csv in string format
    test_data_path : str = os.path.join('artifacts', 'test.csv')
    # testing data will be saved in artifacts folder with file name test.csv in string format
    raw_data_path : str = os.path.join('artifacts', 'data.csv')
    # Original data will be saved in artifacts folder with file name data.csv in str format

    
class DataIngestion:

    def __init__(self):
        self.ingestion_config=DataIngestionConfig

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        
        
        try:
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            # creating path for storing training data and os.path.dirname extracts the directory name if the directory already exists no error occurs

            df.to_csv(self.ingestion_config.raw_data_path,index=True,header=True)
            # converting the original file from df to csv format and saving in raw data path with header and index as true

            logging.info("train test split initiated")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            # Segregating training set and testing set

            train_set.to_csv(self.ingestion_config.train_data_path,index=False, header= True)
            # converting the training file from df to csv format and saving in train data path with header as true and index as false
            
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            # converting the testing file from df to csv format and saving in test data path with header as false and index as true
            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
                # we need further use of these data so we are returning
            )
        except Exception as e:
            from src.exception import CustomException # moved into function beacuse import outside giving circular import error
            raise CustomException(e,sys)
        

if __name__ == '__main__':
    obj = DataIngestion()
    obj.initiate_data_ingestion()