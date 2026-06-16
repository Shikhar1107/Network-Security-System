# Network Security System

An end-to-end machine learning project for detecting potentially malicious/phishing websites using structured network security features.
The project follows a modular ML pipeline architecture with data ingestion, validation, transformation, model training, experiment tracking, model persistence, and FastAPI-based prediction.

## Project Overview

This project demonstrates how a production-style machine learning system can be built for a binary classification use case in cybersecurity. The model predicts whether a given website/network record is legitimate or potentially unsafe based on extracted URL and network-related features.

The system includes:

* Data ingestion from MongoDB
* Data validation and train-test split
* Data transformation using `KNNImputer`
* Multiple model training with hyperparameter tuning
* Model evaluation using classification metrics
* Experiment tracking with MLflow and DagsHub
* Model and preprocessor serialization
* FastAPI application for prediction
* Docker support for containerized deployment
* GitHub Actions workflow for CI/CD with AWS ECR and self-hosted deployment

## Tech Stack

| Area           | Tools / Libraries           |
| -------------- | --------------------------- |
| Language       | Python 3.12                 |
| ML Libraries   | scikit-learn, pandas, numpy |
| Model Tracking | MLflow, DagsHub             |
| Database       | MongoDB Atlas               |
| API Framework  | FastAPI                     |
| Templating     | Jinja2                      |
| Deployment     | Docker                      |
| CI/CD          | GitHub Actions              |
| Cloud Registry | AWS ECR                     |
| Utilities      | python-dotenv, PyYAML       |

## Machine Learning Workflow

The project is organized as a pipeline with separate components for each stage.

### 1. Data Ingestion

The ingestion stage reads raw network security data from MongoDB and stores it locally for further processing.

Key responsibilities:

* Connect to MongoDB Atlas
* Export collection data as a pandas DataFrame
* Save raw data into a feature store
* Split data into train and test files

### 2. Data Validation

The validation stage checks whether the incoming data matches the expected schema.

Key responsibilities:

* Validate required columns
* Check dataset structure
* Separate valid train and test files
* Generate a validation artifact for downstream stages

### 3. Data Transformation

The transformation stage handles missing values and prepares the data for model training.

Key responsibilities:

* Split input features and target column
* Replace target label values where required
* Apply `KNNImputer`
* Save transformed train and test arrays
* Save the fitted preprocessing object

### 4. Model Training

The training stage compares multiple classification models and selects the best-performing one.

Models used:

* Random Forest Classifier
* Decision Tree Classifier
* Gradient Boosting Classifier
* Logistic Regression
* AdaBoost Classifier

Hyperparameter tuning is performed using `GridSearchCV`.

The best model is selected based on classification performance, especially F1 score.

### 5. Experiment Tracking with MLflow

MLflow is used to track model experiments and compare different model runs.

Logged information includes:

* Model name
* Best hyperparameters
* F1 score
* Precision
* Recall
* Model artifact

DagsHub is used as a remote MLflow tracking server.

### 6. Prediction API

The project includes a FastAPI application where users can upload a CSV file and receive predictions.

The prediction flow:

1. Upload CSV file
2. Load saved preprocessor
3. Load trained model
4. Transform input data
5. Generate predictions
6. Return prediction results in an HTML table
7. Save prediction output locally

## Project Structure

```text
network_security_system/
│
├── networksecurity/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── constant/
│   │   └── training_pipeline.py
│   │
│   ├── entity/
│   │   ├── artifact_entity.py
│   │   └── config_entity.py
│   │
│   ├── exception/
│   │   └── exception.py
│   │
│   ├── logging/
│   │   └── logger.py
│   │
│   ├── utils/
│   │   ├── main_utils.py
│   │   └── ml_utils/
│   │       ├── metric/
│   │       │   └── classification_metric.py
│   │       └── model/
│   │           └── estimator.py
│
├── templates/
│   └── table.html
│
├── final_model/
│   ├── model.pkl
│   └── preprocessor.pkl
│
├── prediction_output/
│   └── output.csv
│
├── app.py
├── main.py
├── Dockerfile
├── requirements.txt
├── setup.py
├── .env
├── .gitignore
└── README.md
```

> Note: Generated artifacts such as trained models, preprocessors, prediction outputs, and pipeline artifacts should not be committed to GitHub.

## Model Evaluation Metrics

The project uses the following classification metrics:

* F1 Score
* Precision
* Recall

These metrics are tracked in MLflow for each experiment run.

## MLflow Tracking

MLflow helps track and compare experiments across different models and hyperparameter combinations.

Example tracked parameters:

```text
model_name = Random Forest
n_estimators = 128
```

Example tracked metrics:

```text
f1_score
precision
recall_score
```

The best model is logged as an MLflow model artifact and can optionally be registered in the MLflow Model Registry.

## FastAPI Application

Run the FastAPI app locally:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Then open:

```text
http://localhost:8000
```

Prediction endpoint:

```text
POST /predict
```

The endpoint accepts a CSV file and returns predictions in a rendered HTML table.

## Docker Setup

Build the Docker image:

```bash
docker build -t network-security-system .
```

Run the container:

```bash
docker run -p 8000:8000 network-security-system
```

If the application runs on port `8000` inside the container, map it like this:

```bash
docker run -p 8080:8000 network-security-system
```

Then access:

```text
http://localhost:8080
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow for CI/CD.

The workflow performs:

1. Continuous Integration

   * Checkout repository
   * Linting placeholder
   * Unit testing placeholder

2. Continuous Delivery

   * Configure AWS credentials
   * Login to Amazon ECR
   * Build Docker image
   * Push image to ECR

3. Continuous Deployment

   * Run on a self-hosted GitHub Actions runner
   * Pull latest Docker image from ECR
   * Run the application container on the server
   * Clean unused Docker resources

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
MONGO_DB_URI=your_mongodb_connection_string
MLFLOW_TRACKING_URI=your_mlflow_tracking_uri
MLFLOW_TRACKING_USERNAME=your_dagshub_username
MLFLOW_TRACKING_PASSWORD=your_dagshub_token
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
```

Do not commit `.env` to GitHub.

## Git Ignore Recommendations

The following files and folders should be ignored:

```gitignore
.venv/
__pycache__/
.env
Artifacts/
final_model/
prediction_output/
*.pkl
*.log
```

## How to Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Shikhar1107/network_security_system.git
cd network_security_system
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

For Windows:

```bash
.venv\Scripts\activate
```

For Linux/Mac:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add the required environment variables.

### 5. Run the training pipeline

```bash
python main.py
```

### 6. Start the FastAPI app

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Example Prediction Flow

1. Start the FastAPI server
2. Upload a CSV file through the prediction route
3. The app loads the saved preprocessor and model
4. The uploaded data is transformed
5. Predictions are generated
6. Results are displayed in an HTML table

## Key Learnings

This project helped implement and understand:

* End-to-end machine learning pipeline design
* Modular project architecture
* MongoDB-based data ingestion
* Schema validation
* Data transformation and preprocessing
* Model comparison using multiple ML algorithms
* Hyperparameter tuning with GridSearchCV
* Experiment tracking using MLflow and DagsHub
* Model serialization and inference
* FastAPI-based ML model serving
* Dockerization of ML applications
* CI/CD deployment workflow with GitHub Actions and AWS ECR

## Future Improvements

Planned improvements:

* Add real linting and unit tests in GitHub Actions
* Add model performance threshold before deployment
* Add automated model promotion using MLflow Model Registry
* Add API request validation using Pydantic models
* Add batch prediction history tracking
* Add monitoring for prediction drift
* Add cloud deployment using ECS or EC2
* Improve UI for file upload and prediction results

## Author

**Shikhar Gupta**

GitHub: [@Shikhar1107](https://github.com/Shikhar1107)
