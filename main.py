from heart.logger import logging
from heart.exception import HeartException
import os
import sys
from heart.utils import get_collection_as_dataframe
from heart.entity.config_entity import DataIngestionConfig
from heart.entity import config_entity
from heart.components.data_ingestion import DataIngestion










if __name__ == '__main__':
    try:
        get_collection_as_dataframe(database_name = "HEART" , collection_name = "HEART_PROJECT" )
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config = training_pipeline_config)
        print(data_ingestion_config.to_dict())
        
        # data_ingestion
        
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
    except Exception as e:
        print(e)