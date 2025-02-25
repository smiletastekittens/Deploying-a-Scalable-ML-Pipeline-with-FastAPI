import pickle
from sklearn.metrics import fbeta_score, precision_score, recall_score
from sklearn.linear_model import LogisticRegression
from ml.data import process_data


def train_model(X_train, y_train, **kwargs):
    """
    Trains a machine learning model and returns it.

    Inputs
    ------
    X_train : np.array
        Training data.
    y_train : np.array
        Labels.
    kwargs : dict
        Additional model parameters
    Returns
    -------
    model : sklearn.linear_model.LogisticRegression
        Trained machine learning model.
    """
    try:
        lr = LogisticRegression(**kwargs).fit(X_train, y_train)
    except Exception as e:
        raise Exception(f"Could not create and train model: {type(e)}: {e}")
    return lr


def compute_model_metrics(y, preds):
    """
    Validates the trained machine learning model using precision, recall, and F1.

    Inputs
    ------
    y : np.array
        Known labels, binarized.
    preds : np.array
        Predicted labels, binarized.
    Returns
    -------
    precision : float
    recall : float
    fbeta : float
    """
    fbeta = fbeta_score(y, preds, beta=1, zero_division=1)
    precision = precision_score(y, preds, zero_division=1)
    recall = recall_score(y, preds, zero_division=1)
    return precision, recall, fbeta


def inference(model, X):
    """ Run model inferences and return the predictions.

    Inputs
    ------
    model : sklearn.linear_model.LogisticRegression
        Trained machine learning model.
    X : np.array
        Features used for prediction.
    Returns
    -------
    preds : np.array
        Predicted labels from the model.
    """
    return model.predict(X)

def save_model(model, path):
    """ Serializes model to a file.

    Inputs
    ------
    model
        Trained machine learning model or OneHotEncoder.
    path : str
        Path to save pickle file.
    """
    try:
        with open(path, 'wb+') as fp:
            pickle.dump(model, fp)
    except Exception as e:
        raise Exception(f'Could not write model to disk: {type(e)}: {e}')


def load_model(path):
    """ Loads pickle file from `path` and returns it.
    
    Inputs
    ------
    path : str
        Path to pickle model file
    Returns
    -------
    model : sklearn.linear_model.LogisticRegression
        The desired model
    """
    try:
        with open(path, 'rb') as fp:
            model = pickle.load(fp)
    except Exception as e:
        raise Exception(f'Could not load model: {type(e)}: {e}, path: {path}')
    return model


def performance_on_categorical_slice(
    data, column_name, slice_value, categorical_features, label, encoder, lb, model
):
    """ Computes the model metrics on a slice of the data specified by a column name and

    Processes the data using one hot encoding for the categorical features and a
    label binarizer for the labels. This can be used in either training or
    inference/validation.

    Inputs
    ------
    data : pd.DataFrame
        Dataframe containing the features and label. Columns in `categorical_features`
    column_name : str
        Column containing the sliced feature.
    slice_value : str, int, float
        Value of the slice feature.
    categorical_features: list
        List containing the names of the categorical features (default=[])
    label : str
        Name of the label column in `X`. If None, then an empty array will be returned
        for y (default=None)
    encoder : sklearn.preprocessing._encoders.OneHotEncoder
        Trained sklearn OneHotEncoder, only used if training=False.
    lb : sklearn.preprocessing._label.LabelBinarizer
        Trained sklearn LabelBinarizer, only used if training=False.
    model : ???
        Model used for the task.

    Returns
    -------
    precision : float
    recall : float
    fbeta : float

    """
    sliced_data = data[data[column_name] == slice_value]
    X_slice, y_slice, _, _ = process_data(
        X=sliced_data,
        categorical_features=categorical_features,
        label=label,
        training=False,
        encoder=encoder,
        lb=lb
    )
    preds = inference(model, X_slice)
    precision, recall, fbeta = compute_model_metrics(y_slice, preds)
    return precision, recall, fbeta
