import pandas as pd
from sklearn import ensemble
from sklearn.externals import joblib
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.read_csv("weather_calls.csv")

y = df["calls"].as_matrix()

del df["calls"]

#remove features (not enough training data)
del df["tornado"]
del df["state_count"]
del df["year"]
del df["day"]

X = df.as_matrix()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# Fit regression model
model = ensemble.GradientBoostingRegressor(
    n_estimators=1000,
    learning_rate=0.029,
    max_depth=3,
    min_samples_leaf=3,
    max_features=0.3,
    loss="huber",
    random_state=123
)
model.fit(X_train, y_train)

err_train = mean_absolute_error(y_train, model.predict(X_train))
print("Error (train):", err_train)

err_test = mean_absolute_error(y_test, model.predict(X_test))
print("Error (test):", err_test)

joblib.dump(model, "weather_predict_model.pkl")
