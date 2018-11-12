def obtain_commute_times(origin, destination, time_range, time_int):
    '''
    This function will obtain the commute times from origin to destination.
    '''
    from googlemaps import Client
    from datetime import datetime, timedelta
    import numpy as np
    import time
    import pytz

    # Import api key from apikey.py
    from apikey import gmaps_dir_matrix_key

    API_key = gmaps_dir_matrix_key # Insert your Google Distance Matrix API Key here

    gmaps = Client(API_key)

    # The time interval on x-axis between each api call/data point
    time_interval = time_int  # time interval in Seconds
    t_int_minutes = time_interval / 60
    
    # Define the correct timezone via the destination
    # Geocode the input address
    geocode_result = gmaps.geocode(destination)
    # Obtain latitude and longitude information
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']

    # Obtain the timezone for the geocoded address longitude and latitude
    timezone = gmaps.timezone((lat, lng))
    tz = timezone['timeZoneId']

    # Pass the timezone to datetime.today to get the current time in that timezone
    location_tz = pytz.timezone(tz)
    # location_tz = pytz.timezone("US/Pacific")
    today =datetime.now(location_tz)
    ct_time = datetime.now(pytz.timezone("America/Chicago")) # Get central time

    # This gives the nearest wednesday at midnight to the current data
    print("Today is ")
    print(today)
    today_ind = today.weekday()
    day_modif = 16 - today_ind  # 16 to get the nearest wednesday, two weeks from now
    wednesday_mid = today + timedelta(days=day_modif, seconds=-today.second, minutes=-today.minute, hours=-today.hour)
    print(today.hour)
    wed_mid_int = int(wednesday_mid.strftime("%s"))

    # This converts the start time into an integer time on monday
    hour_range_depart = time_range

    # Calculate time diff from central time
    time_diff_ct = int(int(today.strftime("%s")) - int(ct_time.strftime("%s")))

    # This builds your time array based on the start time and end time monday and the difference between the time zone of interest and the central time zone
    start_time = wed_mid_int + (hour_range_depart[0]) * 3600 + time_diff_ct
    end_time = wed_mid_int + (hour_range_depart[1]) * 3600 +time_diff_ct
    num_intervals = int((end_time - start_time) / time_interval)

    # Use linspace to make our integer times
    times = np.linspace(start_time, end_time, num_intervals + 1, endpoint=True).astype(np.int)

    org_mat = [origin]
    dest_mat = [destination]

    commute_times = [] * len(times)
    print(times)
    for i in range(0, len(times)):
        dept_time_iter = times[i]
        directions = gmaps.distance_matrix(org_mat, dest_mat, departure_time=dept_time_iter,
                                           traffic_model='pessimistic')
        commute_time = directions['rows'][0]['elements'][0]['duration_in_traffic']['value']
        commute_times.append(round(commute_time/60, 1))

    return commute_times