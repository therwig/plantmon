import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import datetime
import numpy as np

def timeval(s):
    dt = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    return dt.timestamp()
    # return dt

with open('data/log.txt','r') as f:
    dat = [l.split() for l in f]

# date  = [x[0] for x in dat]
time  = [timeval(x[0]+" "+x[1]) for x in dat]
nsamp = [int(x[2]) for x in dat]
temp  = [float(x[3]) for x in dat]
tempe = [float(x[4]) for x in dat]
mois  = [float(x[5]) for x in dat]
moise = [float(x[6]) for x in dat]

for i in range(len(nsamp)):
    # tempe[i] = tempe[i]/np.sqrt(nsamp[i])
    # moise[i] = moise[i]/np.sqrt(nsamp[i])

    print(time[i], nsamp[i], temp[i], tempe[i], mois[i], moise[i])
