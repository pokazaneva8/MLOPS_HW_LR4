import os
import argparse
import numpy as np
from omegaconf import OmegaConf
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeRegressor
from joblib import dump
import mlflow

from src.minio_client import MINIO_CLIENT

mlflow.set_tracking_uri("http://localhost:5000")


def load_data(data_path):
    df = pd.read_csv(data_path)
    X = df.drop("averageRating", axis=1)
    y = df["averageRating"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=40
    )
    return X_train, X_test, y_train, y_test


def train_model(X_train, X_test, y_train, y_test, params):
    with mlflow.start_run(run_name="Decision Tree"):
        grid_search = GridSearchCV(DecisionTreeRegressor(), param_grid=params, cv=5)
        grid_search.fit(X_train, y_train)
        best_params = grid_search.best_params_
        dtr = DecisionTreeRegressor(**best_params).fit(X_train, y_train)
        y_hat = dtr.predict(X_test)

        mlflow.log_param("max_depth", best_params.get("max_depth"))
        mlflow.log_param("min_samples_split", best_params.get("min_samples_split"))
        mlflow.log_param("min_samples_leaf", best_params.get("min_samples_leaf"))

        dtr_mse = mean_squared_error(y_test, y_hat)
        dtr_rmse = np.sqrt(dtr_mse)
        dtr_r2 = r2_score(y_test, y_hat)

        mlflow.log_metric("MSE", dtr_mse)
        mlflow.log_metric("RMSE", dtr_rmse)
        mlflow.log_metric("R2", dtr_r2)

        model_name = (
            f"DecisionTreeRegressor_"
            f'{best_params["max_depth"]}_'
            f'{best_params["min_samples_split"]}_'
            f'{best_params["min_samples_leaf"]}'
            f".joblib"
        )

        dump(grid_search.best_estimator_, os.path.join("models", model_name))
        upload_to_s3(model_name)


def upload_to_s3(file_name):
    BUCKET_NAME = "trains"
    try:
        MINIO_CLIENT.create_bucket(Bucket=BUCKET_NAME)
        print(f"Бакет '{BUCKET_NAME}' успешно создан!")
        MINIO_CLIENT.upload_file(
            os.path.join("models", file_name),
            BUCKET_NAME,
            f"experiments/{mlflow.active_run().info.run_id}/{file_name}",
        )
    except MINIO_CLIENT.exceptions.BucketAlreadyExists:
        print(f"Бакет '{BUCKET_NAME}' уже существует.")
        MINIO_CLIENT.upload_file(
            os.path.join("models", file_name),
            BUCKET_NAME,
            f"experiments/{mlflow.active_run().info.run_id}/{file_name}",
        )
    except MINIO_CLIENT.exceptions.BucketAlreadyOwnedByYou:
        print(f"Бакет '{BUCKET_NAME}' уже существует.")
        MINIO_CLIENT.upload_file(
            os.path.join("models", file_name),
            BUCKET_NAME,
            f"experiments/{mlflow.active_run().info.run_id}/{file_name}",
        )
    except Exception as e:
        print(f"Ошибка при создании бакета: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обучение модели")
    parser.add_argument(
        "--data-path", type=str, required=True, help="Путь до преобразованного датасета"
    )
    parser.add_argument(
        "--params", type=str, required=True, help="Путь до гиперпараметров"
    )
    args = parser.parse_args()

    conf = OmegaConf.load(args.params)
    X_train, X_test, y_train, y_test = load_data(args.data_path)

    mlflow.set_experiment("Эксперимент")

    for model_name in conf.grid_search.keys():
        params = dict(conf.grid_search[model_name])
        train_model(X_train, X_test, y_train, y_test, params)
