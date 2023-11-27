import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from taxifare.ml_logic.preprocessor import preprocess_features
# from taxifare.ml_logic.data import clean_data
# from taxifare.ml_logic.model import initialize_model, compile_model, evaluate_model
# from taxifare.ml_logic.registry import save_results, load_model
app = FastAPI()
# app.state.model = load_model()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# @app.get("/predict")
# def predict(
        # pickup_datetime: str,  # 2013-07-06 17:18:00
        # pickup_longitude: float,    # -73.950655
        # pickup_latitude: float,     # 40.783282
        # dropoff_longitude: float,   # -73.984365
        # dropoff_latitude: float,    # 40.769802
        # passenger_count: int
    # ):      # 1
    # """
    # Make a single course prediction.
    # Assumes `pickup_datetime` is provided as a string by the user in "%Y-%m-%d %H:%M:%S" format
    # Assumes `pickup_datetime` implicitly refers to the "US/Eastern" timezone (as any user in New York City would naturally write)
    # """

    # store X_pred into a dataframe
    # X_pred = pd.DataFrame(locals(), index=[0])
    # X_pred['pickup_datetime'] = pd.Timestamp(pickup_datetime, tz="US/Eastern")

    # # process X
    # X_pred = preprocess_features(X_pred)

    # # predict y
    # y_pred = app.state.model.predict(X_pred)
    # return dict(fare_amount=float(y_pred))

@app.get("/")
def root():
    return {
        'testing' : 'Hello'
        }
