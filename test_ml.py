import os
import pytest

import numpy as np
import pandas as pd

from ml.model import process_data
from ml.model import load_model, inference
from sklearn.linear_model import LogisticRegression


@pytest.fixture(scope="session")
def data():
    project_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(project_path, "data", "census.csv")
    data = pd.read_csv(data_path)
    return data

@pytest.fixture(scope="session")
def features():
    feat =  [
        "workclass",
        "education",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native-country",
    ]

    feat.sort()
    return feat


@pytest.fixture(scope="session")
def model():
    project_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_path, "model", "model.pkl")
    model = load_model(model_path)
    return model

@pytest.fixture(scope="session")
def encoder():
    project_path = os.path.dirname(os.path.abspath(__file__))
    encoder_path = os.path.join(project_path, "model", "encoder.pkl")
    encoder = load_model(encoder_path)
    return encoder


def test_dataset_features_and_label(data, features):
    """
    Inspects the dataset columns to ensure that the requisite features and
    label are present
    """

    label = 'salary'
    columns = data.columns.to_list()
    assert label in columns, f"Label column {label} not found in the dataset"

    columns.remove('salary')
    columns.sort()

    has_column = list(map(lambda x: x in columns, features))

    assert all(has_column), f"Columns in dataset do not contain required features for the model"


def test_model_class(model):
    """
    Checks the model type information to ensure it matches the expected class
    """
    assert isinstance(model, LogisticRegression), f"Unexpected model class: {type(model)}"


def test_model_output(data, features, model, encoder):
    """
    Tests the model inference output to ensure it works and conforms
    to an expected range
    """
    sample = data.head(100)

    X_test, _, _, _ = process_data(
        sample,
        categorical_features=features,
        label="salary",
        training=False,
        encoder=encoder
    )

    preds = inference(model, X_test)
    bounded = list(map(lambda x: x >= 0.0 and x <= 1.0, preds))

    assert all(bounded), "Model inference output is not constrained between 0.0 and 1.0"
