import numpy as np
import pandas as pd
import sys
import os
from heart.exception import HeartException
from heart.logger import logging
from heart.config import mongo_client
import yaml
import dill


def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    
    try:
        
        logging.info(f"Reading Data from Database : {database_name} and Collection : {collection_name}")
        df = pd.DataFrame(mongo_client[database_name][collection_name].find())
        logging.info(f"Find Columns : {df.columns}")
        if "_id" in df.columns:
            df = df.drop("_id", axis=1)
        if "Unnamed: 0" in df.columns:
            df = df.drop("Unnamed: 0", axis=1)
            
        logging.info(f"Rows and Columns in DataFrame : {df.shape}")
        logging.info(f"Find Columns : {df.columns}")
        return df
        
    except Exception as e:
        raise HeartException(e, sys)



# Data_Validation

# def convert_columns_float(df:pd.DataFrame, exclude_columns:list)->pd.DataFrame:
    
#     try:
        
#         for column in df.columns:
#             if column not in df.exclude_columns:
#                 if df[column].dtypes != 'O':
#                     df[column] = df[column].astype('float')
            
#         return df

#     except Exception as e:
#         raise HeartException(e, sys)



# def write_yaml_file(file_path,data:dict):
#     try:
#         file_dir = os.path.dirname(file_path)
#         os.makedirs(file_dir,exist_ok=True)
#         with open(file_path,"w") as file_writer:
#             yaml.dump(data,file_writer)
#     except Exception as e:
#         raise HeartException(e, sys)


def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise HeartException(e, sys)

def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtypes != 'O':
                    df[column]=df[column].astype('float')
        return df
    except Exception as e:
        raise e