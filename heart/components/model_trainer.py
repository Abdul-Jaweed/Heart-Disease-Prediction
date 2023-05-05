# Model Define and Trainer
# Saving Accuracy
# 70,78,85,95,99 then we can accept else we reject the (threshold)
# Checking Overfitting and Underfitting



from heart.entity import artifact_entity,config_entity
from heart.exception import HeartException
from heart.logger import logging
from typing import Optional
import os,sys 
import xgboost as xg
from sklearn.linear_model import LogisticRegression
from heart import utils
from sklearn.metrics import accuracy_score

class ModelTrainer:
    
    def __init__(self, model_trainer_config:config_entity.ModelTrainerConfig,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            
        except Exception as e:
            raise HeartException(e, sys)
    
    
    def train_model(self,x,y):
        try:
            
            lr = LogisticRegression()
            lr.fit(x,y)
            return lr
        
        except Exception as e:
            raise HeartException(e, sys)
        
    
    
    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            
            logging.info(f"Loading train and test array.")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)
            

            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]
            

            logging.info(f"Train the model")
            model = self.train_model(x=x_train,y=y_train)
            
            
            logging.info(f"Calculating train accuracy_score")
            yhat_train = model.predict(x_train)
            accuracy_train_score = accuracy_score(y_true=y_train, y_pred=yhat_train)

            logging.info(f"Calculating test accuracy_score")
            yhat_test = model.predict(x_test)
            accuracy_test_score = accuracy_score(y_true=y_test, y_pred=yhat_test)
            
            
            logging.info(f"train score:{accuracy_train_score} and tests score {accuracy_test_score}")
            #check for overfitting or underfiiting or expected score
            logging.info(f"Checking if our model is underfitting or not")
            if accuracy_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: Model Actual Score: {accuracy_test_score}")
              
                
            logging.info(f"Checking if our model is overfiiting or not")
            diff = abs(accuracy_train_score-accuracy_test_score)
            
            
            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score difference : {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")
            
            
            #save the trained model
            logging.info(f"Saving Model Object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)
                
            
            
            #prepare artifact
            
            logging.info(f"Prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            accuracy_train_score=accuracy_train_score, accuracy_test_score=accuracy_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            
            return model_trainer_artifact
                
  
        except Exception as e:
            raise HeartException(e, sys)


