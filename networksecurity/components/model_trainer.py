from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact, ClassificationMetricArtifact
import os,sys
from networksecurity.utils import save_object, load_object, load_numpy_array_data
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier)
import mlflow
from urllib.parse import urlparse
import dagshub
from dotenv import load_dotenv
load_dotenv()

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self, best_model, classificationmetric, model_name, best_params):

        try:
            dagshub.init(repo_owner='shikharjul01', repo_name='Network-Security-System', mlflow=True)

            mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            with mlflow.start_run():
                f1_score = classificationmetric.f1_score
                precision_score = classificationmetric.precision_score
                recall_score = classificationmetric.recall_score

                # Log model name and best hyperparameters
                mlflow.log_param("model_name", model_name)
                mlflow.log_params(best_params)

                # Log metrics
                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision", precision_score)
                mlflow.log_metric("recall_score", recall_score)

                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(
                        best_model,
                        name="model",
                        registered_model_name="NetworkSecurityModel"
                    )
                else:
                    mlflow.sklearn.log_model(best_model, "model")
        except Exception as e:
            logging.warning(f"MLflow/DagsHub tracking failed: {e}")
                
    def evaluate_models(self, x_train,y_train,x_test,y_test,models,params):
        try:
            report = {}
            best_params_report = {}

            for i in range(len(list(models))):
                model_name = list(models.keys())[i]
                model = list(models.values())[i]
                param = params[list(models.keys())[i]]

                gs = GridSearchCV(model,param,cv = 3)
                gs.fit(x_train,y_train)

                model.set_params(**gs.best_params_)
                model.fit(x_train,y_train)

                y_train_pred = model.predict(x_train)
                y_test_pred = model.predict(x_test)

                train_classification_metric = get_classification_score(
                y_true=y_train,
                y_pred=y_train_pred
                )

                test_classification_metric = get_classification_score(
                    y_true=y_test,
                    y_pred=y_test_pred
                )

                report[model_name] = test_classification_metric.f1_score
                best_params_report[model_name] = gs.best_params_

                logging.info(f"Model name: {model_name}")
                logging.info(f"Best params: {gs.best_params_}")
                logging.info(f"Train metric: {train_classification_metric}")
                logging.info(f"Test metric: {test_classification_metric}")

            return report, best_params_report
            
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def train_model(self,x_train,y_train,x_test,y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose = 1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier()
        }
        params = {
            "Decision Tree": {
                'criterion': ['gini','entropy','log_loss'],
                # 'splitter': ['best', 'random'],
                # 'max_features': ['sqrt','log2']
            },
            "Random Forest": {
                # "criterion": ['gini','entropy','log_loss'],
                # 'max_features': ['sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Gradient Boosting": {
                # "loss": ['log_loss','exponential'],
                'learning_rate': [.1,.01,.05,.001],
                'subsample': [0.6,0.7,0.75,0.8,0.85,0.9],
                # "criterion": ['gini','entropy','log_loss'],
                # 'max_features': ['sqrt','log2']
                'n_estimators': [8,16,32,64,128,256]
            },
            'Logistic Regression': {},
            "AdaBoost": {
                'learning_rate': [.1,.01,.05,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
        }
        model_report, best_params_report = self.evaluate_models(x_train, y_train, x_test, y_test, models, params)

        best_model_score = max(model_report.values())

        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_model = models[best_model_name]
        best_params = best_params_report[best_model_name]

        y_train_pred = best_model.predict(x_train)

        classification_train_metric=get_classification_score(y_train,y_train_pred)

        # Track the experiments with mlflow
        self.track_mlflow(
            best_model=best_model,
            classificationmetric=classification_train_metric,
            model_name=best_model_name,
            best_params=best_params
        )
        y_test_pred=best_model.predict(x_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

        self.track_mlflow(
            best_model=best_model,
            classificationmetric=classification_test_metric,
            model_name=best_model_name,
            best_params=best_params
        )
        
        preprocessor =  load_object(self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)
        #model pusher
        save_object("final_model/model.pkl",best_model)

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path, train_metric_artifact=classification_train_metric, test_metric_artifact= classification_test_metric
        )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact

    def initaite_model_trainer(self)-> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            print("train_arr shape:", train_arr.shape)
            print("test_arr shape:", test_arr.shape)
            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:, -1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_trainer_artifact = self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)