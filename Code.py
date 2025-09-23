import numpy as np
import matplotlib.pyplot as plt


y0 = 39045 #  initial height
NumPoints = 1000 # number of points to iterate over

g = 9.81 # m/s^2, acceleration, for constant g
gvals = np.zeros(NumPoints) # blank array for calculation of g at different times

cd=1 # drag coefficient of skydiver
A=0.6 # area of sky diver in m
kvals = np.zeros(NumPoints) # empty array for calculation of k at different times


yvals = np.zeros(NumPoints)# empty array for calculation of y at different times
vyvals = np.zeros(NumPoints)# empty array for calculation of velocity at different times


rhovals=np.zeros(NumPoints)# empty array for calculating rho at different times
m=80 # mass of sky diver

rho0=1.2 # initial rho
k=cd*rho0*A/2 # intial k from initial rho
h=7640.0 # hvalue(given in task)


def Menu():
    """
    Menu function

    
    sends to the right function
    
    """
    Input = input("Would you like option a,b,c or q to quit.")#requests input for menu
    if Input == "a":#if a selected, run a function
        a()
    elif Input =="b":#if b selected, run b function
        b()
    elif Input =="c":#if c selected, run c function
        c()
    elif Input =="q":#if q selected do not repeat menu, effectively ends program
        pass
    else:
        print('please type "a", "b", "c" or "q"')#if any other inputs given, remind user of valid inputs and start menu again
        Menu()


#a)
def a():
    """
    calculates analytical solution to free-fall equations of motion and plots them on graphs of time Vs height and time Vs vertical velocity

    """
    tvals = np.linspace(0,30,NumPoints)#creates array for NumPoints amount of values of t evenly spaced between 0 and 30
    yvals[0]=1000 #defines start height
    for i in range(NumPoints-1):#calculates values for each t
        yvals[i]=1000 - ((m/k)*np.log(np.cosh(np.sqrt(k*g/m)*tvals[i]))) #calculates y value for t
        vyvals[i]=-np.sqrt(m*g/k)*np.tanh(np.sqrt(k*g/m)*tvals[i])#calculates vy for each t
        if yvals[i]<=0: #prevent velocity from being nonzero after colision with the ground.
            vyvals[i],vyvals[i+1]=0,0
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(12,4)) #create 2 axis in one plot
    fig.suptitle('Altitude and Vertical Velocity graphs solved analyticaly.') #titles overall plot
    ax1.set(xlabel='Time (s)', ylabel='Height (m)', title='Altitude') #sets title and axis titles for first graph
    ax2.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='Vertical Velocity')#sets title and axis titles for second graph
    ax1.plot(tvals,np.maximum(yvals,0),'tab:red')#plots graph of time Vs height, guarenteeing the height cannot go below 0
    ax2.plot(tvals,vyvals,'tab:green')#plots time Vs Vertical velocity of diver
    plt.show()#shows the graphs
    Menu()#return to menu function




#b)
def b():
    """
    calculates and plots Height and Vertical velocity for different time values using euler method from a height of 1km

    """
    yvals[0]=1000#set initial height
    tvals = np.linspace(0,30,NumPoints)#creates array for NumPoints amount of values of t evenly spaced between 0 and 30
    dt=(30)/NumPoints#calculates the time step for that resolution
    for i in range(NumPoints-1):#calculates values for each t
        gvals[i]=(6.67430E-11)*((5.9722e24)/((6371e3)+yvals[i])**2)#calculates value of g per time
        vyvals[i+1] = vyvals[i]-dt*(gvals[i]+((k/m)*np.abs(vyvals[i])*vyvals[i]))#calculates velocity value per time
        if yvals[i]<=0:#guarentee height is never non zero and when it is, the velocity is also zero
            vyvals[i],vyvals[i+1]=0,0
        yvals[i+1] = yvals[i]+dt*vyvals[i]#calculates height for each time value
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(12,4))#create 2 axis in one plot
    fig.suptitle("Altitude and Vertical Velocity graphs solved using Euler's method.")#titles overall plot
    ax1.set(xlabel='Time (s)', ylabel='Height (m)', title='Altitude')#sets title and axis titles for first graph
    ax2.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='Vertical Velocity')#sets title and axis titles for second graph
    ax1.plot(tvals,np.maximum(yvals,0),'tab:red')#plots graph of time Vs height, guarenteeing the height cannot go below 0
    ax2.plot(tvals,vyvals,'tab:green')#plots time Vs Vertical velocity of diver
    plt.show()#shows the graphs
    Menu()#return to menu function

#c)
def c():
    """
    calculates and plots Height and Vertical velocity for different time values using euler method for actual values from Baumgartner

    """
    time=500#variable to choose time axis length
    tvals = np.linspace(0,time,NumPoints)#creates array for NumPoints amount of values of t evenly spaced between 0 and time value
    dt=(time)/NumPoints#calculates the time step for that resolution
    yvals[0]=y0#set initial height to y0 (defined earlier)
    for i in range(NumPoints-1):#calculates values for each t
        rhovals[i]=rho0*np.exp(-yvals[i]/h)#calculates rho for each t
        kvals[i]=cd*rhovals[i]*A/2#calculates k for each t
        gvals[i]=(6.67430E-11)*((5.9722e24)/((6371e3)+yvals[i])**2)#calculates g for each t
        vyvals[i+1] = vyvals[i]-dt*(gvals[i]+((kvals[i]/m)*np.abs(vyvals[i])*vyvals[i]))#calculates velocity for each t
        if yvals[i]<=0:#guarentee height is not below 0
            vyvals[i],vyvals[i+1]=0,0
        yvals[i+1] = yvals[i]+dt*vyvals[i]#calculate height per t
    
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(12,4))#create 2 axis in one plot
    fig.suptitle("Altitude and Vertical Velocity graphs solved using Euler's method for Baumgartner's jump.")#titles overall plot
    ax1.set(xlabel='Time (s)', ylabel='Height (m)', title='Altitude')#sets title and axis titles for first graph
    ax2.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='Vertical Velocity')#sets title and axis titles for second graph
    ax1.plot(tvals,np.maximum(yvals,0),'tab:red')#plots graph of time Vs height, guarenteeing the height cannot go below 0
    ax2.plot(tvals,vyvals,'tab:green')#plots time Vs Vertical velocity of diver
    
    
    yiszero = np.where(yvals <= 0)[0]#finds first value when height could go below zero
    ax1.axvline(x=tvals[yiszero[0]],linestyle = 'dashed')#plots line perpendicular to x axis
    ax1.annotate(f'time=: {tvals[yiszero[0]]:.2f} s',xy=(tvals[yiszero[0]], 0), xytext=(tvals[yiszero[0]]-80, y0-300),bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))#annotates the line with a box stating the x value
    
    max_y=np.min(vyvals)#calculates the maxmimum negative velocity
    max_x=tvals[np.argmin(vyvals)]
    ax2.scatter(max_x,max_y)#plots maximum negative velocity
    ax2.annotate(f'Min: {max_y:.2f} m/s', xy=(max_x, max_y), xytext=(max_x + 50, max_y+4),arrowprops=dict(facecolor='black', shrink=0.05),)#labels the maximum velocity point
    plt.show() # shows the graphs
    Menu()#returns to menu function




#The folowing graphs were not nescesary for the asignment but used to make the report me legible and as such are not optimised for efficiency and must be run by selecting them (not accessible from the menu) 




def cvaryingm():
    """
    calculates and plots Height and Vertical velocity for different time values using euler method for actual values from Baumgartner  as his mass is varied
    """
    time=500#variable to choose time axis length
    masses=[40,60,80,100,120]#choose masses we want to plot on the graphs
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(12,4))#create 2 axis in one plot
    fig.suptitle("Altitude and Vertical Velocity graphs solved using Euler's method for Baumgartner's jump.")#titles overall plot
    ax1.set(xlabel='Time (s)', ylabel='Height (m)', title='Altitude')#sets title and axis titles for first graph
    ax2.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='Vertical Velocity')#sets title and axis titles for second graph
    for mass in masses:#calculates values for each mass
        tvals = np.linspace(0,time,NumPoints)#creates array for NumPoints amount of values of t evenly spaced between 0 and time value
        dt=(time)/NumPoints#calculates the time step for that resolution
        yvals[0]=y0#set initial height to y0 (defined earlier)
        for i in range(NumPoints-1):#calculates values for each t
            rhovals[i]=rho0*np.exp(-yvals[i]/h)#calculates rho for each t
            kvals[i]=cd*rhovals[i]*A/2#calculates k for each t
            gvals[i]=(6.67430E-11)*((5.9722e24)/((6371e3)+yvals[i])**2)#calculates g for each t
            vyvals[i+1] = vyvals[i]-dt*(gvals[i]+((kvals[i]/mass)*np.abs(vyvals[i])*vyvals[i]))#calculates velocity for each t
            if yvals[i]<=0:#guarentee height is not below 0
                vyvals[i],vyvals[i+1]=0,0
            yvals[i+1] = yvals[i]+dt*vyvals[i]#calculate height per t
        ax1.plot(tvals, np.maximum(yvals, 0), label=f'Mass = {mass}')#plots graph of time Vs height, guarenteeing the height cannot go below 0, for each mass
        ax1.legend()#shows all the plots on axis one
        ax2.plot(tvals,vyvals)#plots time Vs Vertical velocity of diver for each mass
        
    plt.show() #shows plot
    
def cvaryingy0():
    """
    calculates and plots Height and Vertical velocity for different time values using euler method for actual values from Baumgartner  as his initial height is varied

    """
    time=500#variable to choose time axis lengt
    heights=[20000,30000,40000,50000,60000]#choose heights we want to plot on the graphs
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(12,4))#create 2 axis in one plot
    fig.suptitle("Altitude and Vertical Velocity graphs solved using Euler's method for Baumgartner's jump.")#titles overall plot
    ax1.set(xlabel='Time (s)', ylabel='Height (m)', title='Altitude')#sets title and axis titles for first graph
    ax2.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='Vertical Velocity')#sets title and axis titles for second graph
    for height in heights:#calculates values for each height
        tvals = np.linspace(0,time,NumPoints)#creates array for NumPoints amount of values of t evenly spaced between 0 and time value
        dt=(time)/NumPoints#calculates the time step for that resolution
        yvals[0]=height#set initial height to y0 (defined earlier)
        for i in range(NumPoints-1):#calculates values for each t
            rhovals[i]=rho0*np.exp(-yvals[i]/h)#calculates rho for each t
            kvals[i]=cd*rhovals[i]*A/2#calculates k for each t
            gvals[i]=(6.67430E-11)*((5.9722e24)/((6371e3)+yvals[i])**2)#calculates g for each t
            vyvals[i+1] = vyvals[i]-dt*(gvals[i]+((kvals[i]/m)*np.abs(vyvals[i])*vyvals[i]))#calculates velocity for each t
            if yvals[i]<=0:#guarentee height is not below 0
                vyvals[i],vyvals[i+1]=0,0
            yvals[i+1] = yvals[i]+dt*vyvals[i]#calculate height per t
        ax1.plot(tvals, np.maximum(yvals, 0), label=f'Height = {height}')#plots graph of time Vs height, guarenteeing the height cannot go below 0, for each height
        ax1.legend()#shows all the plots on axis one
        ax2.plot(tvals,vyvals)#plots time Vs Vertical velocity of diver for each height
        
    plt.show()#shows plot


def bvart():
    """
    calculates and plots Height and Vertical velocity for different time values using euler method from a height of 1km for different resolutions

    """
    resolutions=[10,30,50,70,100]#sets resolutions we want
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(12,4))#create 2 axis in one plot
    fig.suptitle("Altitude and Vertical Velocity graphs solved using Euler's method.")#titles overall plot
    ax1.set(xlabel='Time (s)', ylabel='Height (m)', title='Altitude')#sets title and axis titles for first graph
    ax2.set(xlabel='Time (s)', ylabel='Speed (m/s)', title='Vertical Velocity')#sets title and axis titles for second graph
    for resolution in resolutions:#calculates values for each resolution
        gvals1 = np.zeros(resolution)#makes local variable equivalent of gval
        yvals1 = np.zeros(resolution)#makes local variable equivalent of yvals
        vyvals1 = np.zeros(resolution)#makes local variable equivalent of vyvals
        yvals1[0]=1000#set initial height to 1km
        tvals1 = np.linspace(0,30,resolution)#creates array for NumPoints amount of values of t evenly spaced between 0 and time value
        dt=(30)/resolution#calculates the time step for that resolution
        for i in range(resolution-1):#calculates values for each resolution
            gvals1[i]=(6.67430E-11)*((5.9722e24)/((6371e3)+yvals1[i])**2)#calculates g for each t
            vyvals1[i+1] = vyvals1[i]-dt*(gvals1[i]+((k/m)*np.abs(vyvals1[i])*vyvals1[i]))#calculates velocity for each t
            if yvals1[i]<=0:#guarentee height is not below 0
                vyvals1[i],vyvals1[i+1]=0,0
            yvals1[i+1] = yvals1[i]+dt*vyvals1[i]
        ax1.plot(tvals1, np.maximum(yvals1, 0), label=f'Resolution = {resolution}')#plots graph of time Vs height, guarenteeing the height cannot go below 0, for each resolution
        ax1.legend()#shows all the plots on axis one
        ax2.plot(tvals1,vyvals1)#plots time Vs Vertical velocity of diver for each resolution
    plt.show()#shows plot



bvart()
Menu()#initiates program by running menu function