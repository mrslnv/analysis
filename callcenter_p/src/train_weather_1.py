import pandas as pd
from sklearn import ensemble
from sklearn.externals import joblib
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.read_csv("weather_calls.csv")

y = df['calls'].as_matrix()

del df["calls"]

X = df.as_matrix()

for i in range(0,10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)

    # Fit regression model
    model = ensemble.GradientBoostingRegressor(
        n_estimators=1000,
        learning_rate=0.029,
        max_depth=3,
        min_samples_leaf=3,
        max_features=0.2,
        loss='huber',
        random_state=i
    )
    model.fit(X_train, y_train)

    err = mean_absolute_error(y_train, model.predict(X_train))
    print("Error (train",i,"):", err)

    err = mean_absolute_error(y_test, model.predict(X_test))
    print("Error (test",i,"):", err)

