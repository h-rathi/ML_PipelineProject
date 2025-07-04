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
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from src.utils import evaluate_model
@dataclass
class ModelTrainerConfig:
    train_model_file_path=os.path.join("artifact","model_trainer","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            X_train,Y_train,X_test,Y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model={
                "Random Forest":RandomForestClassifier(),
                "Decision Tree":DecisionTreeClassifier(),
                "Logistic Regression":LogisticRegression()
            }
            params={
                "Random Forest":{

                    "class_weight":["balanced"],
                    'n_estimators': [20, 50, 30],
                    'max_depth': [10, 8, 5],
                    'min_samples_split': [2, 5, 10],
}
,
                "Decision Tree":{
                    "class_weight":["balanced"],
                    "criterion":['gini',"entropy","log_loss"],
                    "splitter": ['best','random'],
                    "max_depth":[3,4,5,6],
                    "min_samples_split": [2,3,4,5],
                    "min_samples_leaf":[1,2,3],
                    "max_features": ["auto","sqrt","log2"]
},
                "Logistic Regression":{
                    "class_weight": ["balanced"],
                    'penalty': ['11','12'],
                    'C':[0.001, 0.01, 0.1,1,10,100],
                    'solver': ['liblinear', 'saga' ]
}
            
            }
            
            model_report:dict=evaluate_model(X_train=X_train,Y_train=Y_train,X_test=X_test,Y_test=Y_test,models=model,params=params)
            best_model_score=max(sorted(model_report.values()))
            
            best_model_name=list(model.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model=model[best_model_name]
            logging.info(f"best model found :{best_model_name}, accuracy score :{best_model_score}")
            save_object(file_path=self.model_trainer_config.train_model_file_path,
                        obj=best_model
                        )
                                 
            


        except Exception as e:
            raise Custom_Exception(e,sys)