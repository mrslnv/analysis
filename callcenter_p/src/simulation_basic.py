from callcenter import CallCenter

call_center = CallCenter("time.csv")

regular_day_sche = call_center.create_regular_schedule()

call_center.load_schedule(regular_day_sche, [])

print("Utilization:", call_center.get_utilization())

call_center.run_simulation()

print("Avg. wait time:", call_center.get_avg_wait())
print("QoS (% under 20s wait):", call_center.get_qos())

call_center.write_stats("wtime-output-basic.csv")
