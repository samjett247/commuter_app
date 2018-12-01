
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
import numpy as np

from gmaps_api_call import obtain_commute_times
from generate_labels import gen_labels
from compute_statistics import compute_statistics
import os
import sys
# import logging 
# import requests

# From home (fh) time range
fh_time_range = (6,10)

# From work (fw) time range
fw_time_range = (15, 19)

# Define the time intervals of the predictions (in seconds)
time_int = 900 # Seconds


# Create app variable
app = Flask(__name__)

# Add the secret generator for the session key
app.secret_key = os.urandom(24)

# Define Google Analytics tracking ID
GA_TRACKING_ID = ''


def track_event(category, action, label=None, value=0):
    data = {
        'v': '1',  # API Version.
        'tid': GA_TRACKING_ID,  # Tracking ID / Property ID.
        # Anonymous Client Identifier. Ideally, this should be a UUID that
        # is associated with particular user, device, or browser instance.
        'cid': '555',
        't': 'event',  # Event hit type.
        'ec': category,  # Event category.
        'ea': action,  # Event action.
        'el': label,  # Event label.
        'ev': value,  # Event value, must be an integer
    }

    response = requests.post(
        'http://www.google-analytics.com/collect', data=data)

    # If the request fails, this will raise a RequestException. Depending
    # on your application's needs, this may be a non-error and can be caught
    # by the caller.
    response.raise_for_status()


# Create route for the app
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/')
# track_event(category='Visits', action='site visits')
def index():
    # Return the template
    return render_template('home.html')

@app.route('/about')
# track_event(category='Visits', action='about visits')
def about():
    return render_template('about.html')


@app.route('/optimize', methods = ['POST', 'GET'])
def optimize_commute():

    print(request.form)
    if request.method == 'POST' and request.form.get('home_addr')!= None:

        # Take the parameters from the form and store them in the session dict for easier access

        session['user_name'] = request.form['user_name']
        session['home_addr'] = request.form['home_addr']
        session["work_addr"]  = request.form['work_addr']
        session['departure_from_home']  = request.form["departure_from_home"]
        session['departure_from_work']= request.form['departure_from_work']
        # Compute the fh and fw time ranges based on the entries into the form, +- 2 hours
        fh_average = int(departure_from_home[0:2])
        fh_time_range = (fh_average-2,fh_average+2)

        fw_average = int(departure_from_work[0:2])
        fw_time_range = (fw_average-2,fw_average+2)

        # Call the google API to get the route info for the person
        # Call api to get  commute times
        # global fh_commute_times, fw_commute_times
        session['fh_commute_times'] = obtain_commute_times(home_addr, work_addr, fh_time_range, time_int)
        session['fw_commute_times'] = obtain_commute_times(work_addr, home_addr, fw_time_range, time_int)

        # Generate the labels for both cases
        # global fh_labels, fw_labels
        session['fh_labels'] = fh_labels = gen_labels(fh_time_range, time_int)
        session['fw_labels'] = gen_labels(fw_time_range, time_int)

        # Compute statistics for both cases
        session['fh_statistics'] = compute_statistics(fh_commute_times, fh_labels)
        session['fw_statistics']= compute_statistics(fw_commute_times, fw_labels)

        # Create the arguments package of variables to pass between the pages. The order is important and shouldnt be changed, but can be added to if needed
        return redirect(url_for(".results"))

    # track_event(category='Commute Tracked', action='commute tracked')
    return render_template('optimize.html')


# This creates the route for the fromhome data presentation page
@app.route('/results/fromhome/', methods = ['POST', 'GET'])
def fromhome():
    if request.method =="POST" and request.form['route']=='from work':
            return redirect(url_for(".fromwork"))
    return render_template("commutetowork.html", user_name = session['user_name'], labels=session['fh_labels'], plot_data=session['fh_commute_times'], statistics=session['fh_statistics'])

# This creates the route for the fromwork data presentation page
@app.route('/results/fromwork/', methods = ['POST', 'GET'])
def fromwork():
    if request.method =="POST" and request.form['route']=='from home':
            return redirect(url_for(".fromhome"))
    return render_template("commutefromwork.html", user_name = session['user_name'], labels=session['fw_labels'], plot_data=session['fw_commute_times'], statistics=session['fw_statistics'])

@app.route('/results/', methods = ['POST', 'GET'])
def results():
    # Interpret the arguments from the call to results to send to the desired 
    # args = request.args.get("args")
    if request.method =="POST":
        if request.form['route']=='from home':
            return redirect(url_for(".fromhome"))
        if request.form['route']=='from work':
            return redirect(url_for(".fromwork"))
    return render_template("choices.html")




if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=8080, host='0.0.0.0')
