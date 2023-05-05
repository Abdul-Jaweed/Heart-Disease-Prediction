from heart.logger import logging
from heart.exception import HeartException
import os
import sys
from heart.utils import get_collection_as_dataframe
from heart.entity.config_entity import DataIngestionConfig
from heart.entity import config_entity
from heart.components.data_ingestion import DataIngestion
from heart.components.data_validation import DataValidation
from heart.components.data_transformation import DataTransformation
from heart.components.model_trainer import ModelTrainer










if __name__ == '__main__':
    try:
        get_collection_as_dataframe(database_name = "HEART" , collection_name = "HEART_PROJECT" )
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config = training_pipeline_config)
        print(data_ingestion_config.to_dict())
        
        # data_ingestion
        
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
        
        #data validation
        
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                        data_ingestion_artifact=data_ingestion_artifact)
        
        data_validation_artifact = data_validation.initiate_data_ingestion()
        
        
        
        # data transformations
        
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        
        # model trainer
        
        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
       
        
        
        
        
    except Exception as e:
        print(e)