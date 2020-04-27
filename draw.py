import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import datetime
import numpy as np
import os
from time import strftime, localtime

def plot(x, _y, _avg, name, text='', xtitle='time', ytitle='', odir='plots/'):
    y, ye = _y[0], _y[1]
    avg, avge = _avg[0], _avg[1]
    
    plt.figure(figsize=(6,4))
    plt.errorbar(x=x, y=y, yerr=ye)
    plt.errorbar(x=x, y=avg, yerr=avge)
    ax = plt.gca()
    plt.text(0.1, 0.9, text, transform=ax.transAxes)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    # plt.locator_params(axis='x', nbins=4)
    plt.savefig(odir+"/"+name+".png")
    plt.close()
    return

def AvgErr(x):
    return np.sum( [i*i for i in x] ) / len(x)
def rebinTime(t, N):
    return [ np.average(t[i*N:(i+1)*N]) for i in range(int(len(t)/N))]
def rebin(y, ye, N):
    avg  = [ np.average(y[i*N:(i+1)*N]) for i in range(int(len(y)/N))]
    avge = [AvgErr(ye[i*N:(i+1)*N]) for i in range(int(len(y)/N))]
    return avg, avge

def rebinToN(y, ye, N):
    return rebin(y, ye, int(len(y)/N))
def rebinTimeToN(t, N):
    return rebinTime(t, int(len(t)/N))

def moving_average(x,d=5):
    a=[]
    for i in range(len(x)):
        if i<d:
            a.append( sum(x[0:i+1]) / (i+1.) )
        else:
            a.append( sum(x[i-d+1:i+1]) / d )
    return a

def get_avg(_x,d=5):
    e=max(1,int(d/2))
    x=_x[0].copy()
    x = np.insert(x,0,[x[0]]*e)
    x = np.append(x,[x[-1]]*e)
    a=[]
    for i in range(len(_x[0])):
        a.append( x[i:i+2*e+1].sum()/(2*e+1) )

    return np.vstack( [np.array(a),np.zeros_like(a)] )

#    PlotLast(seconds, time, temp, mois, avg_temp, avg_mois, sname, lname, odir)
def PlotLast(interval_sec, _time, _temp, _mois,
             _avg_temp, _avg_mois, prefix, label, odir,
             nbins=-1):
    latest = _time[-1]
    istart=0
    while(latest-_time[istart] > interval_sec): istart += 1
    time = _time [istart:]
    temp = _temp [:,istart:]
    mois = _mois [:,istart:]
    avg_temp = _avg_temp [:,istart:]
    avg_mois = _avg_mois [:,istart:]

    if nbins>0:
        time = rebinTimeToN(time, nbins)
        # temp, tempe = rebinToN(temp, tempe, nbins)
        # mois, moise = rebinToN(mois, moise, nbins)
        temp = np.vstack( rebinToN(temp[0], tempe[1], nbins) )
        mois = np.vstack( rebinToN(mois[0], moise[1], nbins) )
    time = (np.array(time) - time[-1]) / 60 # minutes from last data
    
    if interval_sec < 2*60*60:
        xtitle = "time (minutes)"
    elif interval_sec < 2*24*60*60:
        xtitle = "time (hours)"
        time /= 60
    else:
        xtitle = "time (days)"
        time /= (24*60)

    #latest_str = strftime("%Y-%m-%d %H:%M:%S", localtime(latest))
    latest_str = strftime("%H:%M:%S on %a %b %d, %Y", localtime(latest))
    os.system( 'echo "{}" > {}/{}.txt'.format(latest_str, odir, prefix) )
    plot(time, temp, avg_temp, prefix+"_temp", xtitle = xtitle, ytitle="Temperature [deg F]", text=label, odir=odir)
    plot(time, mois, avg_mois, prefix+"_mois", xtitle = xtitle, ytitle="Moisture content", text=label, odir=odir)

def getData(fname):        
    with open(fname,'r') as f:
        dat = [l.split() for l in f]
    
    time  = np.array([float(x[0])for x in dat] )
    nsamp = np.array([int(x[1]) for x in dat]  )
    temp  = np.array([float(x[2]) for x in dat])
    tempe = np.array([float(x[3]) for x in dat])
    mois  = np.array([float(x[4]) for x in dat])
    moise = np.array([float(x[5]) for x in dat])
    temp  = 9./5*temp+32.
    tempe = 9./5*tempe
    
    # convert rms -> error on mean
    for i in range(len(nsamp)):
        tempe[i] = tempe[i]/np.sqrt(nsamp[i])
        moise[i] = moise[i]/np.sqrt(nsamp[i])

    temp = np.vstack( [temp, tempe] )
    mois = np.vstack( [mois, moise] )
        
    return time, temp, mois, nsamp

#
# Get data

time, temp, mois, nsamp = getData('data/log.txt')

navg=5
avg_temp = get_avg(temp,navg)
avg_mois = get_avg(mois,navg)

timespans = [
    (31*24*60*60, "1mo", "Past month"),
    (7*24*60*60,  "1wk", "Past week"),
    (3*24*60*60,  "3day", "Past 3 days"),
    (24*60*60,    "24hr", "Past 24 hours"),
    ( 6*60*60,    "6hr", "Past 6 hours"),
]

#exit(0)
subdirs=['main','average','template']
for s in subdirs:
    odir="plots/"+s
    for seconds, sname, lname in timespans:
        PlotLast(seconds, time, temp, mois, avg_temp, avg_mois, sname, lname, odir)

# PlotLast(31*24*60*60, time, temp, tempe, mois, moise, trend_temp, trend_mois, "1mo", "Past month")
# PlotLast(7*24*60*60, time, temp, tempe, mois, moise, trend_temp, trend_mois, "1wk", "Past week")
# PlotLast(3*24*60*60, time, temp, tempe, mois, moise, trend_temp, trend_mois, "3day", "Past 3 days")
# PlotLast(24*60*60, time, temp, tempe, mois, moise, trend_temp, trend_mois, "24hr", "Past 24 hours")
# PlotLast( 6*60*60, time, temp, tempe, mois, moise, trend_temp, trend_mois, "6hr", "Past 6 hours")

# N=60
# time = rebinTimeToN(time , N)
# temp, tempe = rebinToN(temp, tempe, N)
# mois, moise = rebinToN(mois, moise, N)

# print(len(time), len(temp),len(tempe))
# print(len(time), len(mois),len(moise))

# print('plotting')
# plot(time, temp, tempe, "temp", ytitle="temp")
# plot(time, mois, moise, "mois", ytitle="moisture")


# plt.figure(figsize=(6,4))
# plt.errorbar(x=time, y=temp, yerr=tempe)
# ax = plt.gca()
# # plt.text(0.1, 0.9, name, transform=ax.transAxes)
# plt.xlabel('time')
# plt.ylabel('temp')
# plt.locator_params(axis='x', nbins=4)
# plt.savefig('plots/temp.png')
# plt.close()


# plt.figure(figsize=(6,4))
# plt.errorbar(x=time, y=mois, yerr=moise)
# ax = plt.gca()
# # plt.text(0.1, 0.9, name, transform=ax.transAxes)
# plt.xlabel('time')
# plt.ylabel('moisture')
# plt.savefig('plots/mois.png')
# plt.close()

# #print(time)



