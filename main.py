
from flask import Flask, render_template, request, send_from_directory
import numpy as np

from gmaps_api_call import obtain_commute_times
from generate_labels import gen_labels
from compute_statistics import compute_statistics
import os
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

# @app.route('/articles')
# def articles():
#     return render_template('articles.html', articles= Articles)

@app.route('/optimize', methods = ['POST', 'GET'])
def optimize_commute():
    # Define data
    legend = 'How much Zach is a good boy for Santa'
    print(request.form)
    if request.method == 'POST' and request.form.get('home_addr')!= None:
        # Create global variables based on users defined name and addresses
        global user_name, home_addr, work_addr
        user_name = request.form['user_name']
        home_addr = request.form['home_addr']
        work_addr = request.form['work_addr']

        # Call the google API to get the route info for the person
        # Call api to get  commute times
        global fh_commute_times, fw_commute_times
        fh_commute_times = obtain_commute_times(home_addr, work_addr, fh_time_range, time_int)
        fw_commute_times = obtain_commute_times(work_addr, home_addr, fw_time_range, time_int)

        # Generate the labels for both cases
        global fh_labels, fw_labels
        fh_labels = gen_labels(fh_time_range, 'am', time_int)
        fw_labels = gen_labels(fw_time_range, 'pm', time_int)

        # Compute statistics for both cases
        global fh_statistics, fw_statistics
        fh_statistics = compute_statistics(fh_commute_times, fh_labels)
        fw_statistics = compute_statistics(fw_commute_times, fw_labels)

        return render_template('choices.html')

    elif request.method == 'POST' and request.form.get('route') != None:
        if request.form['route']=='from home':
            return render_template('commutetowork.html', user_name = user_name, labels=fh_labels, plot_data=fh_commute_times, statistics=fh_statistics)

        elif request.form['route']=='from work':
            return render_template('commutefromwork.html', user_name=user_name, labels=fw_labels, plot_data=fw_commute_times, statistics=fw_statistics)
    # track_event(category='Commute Tracked', action='commute tracked')
    return render_template('optimize.html')


@app.route('/result', methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("results.html",result = result)


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')