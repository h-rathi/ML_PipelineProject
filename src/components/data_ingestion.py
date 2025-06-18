import os,sys
import pandas as pd
import numpy as nd
from src.logger import logging
from src.exception import Custom_Exception
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    train_data_path=os.path.join("artifacts","train.csv")
    test_data_path=os.path.join("artifacts","test.csv")
    raw_data_path=os.path.join("artifacts","raw.csv")

#notebook\data\income.csv
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("data ingestion started")
        try:
            data=pd.read_csv(os.path.join("notebook","data","income.csv"))
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
    obj.initiate_data_ingestion()