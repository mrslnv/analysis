from sklearn.externals import joblib

model = joblib.load("weather_predict_model.pkl")

# sev, wnd, hail, jn, pa, mon
sample = [5,397,44,1,1,2]
predict = model.predict([sample])

print("Predicted:",predict)