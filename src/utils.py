import pickle
from src.logger import logging
from src.exception import Custom_Exception
import os,sys
from sklearn.metrics import accuracy_score,precision_recall_curve,f1_score,precision_score,recall_score
from sklearn.model_selection import GridSearchCV
def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise Custom_Exception(e.sys)
    
def evaluate_model(X_train,Y_train,X_test,Y_test,models,params):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=params[list(models.keys())[i]]
            
            GS=GridSearchCV(model,para,cv=5)
            GS.fit(X_train,Y_train)

            model.set_params(**GS.best_params_)
            model.fit(X_train,Y_train)
            y_pred=model.predict(X_test)
            test_model_accuracy=accuracy_score(Y_test,y_pred)
            report[list(models.values())[i]]=test_model_accuracy

            return report

        
    except Exception as e:
        raise Custom_Exception(e,sys)
    
def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj)
        
    except Exception as e:
        raise Custom_Exception(e,sys)