import pandas as pd
import numpy as np
import os
import sys
from heart.entity import config_entity, artifact_entity
from heart.logger import logging
from heart.exception import HeartException
from heart.entity.artifact_entity import DataIngestionArtifact
from heart.utils import get_collection_as_dataframe
from heart import utils
from sklearn.model_selection import train_test_split



class DataIngestion:
    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig):
        
        try:
            self.data_ingestion_config = data_ingestion_config
            
        except Exception as e:
            raise HeartException(e, sys)
    
    
    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        
        try:
            
            logging.info(f"Export Collection Data as Pandas DataFrame")
            
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name = self.data_ingestion_config.database_name,
                collection_name= self.data_ingestion_config.collection_name)
            
            logging.info(f"Save data in future store")
            
            # Replace Na Values into NAN Values
            df.replace(to_replace="na", value=np.NAN, inplace=True)
            
            
            # Save Data into Feature Store
            
            logging.info(f"Create feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            
            logging.info(f"Save DataFrame to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index=False, header=True)
            
            logging.info(f"Splitting Data into Train and Test")
            train_df, test_df = train_test_split(df, test_size= self.data_ingestion_config.test_size, random_state=51)
            
            
            logging.info(f"Creating Dataset Directory folder if not exits")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)
            
            
            logging.info(f"Save Dataset to feature store folder")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path, index=False, header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path, index=False, header=True)


            # prepare a artifact folder
            
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path = self.data_ingestion_config.feature_store_file_path,
                train_file_path = self.data_ingestion_config.train_file_path,
                test_file_path = self.data_ingestion_config.test_file_path)
            
            return data_ingestion_artifact
        except Exception as e:
            raise HeartException(error_message = e, error_detail = sys)            


            
            
        
        except Exception as e:
            raise HeartException(e, sys)