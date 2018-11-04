def obtain_commute_times(origin, destination, time_range, time_int):
    '''
    This function will obtain the commute times from origin to destination.
    '''
    from googlemaps import Client
    from datetime import datetime, timedelta
    import numpy as np
    import time

    API_key = 'AIzaSyCJUNcLHEBBi8pd2CyYzSzlFZFvb_vOhaU'
    gmaps = Client(API_key)

    # The time interval on x-axis between each api call/data point
    time_interval = time_int  # time interval in Seconds
    t_int_minutes = time_interval / 60

    # This gives the nearest wednesday at midnight to the current data
    today = datetime.today()
    today_ind = today.weekday()
    day_modif = 16 - today_ind  # 16 to get the nearest wednesday, two weeks from now
    wednesday_mid = today + timedelta(days=day_modif, seconds=-today.second, minutes=-today.minute, hours=-today.hour)
    wed_mid_int = int(wednesday_mid.strftime("%s"))

    # This converts the start time into an integer time on monday
    hour_range_depart = time_range

    # This builds your time array based on the start time and end time monday

    start_time = wed_mid_int + hour_range_depart[0] * 3600
    end_time = wed_mid_int + hour_range_depart[1] * 3600
    num_intervals = int((end_time - start_time) / time_interval)

    # Use linspace to make our integer times
    times = np.linspace(start_time, end_time, num_intervals + 1, endpoint=True).astype(np.int)

    org = origin
    dest = destination

    org_mat = [org]
    dest_mat = [dest]

    commute_times = [] * len(times)

    for i in range(0, len(times)):
        dept_time_iter = times[i]
        directions = gmaps.distance_matrix(org_mat, dest_mat, departure_time=dept_time_iter,
                                           traffic_model='pessimistic')
        commute_time = directions['rows'][0]['elements'][0]['duration_in_traffic']['value']
        commute_times.append(round(commute_time/60, 1))

    return commute_times


