import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import datetime
import numpy as np
import os
from time import strftime, localtime

def plot(x, y, ye, avg, name, text='', xtitle='time', ytitle=''):
    plt.figure(figsize=(6,4))
    plt.errorbar(x=x, y=y, yerr=ye)
    #plt.errorbar(x=x, y=avg, yerr=np.zeros_like(avg))
    ax = plt.gca()
    plt.text(0.1, 0.9, text, transform=ax.transAxes)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    # plt.locator_params(axis='x', nbins=4)
    plt.savefig("plots/"+name+".png")
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

def moving_average(a, n=3) :
    x=a.copy()
    c = np.cumsum(a, dtype=float)
    for i in range(len(a)):
        x[i] = (c[i]-c[max(i-n,0)])/min(n,i+1)
    x[0]=a[0]
    for i in range(n):
        x[i]=a[:i].sum()/(i+1)
        
    return x

def PlotLast(interval, _time, _temp, _tempe, _mois, _moise,
             _trend_temp, _trend_mois, prefix, label, nbins=-1):
    latest = _time[-1]
    istart=0
    while(latest-_time[istart] > interval): istart += 1
    time = _time [istart:]
    temp = _temp [istart:]
    tempe= _tempe[istart:]
    mois = _mois [istart:]
    moise= _moise[istart:]
    trend_temp = _trend_temp [istart:]
    trend_mois = _trend_mois [istart:]

    if nbins>0:
        time = rebinTimeToN(time, nbins)
        temp, tempe = rebinToN(temp, tempe, nbins)
        mois, moise = rebinToN(mois, moise, nbins)
    time = (np.array(time) - time[-1]) / 60 # minutes from last data
    
    if interval < 2*60*60:
        xtitle = "time (minutes)"
    elif interval < 2*24*60*60:
        xtitle = "time (hours)"
        time /= 60
    else:
        xtitle = "time (days)"
        time /= (24*60)

    #latest_str = strftime("%Y-%m-%d %H:%M:%S", localtime(latest))
    latest_str = strftime("%H:%M:%S on %a %b %d, %Y", localtime(latest))
    os.system( 'echo "{}" > plots/{}.txt'.format(latest_str, prefix) )
    plot(time, temp, tempe, trend_temp, prefix+"_temp", xtitle=xtitle, ytitle="Temperature [deg F]", text=label)
    plot(time, mois, moise, trend_mois, prefix+"_mois", xtitle=xtitle, ytitle="Moisture content", text=label)

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

    # unit is unix time "time.time()"
    # time = [localtime(t) for t in time]
    # # time.localtime()        
    # print( 'first times:', time[:3])
    # print( 'last times:', time[-3:])
    # exit(0)
    return time, nsamp, temp, tempe, mois, moise

time, nsamp, temp, tempe, mois, moise = getData('data/log.txt')

navg=5
trend_temp = moving_average(temp,navg)
trend_mois = moving_average(mois,navg)
# print(len(trend_temp), len(temp))

PlotLast(31*24*60*60, time, temp, tempe, mois, moise, trend_temp, trend_mois, "1mo", "Past month")
PlotLast(7*24*60*60, time, temp, tempe, mois, moise, trend_temp, trend_mois, "1wk", "Past week")
PlotLast(3*24*60*60, time, temp, tempe, mois, moise, trend_temp, trend_mois, "3day", "Past 3 days")
PlotLast(24*60*60, time, temp, tempe, mois, moise, trend_temp, trend_mois, "24hr", "Past 24 hours")
PlotLast( 6*60*60, time, temp, tempe, mois, moise, trend_temp, trend_mois, "6hr", "Past 6 hours")

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



