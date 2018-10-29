
from flask import Flask, render_template, request
import numpy as np

from gmaps_api_call import obtain_commute_times
from generate_labels import gen_labels

# From home (fh) time range
fh_time_range = (6,9)

# From work (fw) time range
fw_time_range = (15,18)

# Define the time intervals of the predictions (in seconds)
time_int = 900 # Seconds


from data import articles
from sam import my_name
from datetime import time

# Create app variable
app = Flask(__name__)


# Create route for the app

@app.route('/')
def index():
    # Return the template
    return render_template('home.html')

@app.route('/about')
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
        # Call api to get from home commute times
        global fh_commute_times, fw_commute_times
        fh_commute_times = obtain_commute_times(home_addr, work_addr, fh_time_range, time_int)
        fw_commute_times = obtain_commute_times(work_addr, home_addr, fw_time_range, time_int)

        # Generate the labels for both cases
        global fh_labels, fw_labels
        fh_labels = gen_labels(fh_time_range, 'am', time_int)
        fw_labels = gen_labels(fw_time_range, 'pm', time_int)

        #

        return render_template('choices.html')

    elif request.method == 'POST' and request.form.get('route') != None:
        if request.form['route']=='from home':
            return render_template('commutetowork.html', user_name = user_name, labels=fh_labels, plot_data=fh_commute_times)

        elif request.form['route']=='from work':
            return render_template('commutefromwork.html', user_name=user_name, labels=fw_labels, plot_data=fw_commute_times)

    return render_template('optimize.html')


@app.route('/result', methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("results.html",result = result)


if __name__ == "__main__":
    app.run(debug=True, port=5002)