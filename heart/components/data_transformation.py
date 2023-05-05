# Filling Missing Values
# Handling Outlier
# Imbalanced Data Handling
# Convert catergorical to numerical 

from heart.entity import artifact_entity, config_entity
from heart.logger import logging
from heart.exception import HeartException
import sys
import os
from typing import Optional
from sklearn.pipeline import Pipeline
import pandas as pd
from heart import utils
import numpy as np
from sklearn.preprocessing import StandardScaler
from heart.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder

class DataTransformation:
    
    def __init__(self, data_transformation_config: config_entity.DataTransformationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise HeartException(e, sys)
    
    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        try:
            standard_scaler = StandardScaler()
            pipeline = Pipeline(steps=[
                    ('StandardScaler', standard_scaler)
                ])
            return pipeline
        except Exception as e:
            raise HeartException(e, sys)
    
    def initiate_data_transformation(self) -> artifact_entity.DataTransformationArtifact:
        try:
            #reading training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            #selecting input feature for train and test dataframe
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)

            #selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            #apply data transformer
            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            #transforming input features
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)
            
            #concatenate transformed input features with target features
            train_arr = np.c_[input_feature_train_arr, target_feature_train_df.squeeze()]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_df.squeeze()]

            #save transformed arrays
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_arr)

            #save data transformer object
            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
                               obj=transformation_pipeline)

            #save target encoder
            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
                               obj=label_encoder)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path,
                target_encoder_path=self.data_transformation_config.target_encoder_path)

            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise HeartException(e, sys)
