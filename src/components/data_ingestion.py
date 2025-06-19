import os,sys
import pandas as pd
import numpy as nd
from src.logger import logging
from src.exception import Custom_Exception
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from src.components.data_transformation import DataTransformation
@dataclass
class DataIngestionConfig:
    train_data_path=os.path.join("artifacts","data_ingestion","train.csv")
    test_data_path=os.path.join("artifacts","data_ingestion","test.csv")
    raw_data_path=os.path.join("artifacts","data_ingestion","raw.csv")

#notebook\data\income.csv
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("data ingestion started")
        try:
            data=pd.read_csv(os.path.join("notebook","data","clean_data.csv"))
            logging.info("data reading from csv file")
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False)

            train_set,test_set=train_test_split(data,test_size=0.3,random_state=1)
            logging.info("data splitting completed into train and test")
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            train_set.to_csv()
            logging.info("data Ingestion completed")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.info("Error occured in data ingestion stage")
            raise Custom_Exception(e,sys)

if __name__=="__main__":
    obj=DataIngestion()
    train_data_path,test_data_path=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.inititaite_data_transformation(train_data_path,test_data_path)