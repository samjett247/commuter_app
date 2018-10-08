
from googlemaps import Client
from datetime import datetime
dt = datetime.today()  # Get timezone naive now
now_int_time = str(dt.timestamp())[0:10]
print('Now time stamp ' + now_int_time)

future_int_time = int(now_int_time) + (20+48)*60*60 - 6800
future_int_time = int(now_int_time)

print('Future time stamp ' + str(future_int_time))

API_key = 'AIzaSyCJUNcLHEBBi8pd2CyYzSzlFZFvb_vOhaU'
gmaps = Client(API_key)

# def get_duration(origin, destination, dept_time):

directions = gmaps.directions(origin,destination, departure_time = dept_time, traffic_model = 'pessimistic')
print(directions)
duration = directions[0]['legs'][0]['duration_in_traffic']['text']
    # return duration

dur = get_duration(org, dest, dept_time)
print(datetime.fromtimestamp(dept_time))
print('The duration at the above time is ' + dur)

# print("It will take you " + dur + ' to get to ' + dest + '')





