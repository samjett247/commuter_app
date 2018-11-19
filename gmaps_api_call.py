from googlemaps import Client
from datetime import datetime, timedelta
import numpy as np
import time
import pytz
import os

def convert_timezone_to_utc_epoch(timestamp_string, local_tz):
    ''' 
    input is in GMT/UTC time
    '''
    ts = datetime.strptime(timestamp_string, '%Y-%m-%d %H:%M:%S')
    ts = str(ts)[0:19] #MODIFIED such that the input can be in local time!
    # Compute the Epoch time for the API call
    epoch = int(time.mktime(time.strptime(ts, '%Y-%m-%d %H:%M:%S')))
    return epoch

def obtain_commute_times(origin, destination, time_range, time_int):
    '''
    This function will obtain the commute times from origin to destination.
    '''

    # Import api key from apikey.py
    from apikey import gmaps_dir_matrix_key

    API_key = gmaps_dir_matrix_key # Insert your Google Distance Matrix API Key here
    
    # Build an API Client for the call
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

    # Change the environment timezone to the timezone of the destination
    os.environ['TZ'] = tz

    # Pass the timezone to datetime.today to get the current time in that timezone
    location_tz = pytz.timezone(tz)
    today = datetime.now(location_tz)

    # This gives the nearest wednesday at midnight to the current data
    today_ind = today.weekday()
    day_modif = 16 - today_ind  # 16 to get the nearest wednesday, two weeks from now
    wednesday_mid = today + timedelta(days=day_modif, seconds=-today.second, minutes=-today.minute, hours=-today.hour)
    wed_mid_int = int(wednesday_mid.strftime("%s"))

    # Create the first and last query times
    first_query = wednesday_mid+timedelta(hours = time_range[0])
    first_q = first_query.strftime("%Y-%m-%d %H:%M:%S")
    last_query = wednesday_mid+timedelta(hours = time_range[1])
    last_q = last_query.strftime("%Y-%m-%d %H:%M:%S")
    
    # Convert query times to Epoch time
    start_time = convert_timezone_to_utc_epoch(first_q, location_tz)
    end_time = convert_timezone_to_utc_epoch(last_q, location_tz)

    print("The first epoch is ")
    print(start_time)
    print("The second epoch  is ")
    print(end_time)
    num_intervals = int((end_time - start_time) / time_interval)

    # Use linspace to make our integer times
    times = np.linspace(start_time, end_time, num_intervals + 1, endpoint=True).astype(np.int)

    org_mat = [origin]
    dest_mat = [destination]

    commute_times = [] * len(times)
    
    for i in range(0, len(times)):
        # Call the google distance matrix api for each departure time
        dept_time_iter = times[i]
        directions = gmaps.distance_matrix(org_mat, dest_mat, departure_time=dept_time_iter,
                                           traffic_model='pessimistic')
        commute_time = directions['rows'][0]['elements'][0]['duration_in_traffic']['value']
        commute_times.append(round(commute_time/60, 1))

    # Set the environment to the UTC, for standardization
    os.environ['TZ'] = 'UTC'
    
    return commute_times
