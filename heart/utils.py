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
    

#*********************************** Data_Transformation*******************************************

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise HeartException(e, sys) from e

    
def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise HeartException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise HeartException(e, sys) from e

#***********************************## Model Training*******************************************

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HeartException(e, sys) from e