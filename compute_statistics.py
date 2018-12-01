
def compute_statistics(commute_times, labels):
    '''
    This function will take the commute_times for a given route and the labels for that route to return the parameters:
    (1) Best Commute Departure Time
    (2) Commute Time at Best Departure Time
    (3) Worst Commute Departure Time
    (4) Commute Time at Worst Departure Time
    (5) Weekly Time Savings in given route

    :param commute_times: n length list of commute times in minutes
    :param labels: n length list of labels in time units
    :return: 5 parameters shown above, in tuple form, indexed as shown above
    '''
    import numpy as np
    import sys
    # Convert to numpy array
    commute_times = np.array(commute_times)

    # Find best commute times and ind
    best_depart_ind = np.argmin(commute_times)
    best_commute = np.min(commute_times)

    # Find worst commute times and ind
    worst_depart_ind = np.argmax(commute_times)
    worst_commute = np.max(commute_times)

    depart_times = [] # Best then worst

    # Map the differences to minute values
    diff_map = {1:"45", 2:"30",3:"15"}

    # DEBUGGING
    print("The best depart ind is "+ str(best_depart_ind))
    print("The worst depart ind is " + str(worst_depart_ind))
    print("The labels are ")
    print(labels)
    
    # Find labels for best/worst departure times
    for i in [best_depart_ind, worst_depart_ind]:
        depart_time = labels[i]
        diff=0
        if depart_time == "" or len(depart_time)>5:
            new_i = i
            while depart_time == "" or len(depart_time)>5:
                diff = diff+1
                new_i = new_i+1
                depart_time = labels[new_i]
            new_lab = labels[new_i-4]
            print(new_lab)
            print(len(new_lab))
            # This reconstructs the proper label for the based on the difference in indices
            if len(new_lab)==4:
                depart_time=new_lab[0]+':'+diff_map[diff] + new_lab[-3:]
            elif len(new_lab)==5:
                depart_time=new_lab[0:2]+':'+diff_map[diff] + new_lab[-3:]
            else:
                depart_time = "Error Computing Statistics"
        depart_times.append(depart_time)

    # Compute weekly savings
    weekly_savings = (worst_commute-best_commute)*5

    return (depart_times[0], str(int(round(best_commute))), depart_times[1], str(int(round(worst_commute))), str(int(round(weekly_savings))))
