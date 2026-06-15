from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
import sys

if __name__ == '__main__':
    try:
        data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiated the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(f"Data Ingestion: {data_ingestion_artifact}\n")
        logging.info("Data Ingestion completed!!!")
        data_validation_config = DataValidationConfig(training_pipeline_config=TrainingPipelineConfig())
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        print(f"Data validation artifact: {data_validation_artifact}\n")
        logging.info(f"Data validation artifact: {data_validation_artifact}\n")
        logging.info("Data Transformation Started!!!!")
        data_transformation_config = DataTransformationConfig(TrainingPipelineConfig())
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact = data_transformation.initaite_data_transformation()
        print(f"Data Transformation artifact: {data_transformation_artifact}")
        logging.info(f"Data Transformation artifact: {data_transformation_artifact}")

        logging.info("Data Transformation Completed")

        model_trainer_config = ModelTrainerConfig(TrainingPipelineConfig())
        model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact)
        model_trainer_artifact = model_trainer.initaite_model_trainer()

        logging.info("Model training artiifact created!!")


    except Exception as e:
        raise NetworkSecurityException(e,sys)