from flask import Flask
from src.logger import logging
from src.exception import Custom_Exception
import os,sys
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    try:
        logging.info("we are testing exception handling ")
        return("welcome to the project")
    except Exception as e:
        abc=Custom_Exception(e,sys)

if __name__=="__main__":
    app.run(debug=True)