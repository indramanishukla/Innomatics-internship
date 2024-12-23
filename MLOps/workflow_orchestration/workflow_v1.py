from typing import Any, Dict, List
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor
import mlflow


def load_data(path: str, unwanted_col :list) -> pd.DataFrame:
    data = pd.read_csv(path)
    data.drop(unwanted_col, axis=1, inplace=True)
    return data

def get_scaler(data: pd.DataFrame) -> Any:
    scaler = StandardScaler()
    scaler.fit(data.select_dtypes(exclude='object'))
    return scaler

def get_encoder(data: pd.DataFrame) -> Any:
    encoder = OrdinalEncoder()
    encoder.fit(data.select_dtypes(include='object'))
    return encoder

def rescale_data(data: pd.DataFrame, scaler: Any) ->pd.DataFrame:
    rescaled_data = pd.DataFrame(scaler.transform(data.select_dtypes(exclude='object')), columns=data.select_dtypes(exclude='object').columns, index=data.index)
    return rescaled_data

def encode_data(data: pd.DataFrame, encoder: Any) ->pd.DataFrame:
    encoded_data = pd.DataFrame(encoder.transform(data.select_dtypes(include='object')), columns=data.select_dtypes(include='object').columns, index=data.index)
    return encoded_data

def split_data(X_var: pd.DataFrame, target_var: pd.Series,  train_size_ratio: float) ->Any:
    X_tr, X_te, y_tr, y_te = train_test_split(X_var, target_var, train_size=train_size_ratio, random_state=42)
    return X_tr, X_te, y_tr, y_te

def concat(X_num: pd.DataFrame, X_cat: pd.DataFrame) -> pd.DataFrame:
    concat_data = pd.concat([X_num, X_cat], axis=1)
    return concat_data 


def find_best_model(X_tr: pd.DataFrame, y_tr: pd.Series, estimator: Any, parameters: list, cv: int) ->Any:
    
    mlflow.set_tracking_uri('sqlite:///mlflow.db')
    mlflow.set_experiment('diamonds regression experiment')
    
    mlflow.sklearn.autolog(max_tuning_runs=None)
    with mlflow.start_run():
        

        grid = GridSearchCV(estimator=estimator, 
        scoring= 'neg_root_mean_squared_error',  
        param_grid=parameters, 
        cv = cv, 
        verbose=1)
        grid.fit(X_tr, y_tr)
        # y_test_pred = grid.predict(X_test_proc)
        # rmse = metrics.mean_squared_error(test_labels, y_test_pred, squared=False)
        # mlflow.log_metric('rmse', rmse)

        mlflow.sklearn.autolog(disable=True)
    
        return grid

# workflow

def main(path: str):
    # Define Parameters
    TARGET_COL = 'price'
    UNWANTED_COLS = ['depth', 'y', 'z']
    TRAIN_SIZE_RATIO = 0.7
    DATA_PATH = path

    # Load the data
    dataframe = load_data(path=DATA_PATH, unwanted_col= UNWANTED_COLS)

    # Identify target variable
    target_data = dataframe[TARGET_COL]
    input_data = dataframe.drop([TARGET_COL], axis=1)

    # split data into train test split

    X_train, X_test, y_train, y_test = split_data(input_data, target_data, train_size_ratio= TRAIN_SIZE_RATIO)

    # get scaler and encoder
    scaler = get_scaler(X_train)
    encoder = get_encoder(X_train)
    
    # Rescale and encode data
    X_train_rescaled = rescale_data(X_train, scaler=scaler)
    X_test_rescaled = rescale_data(X_test, scaler=scaler)
    X_train_encoded = encode_data(X_train, encoder=encoder)
    X_test_encoded = encode_data(X_test, encoder=encoder)

    # concate rescaled and encoded data
    X_train_processed = concat(X_train_rescaled, X_train_encoded)
    X_test_processed = concat(X_test_rescaled, X_test_encoded)

    # Model training
    ESTIMATOR = DecisionTreeRegressor()
    HYPERPARAMETERS = [{
        'max_depth': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'min_samples_leaf':[10, 12, 14, 16, 18, 20],
        'min_samples_split': [30, 40, 50, 60],
        'random_state': [42],
        }]

    regresser = find_best_model(X_train_processed, y_train, estimator=ESTIMATOR, parameters= HYPERPARAMETERS, cv=5)
    print(regresser.best_params_)
    print(regresser.score(X_train_processed, y_train))

# Run the main function
main(path = './data/diamonds.csv')