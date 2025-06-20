# handle missing values
# outliers
# handle immbalanced dataset
#convert categorical to numerical data

import os ,sys
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from src.logger import logging
from src.exception import Custom_Exception
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from src.utils import save_object
@dataclass
class DataTransformationConfig():
    preprocessor_obj_file_path=os.path.join("artifacts","data_transformation","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.daata_transformation_config=DataTransformationConfig()

    def get_data_transformation_obj(self):
        try:
            logging.info("Data Transformation started ")
            numerical_features=['age', 'workclass', 'educational-num', 'marital-status', 'occupation',
       'relationship', 'race', 'gender', 'capital-gain', 'capital-loss',
       'hours-per-week']
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                
                ]
            )
            preprocessor=ColumnTransformer([
                ("num_pipeline",num_pipeline,numerical_features)
            ])
            return preprocessor
            
        except Exception as e:
            raise Custom_Exception(e,sys)
    def remove_outliers_IOR(self,col,df):
        try:
            Q1=df[col].quantile(0.25)
            Q3=df[col].quantile(0.75)

            iqr=Q3-Q1
            upper_limit=Q3+1.5*iqr
            lower_limit=Q1-1.5*iqr

            df.loc[(df[col]>upper_limit),col]=upper_limit
            df.loc[(df[col]<lower_limit),col]=lower_limit
            return df

        except Exception as e:
            logging.info("outliers handing code ")
            raise Custom_Exception(e,sys)
        
    def inititaite_data_transformation(self,train_path,test_path):

        try:
            train_data=pd.read_csv(train_path)
            test_data=pd.read_csv(test_path)

            numerical_features=['age', 'workclass', 'educational-num', 'marital-status', 'occupation',
       'relationship', 'race', 'gender', 'capital-gain', 'capital-loss',
       'hours-per-week']
            
            for i in numerical_features:
                self.remove_outliers_IOR(col=i,df=train_data)

            logging.info("outliers capped on our train data ")


            for i in numerical_features:
                self.remove_outliers_IOR(col=i,df=test_data)  
            logging.info("outliers capped on our test data ")

            preprocess_obj=self.get_data_transformation_obj()
            target_column="income"
            drop_column=[target_column]

            # splitting the data 
            logging.info("splitting the train data into dependent and independent")
            input_feature_train_data=train_data.drop(drop_column,axis=1)
            target_feature_train_data=train_data[target_column]

            logging.info("splitting the test data into dependent and independent")
            input_feature_test_data=test_data.drop(drop_column,axis=1)
            target_feature_test_data=test_data[target_column]
            
            #apply transformation on train and test data 
            input_train_arr=preprocess_obj.fit_transform(input_feature_train_data)
            input_test_arr=preprocess_obj.transform(input_feature_test_data)

            #apply preprocessor object  on train and test data 
            train_arr=np.c_[input_train_arr,np.array(target_feature_train_data)]
            test_arr=np.c_[input_test_arr,np.array(target_feature_test_data)]

            save_object(file_path=self.daata_transformation_config.preprocessor_obj_file_path
                        ,obj=preprocess_obj)
            return (train_arr,test_arr,self.daata_transformation_config.preprocessor_obj_file_path)
        except Exception as e:
            raise Custom_Exception(e,sys)
        
        