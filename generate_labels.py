def gen_labels(time_range, time_marker, time_int):

    t_int_minutes = int(time_int/60)

    # Build the from home (fh) xlabels from the time range
    # fh_x_vals = np.linspace(fh_time_range[0], fh_time_range[1], 6*fh_time_range[1]-fh_time_range[0])
    x_labels = (int((time_range[1]-time_range[0])*60/t_int_minutes)+1)*['']
    hour = time_range[0]

    for lab in range(0, len(x_labels)+1):
        if lab%int(60/t_int_minutes) ==0:
            if time_marker == 'am':
                x_labels[lab]=str(hour) + ' ' + time_marker
            else:
                x_labels[lab] = str(hour-12) + ' ' + time_marker
            hour=hour+1
            
    return x_labels