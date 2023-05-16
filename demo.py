from heart.pipeline.batch_prediction import start_batch_prediction
from heart.pipeline.training_pipeline import start_training_pipeline


#file_path = r"data\heart.csv"

if __name__ == '__main__':
    try:
        
        #output = start_batch_prediction(input_file_path=file_path)
        output_file = start_training_pipeline()
    
    except Exception as e:
        print(e)