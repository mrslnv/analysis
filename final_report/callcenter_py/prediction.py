from sklearn.externals import joblib
import pandas as pd

def get_weather_predictions():
    model = joblib.load("weather_predict_model.pkl")

    df = pd.read_csv("weather_calls.csv")

    ys = df["year"]
    ms = df["month"]
    ds = df["day"]
    weather_dates = []
    for y, m, d in zip(ys, ms, ds):
        weather_dates.append(str(y) + "-" + str(m) + "-" + str(d))

    # delete unused features (small training data set :-()
    del df["calls"]
    del df["tornado"]
    del df["state_count"]
    del df["year"]
    del df["day"]

    weather_events = []
    predict = model.predict(df.as_matrix())
    for date, pred in zip(weather_dates, predict):
        extra = int((pred - 380) / (3 * 30)) # above average calls split to 3 hour slots with extra employe
        if extra > 0:
            weather_events.append([date, extra])

    return weather_events
