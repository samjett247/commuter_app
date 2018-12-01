import numpy as np

def gen_labels(time_range, time_int):

    t_int_minutes = 15

    # Build the from xvalues as a linear 
    # fh_x_vals = np.linspace(fh_time_range[0], fh_time_range[1], 6*fh_time_range[1]-fh_time_range[0])
    x_values = np.linspace(time_range[0], time_range[1], (time_range[1]-time_range[0])/(.25) + 1, endpoint = True)
    labels = []
    for lab in range(0, len(x_values)):
        print(x_values[lab])
        if x_values[lab]%1 ==0:        
            if x_values[lab]>=1 and x_values[lab]<24:
                if x_values[lab]<12:
                    labels.append(str(int(x_values[lab]))+' am')
                elif x_values[lab]==12:
                    labels.append(str(int(x_values[lab]))+ ' pm')
                else:
                    labels.append(str(int(x_values[lab]-12))+' pm')
            elif x_values[lab]<1:
                if x_values[lab]==0:
                    labels.append(str(int(x_values[lab]+12))+' am')
                else:  
                    labels.append(str(int(x_values[lab]+12))+' pm')
            else:
                if x_values[lab]==24:
                    labels.append(str(int(x_values[lab]-12))+' am')
                else:
                    labels.append(str(int(x_values[lab]-24))+' am')
        else:
            labels.append('')
    return labels
