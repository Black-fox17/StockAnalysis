from sklearn.preprocessing import MinMaxScaler
from .extract import get_data
import numpy as np
from keras.models import load_model
import joblib
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir,"apple.h5")
model = load_model(model_path)
scaler = joblib.load(os.path.join(current_dir,"scaler.pkl"))

def get_pred(test_data:list)-> float:
    x_test = np.array(test_data)

    # Reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

    # Get the models predicted price values 
    predictions = model.predict(x_test)
    # predictions = scaler.inverse_transform(predictions)
    return predictions


def get_predictions(ticker):
    data = get_data(ticker,61)
    data_values = np.array([[x["price"]] for x in data])
    print(data_values)
    scaled_data = scaler.transform(data_values)
    test_data = scaled_data[-61:-1,0]
    predictions = []
    for _ in range(5):
        result = get_pred([test_data])
        predictions.append(float(scaler.inverse_transform(result)))
        test_data = np.append(test_data,result[0])[-60:]

    
    json_value = {
        "data":data[:24],
        "prediction":predictions
    }
    return json_value
