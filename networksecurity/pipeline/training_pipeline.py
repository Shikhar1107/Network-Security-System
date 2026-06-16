import os, sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig, 
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(self.data_ingestion_config)
            logging.info("Initiated the data ingestion")
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            print(f"Data Ingestion: {data_ingestion_artifact}\n")
            logging.info("Data Ingestion completed!!!")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:

        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            print(f"Data validation artifact: {data_validation_artifact}\n")
            logging.info(f"Data validation artifact: {data_validation_artifact}\n")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info("Data Transformation Started!!!!")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
            data_transformation_artifact = data_transformation.initaite_data_transformation()
            # print(f"Data Transformation artifact: {data_transformation_artifact}")
            logging.info(f"Data Transformation artifact: {data_transformation_artifact}")
            logging.info("Data Transformation Completed")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact)-> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(TrainingPipelineConfig())
            model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact)
            model_trainer_artifact = model_trainer.initaite_model_trainer()
            logging.info("Model training artiifact created!!")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
        except Exception as e:
            raise NetworkSecurityException(e,sys)