from callcenter import CallCenter
from prediction import get_weather_predictions

weather_events = get_weather_predictions()
print("Prediction of severe weather conditions:", weather_events)

call_center = CallCenter("time.csv")

regular_day_sche = call_center.create_regular_schedule()

call_center.load_schedule(regular_day_sche, weather_events)

# a schedule and its utilizaiton can be computed upfront.
# It could be easily optimized even without running the simulation
print("Utilization:", call_center.get_utilization())

call_center.run_simulation()

print("Avg. wait time:", call_center.get_avg_wait())
print("QoS (% under 20s wait):", call_center.get_qos())

call_center.write_stats("wtime-output.csv")
