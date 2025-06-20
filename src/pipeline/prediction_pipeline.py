#create prediction pipeline class 
# def function for loading an object
# create custom class based on data set
# create a function to convert data into dataframe with help of dictionary

import os,sys
from src.logger import logging
from src.exception import Custom_Exception
import numpy as np
import pandas as pd
from dataclasses import dataclass
from src.utils import load_object
class PredictionPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        preprocessor_path=os.path.join("artifacts","data_transformation","preprocessor.pkl")
        model_path=os.path.join("artifact","model_trainer","model.pkl")

        processor=load_object(preprocessor_path)
        model=load_object(model_path)

        scaled =processor.transform(features)
        pred=model.predict(scaled)
        
        return pred


class CustomClass:
    def __init__(self,age:int,	workclass:int,	educational_num:int,	marital_status:int,	occupation:int,	relationship:int,	race:int,	gender:int,	capital_gain:int,	capital_loss:int,	hours_per_week:int,	native_country:int):
        self.age=age
        self.workclass=workclass
        self.educational_num=educational_num
        self.marital_status=marital_status
        self.occupation=occupation
        self.relationship=relationship
        self.race=race
        self.gender=gender
        self.capital_gain=capital_gain
        self.capital_loss=capital_loss
        self.hours_per_week=hours_per_week
        self.native_country=native_country
    

    def get_data_DataFrame(self):
        try:
            custom_input={"age":[self.age],
                          "workclass":[self.workclass],
                          "educational-num":[self.educational_num],
                          "marital-status":[self.marital_status],
                          "occupation":[self.occupation],
                          "relationship":[self.relationship],
                          "race":[self.race],
                          "gender":[self.gender],
                          "capital-gain":[self.capital_gain],
                          "capital-loss":[self.capital_loss],
                          "hours-per-week":[self.hours_per_week],
                          "native-country":[self.native_country]
                          }
            data=pd.DataFrame(custom_input)

            return data
        except Exception as e:
            raise Custom_Exception(e,sys)

