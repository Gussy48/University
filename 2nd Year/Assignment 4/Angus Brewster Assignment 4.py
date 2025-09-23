import numpy as np
import matplotlib.pyplot as plt

# Defining time values

dt = 1                                                               # Time step for RK4 Differentiation
Numpoints = 1000000                                                  # Number of points for RK4 Differentiation
t = np.arange(0, Numpoints * dt, dt)                                 # Array for time values, for Numpoints amount in steps of dt

# Defining constants
G = 6.6743E-11                                                       # Gravitational constant
m_e = 5.97219E24                                                     # Mass of earth
m_m = 7.34767309E22                                                  # Mass of moon
x_moon = 384467E3                                                    # Distance of moon from earth, both in x plane
y_moon = 0                                                           # Y coord of moon, not really nescasary but could be useful for if the position needed to be changed.

def RK4 (t, x, y, vx, vy, dt, Numpoints, f1, f2, f3, f4, moon):
    """
    Calculates values according to Runge-Kutta derivative method

    Parameters
    ----------
    t : np array
        array of time values, Numpoints long in steps of dt
    x : np array
        initially full of zeros, calculated for x coords in plot.
    y : np array 
        initially full of zeros, calculated for y coords in plot.
    vx : TYPE
        velocity in x direction. initially full of zeros, calculated for RK4.
    vy : TYPE
        velocity in y direction. initially full of zeros, calculated for RK4.
    dt : int
        Time step for t array and RK4 calculation.
    Numpoints : int
        Number of times t values to calculate for.
    f1 : function
        provides information about impact of earth and moon on projectiles movement.
    f2 : function
        provides information about impact of earth and moon on projectiles movement.
    f3 : function
        provides information about impact of earth and moon on projectiles movement.
    f4 : function
        provides information about impact of earth and moon on projectiles movement.
    moon : Boolean
        States wether or not the moon is accounted for in the calculation.

    Returns
    -------
    x : np array
        x coordinates of projectile.
    y : np array 
        y coordinates of projectile.

    """
    i = 0                                                            # Index for iteration over
    dots_printed = 0                                                 # Index for progress bar
    print("Calculating trajectory ", end='')                         # Statement to show input has been recieved
    while i < Numpoints - 1:                                         # Repeat for Numpoints number of values
        if i % int(Numpoints / 84) == 0:                             # Prints progress bar, same width as menu
            print("█", end='')
            dots_printed += 1

        # Runge Kutta 4th order
        k1x = f1(t[i], x[i], y[i], vx[i], vy[i])
        k1y = f2(t[i], x[i], y[i], vx[i], vy[i])
        k1vx = f3(t[i], x[i], y[i], vx[i], vy[i])
        k1vy = f4(t[i], x[i], y[i], vx[i], vy[i])

        k2x = f1(t[i] + dt/2, x[i] + dt*k1x/2, y[i] + dt*k1y/2, vx[i] + dt*k1vx/2, vy[i] + dt*k1vy/2)
        k2y = f2(t[i] + dt/2, x[i] + dt*k1x/2, y[i] + dt*k1y/2, vx[i] + dt*k1vx/2, vy[i] + dt*k1vy/2)
        k2vx = f3(t[i] + dt/2, x[i] + dt*k1x/2, y[i] + dt*k1y/2, vx[i] + dt*k1vx/2, vy[i] + dt*k1vy/2)
        k2vy = f4(t[i] + dt/2, x[i] + dt*k1x/2, y[i] + dt*k1y/2, vx[i] + dt*k1vx/2, vy[i] + dt*k1vy/2)
        
        k3x = f1(t[i] + dt/2, x[i] + dt*k2x/2, y[i] + dt*k2y/2, vx[i] + dt*k2vx/2, vy[i] + dt*k2vy/2)
        k3y = f2(t[i] + dt/2, x[i] + dt*k2x/2, y[i] + dt*k2y/2, vx[i] + dt*k2vx/2, vy[i] + dt*k2vy/2)
        k3vx = f3(t[i] + dt/2, x[i] + dt*k2x/2, y[i] + dt*k2y/2, vx[i] + dt*k2vx/2, vy[i] + dt*k2vy/2)
        k3vy = f4(t[i] + dt/2, x[i] + dt*k2x/2, y[i] + dt*k2y/2, vx[i] + dt*k2vx/2, vy[i] + dt*k2vy/2)
        
        k4x = f1(t[i] + dt, x[i] + dt*k3x, y[i] + dt*k3y, vx[i] + dt*k3vx, vy[i] + dt*k3vy)
        k4y = f2(t[i] + dt, x[i] + dt*k3x, y[i] + dt*k3y, vx[i] + dt*k3vx, vy[i] + dt*k3vy)
        k4vx = f3(t[i] + dt, x[i] + dt*k3x, y[i] + dt*k3y, vx[i] + dt*k3vx, vy[i] + dt*k3vy)
        k4vy = f4(t[i] + dt, x[i] + dt*k3x, y[i] + dt*k3y, vx[i] + dt*k3vx, vy[i] + dt*k3vy)

        x[i+1] = x[i] + dt/6 * (k1x + 2*k2x + 2*k3x + k4x)
        y[i+1] = y[i] + dt/6 * (k1y + 2*k2y + 2*k3y + k4y)           # Assign calculated values to array
        vx[i+1] = vx[i] + dt/6 * (k1vx + 2*k2vx + 2*k3vx + k4vx)
        vy[i+1] = vy[i] + dt/6 * (k1vy + 2*k2vy + 2*k3vy + k4vy)

        if np.sqrt(x[i+1]**2 + y[i+1]**2) < 6371E3:                  # If rocket is within earth radius, fill rest of progress bar, and exit loop
            print((85-dots_printed) * "█")
            print("\033[1;32mRocket returned to earth, trajectory calculation stoppped.\x1b[0m",end='')
            print("\nThe journey took", dt * i, "s",end="")
            break
            
        elif moon == True:                                           # If rocket is within moon radius, fill rest of progress bar, and exit loop
            if np.sqrt((x[i + 1] - x_moon) ** 2 + (y[i + 1] - y_moon) ** 2) < 1:
                print((85-dots_printed) * "█")
                print("\033[1;40mRocket collided with celestial body\x1b[0m",end='')
                break
            
        i += 1                                                       # Progress index by 1
        
    print("\nDone!")
    #E_loss = 0
    #for a in range(0, Numpoints-1):
    #    E_loss += abs((0.5 * (vx[a]**2 + vy[0]**2)) + (-G * m_e / (x[a]**2 + y[a]**2)**0.5) + (-G * m_m / ((x[a] - x_moon)**2 + (y[a] - y_moon)**2)**0.5) - (0.5 * (vx[a + 1]**2 + vy[0]**2)) + (-G * m_e / (x[a + 1]**2 + y[a + 1]**2)**0.5) + (-G * m_m / ((x[a + 1] - x_moon)**2 + (y[a + 1] - y_moon)**2)**0.5))
    #print(E_loss)
    #E_ini = (0.5 * (vx[0]**2 + vy[0]**2)) + (-G * m_e / (x[0]**2 + y[0]**2)**0.5) + (-G * m_m / ((x[0] - x_moon)**2 + (y[0] - y_moon)**2)**0.5)    # indicate end of iterations
    #E_fin = (0.5 * (vx[i]**2 + vy[i]**2)) + (-G * m_e / (x[i]**2 + y[i]**2)**0.5) + (-G * m_m / ((x[i] - x_moon)**2 + (y[i] - y_moon)**2)**0.5)
    #print("Initial Energy:", E_ini)
    #print("Final Energy:  ", E_fin)
    #print("Energy lost:   ", E_ini - E_fin)
    #print("% Energy Lost: ", (E_loss) * 100 / E_ini)
    return x, y                                                      # Returns x and y for plotting

def ISSOrbit (t, G, m_e, dt, Numpoints, x0, y0, vx0, vy0):
    """
    

    Parameters
    ----------
    t : np array
        array of time values, Numpoints long in steps of dt
    G : float
        value of gravitational constant.
    m_e : float
        value of earths mass.
    dt : float
        time step in calculations.
    Numpoints : int
        Number of times t values to calculate for.
    x0 : float
        initial x position of projectile.
    y0 : float
        intiail y position of projectile.
    vx0 : float
        initial x velocity of projectile.
    vy0 : float
        initial y velocity of projectile.

    Returns
    -------
    Graph (matplotlib)
        plot of projectile trajectory for a projectile around the earth.

    """
    x = np.zeros(Numpoints)
    y = np.zeros(Numpoints)                                          # Set all arrays as zeros of length Numpoints,
    vx = np.zeros(Numpoints)                                         # Must be local in order not to interfere with other funcitons of the program
    vy = np.zeros(Numpoints)
    x[0] = x0
    y[0] = y0                                                        # Sets initial values of arrays
    vx[0] = vx0
    vy[0] = vy0
    def f1(t, x, y, vx, vy): #make more effiecient?
        return vx

    def f2(t, x, y, vx, vy):
        return vy

    def f3(t, x, y, vx, vy):
        return (-G * m_e * x) / ((x**2 + y**2)**(3/2))

    def f4(t,x,y,vx,vy):
        return (-G * m_e * y) / ((x**2 + y**2)**(3/2))
    
    RK4(t, x, y, vx, vy, dt, Numpoints, f1, f2, f3, f4, False)       # Calls RK4 function with relevent parameters
    
    # initiate plotting
    fig,(ax1) = plt.subplots()
    
    #setup subplot ax1 with title, labels, plot of earth and x,y
    ax1.set(xlabel = 'X Coordinate, relative to the Earth (m)', ylabel = 'Y Coordinate, relative to the Earth (m)', title = 'Trajectory of ISS')
    ax1.imshow(plt.imread('earth.png'), extent = [-6378100, 6378100, -6378100, 6378100],aspect="equal")
    ax1.plot(x, y)
    
    #plot whole graph
    plt.show()
    

def RocketOrbit(t, G, m_e, m_m, dt, Numpoints, x0, y0, vx0, vy0):
    """
    

    Parameters
    ----------
    t : np array
        array of time values, Numpoints long in steps of dt
    G : float
        value of gravitational constant.
    m_e : float
        value of earths mass.
    m_m : float
        value of moons mass.
    dt : float
        time step in calculations.
    Numpoints : int
        Number of times t values to calculate for.
    x0 : float
        initial x position of projectile.
    y0 : float
        intiail y position of projectile.
    vx0 : float
        initial x velocity of projectile.
    vy0 : float
        initial y velocity of projectile.

    Returns
    -------
    Graph (matplotlib)
        plot of projectile trajectory for a projectile interacting with the earth and moons graviational pull.

    """
    x = np.zeros(Numpoints)
    y = np.zeros(Numpoints)                                          # Set all arrays as zeros of length Numpoints,
    vx = np.zeros(Numpoints)                                         # Must be local in order not to interfere with other funcitons of the program
    vy = np.zeros(Numpoints)
    x[0] = x0
    y[0] = y0                                                        # Sets initial values of arrays
    vx[0] = vx0
    vy[0] = vy0
    def f1(t, x, y, vx, vy):
        return vx

    def f2(t, x, y, vx, vy):    
        return vy

    def f3(t, x, y, vx, vy):
        return ((-m_e * G * x) / ((x**2 + y**2)**(3/2))) + ((-m_m * G * (x - x_moon)) / (((x - x_moon)**2 + (y - y_moon)**2)**(3/2)))

    def f4(t,x,y,vx,vy):
        return ((-m_e * G * y) / ((x**2 + y**2)**(3/2))) + ((-m_m * G * (y - y_moon)) / (((x - x_moon)**2 + (y - y_moon)**2)**(3/2)))
        

    RK4(t, x, y, vx, vy, dt, Numpoints, f1, f2, f3, f4, True)        # Call RK4 function with relevent parameters
    
    #initiate plotting
    fig, (ax1) = plt.subplots(figsize=(10, 10))
    
    # ax1 subplot set up with title, labels, moon and earth plotted to scale, x vs y for rocket plotted
    ax1.set(xlabel = 'X Coordinate, relative to the Earth (m)', ylabel = 'Y Coordinate, relative to the Earth (m)', title = 'Trajectory of Rocket')
    ax1.plot(x, y)
    ax1.imshow(plt.imread('earth.png'), extent=[-6378100, 6378100, -6378100, 6378100])
    ax1.imshow(plt.imread('moon.png'), extent=[x_moon - 1737400, x_moon + 1737400, y_moon - 1737400, y_moon + 1737400])
    
    # inset axis setup for title, labels, limits, position of plot, plot of x,y and moon
    axins = ax1.inset_axes([0.79, 0, 0.25, 0.25])
    axins.plot(x, y)
    axins.imshow(plt.imread('moon.png'), extent=[x_moon - 1737400, x_moon + 1737400, y_moon - 1737400, y_moon + 1737400])
    axins.set_title("Zoomed View of the Moon", fontsize=7)
    axins.set_xlim(x_moon - 1E7, x_moon + 1E7)
    axins.set_ylim(y_moon - 1E7, y_moon + 1E7)
    axins.set_aspect('equal')
    
    # Hide the axis labels
    axins.get_xaxis().set_visible(False)
    axins.get_yaxis().set_visible(False)
    ax1.set_xlim(-1E8, x_moon + 1E8)
    ax1.set_ylim(-2E8, 2E8)
    
    # plot whole graph
    plt.show()

def Menu():
    """
    Menu function
    
    
    Sends user to correct function in program or quits, has input checking implemented
    
    """
    
    # takes input for menu function
    Input = input("""|-----------------------------------------------------------------------------------------------------------|
|                                            Choose your function                                           |
|-----------------------------------------------------------------------------------------------------------|
| For a simulation of the ISS orbit, type "a"                                                               |
| For a simulation of a rocket launching from earth orbit, orbiting the moon and passing by earth, type "b" |
| For a simulation of a rocket launching from the earth, orbiting the moon and returning to earth, type "c" |
| For a simulation of a rocket, with initial conditions of your choice, type "d"                            |
| To quit, type "q"                                                                                         |
|-----------------------------------------------------------------------------------------------------------|""")

    # send user to correct part of program and return to menu once complete
    if Input == "a":
        ISSOrbit(t, G, m_e, dt, Numpoints, 0, 6600E3, 7823.2, 0)
        Menu()
    elif Input == "b":
        RocketOrbit(t, G, m_e, m_m, dt, Numpoints, -6371E3-6.5E6, 0, 0, 7745.6)
        Menu()
    elif Input == "c":
        RocketOrbit(t, G, m_e, m_m, dt, Numpoints, -6371E3, 0, 0, 11096)
        Menu()
    elif Input == "d":
        # define error message for input checking
        ErrMsg = """\033[0;41;30m|                                      Please input an decimal value.                                       |\x1b[0m
|-----------------------------------------------------------------------------------------------------------|"""
        while True:   # checks input value for x0, sends error if not an integer, uses default if nothing is input
            try:
                x0 = float(input("""|                            Please input the initial x coordinate of the rocket.                           |
|                                 (press enter for default number, 6371000)                                 |
|-----------------------------------------------------------------------------------------------------------|""").strip() or 6371E3)    
                break
            except ValueError:
                print(ErrMsg)        
                
        while True:   # checks input value for y0, sends error if not an integer, uses default if nothing is input    
            try:
                y0 = float(input("""|                            Please input the initial y coordinate of the rocket.                           |
|                                    (press enter for default number, 0)                                    |
|-----------------------------------------------------------------------------------------------------------|""").strip() or 0)    
                break
            except ValueError:
                print(ErrMsg)   
        
        while True:   # checks input value for vx0, sends error if not an integer, uses default if nothing is input
            try:
                vx0 = float(input("""|                             Please input the initial x velocity of the rocket.                            |
|                                  (press enter for default number, 11090)                                  |
|-----------------------------------------------------------------------------------------------------------|""").strip() or 11090)    
                break
            except ValueError:
                print(ErrMsg) 
        
        while True:   # checks input value for vy0, sends error if not an integer, uses default if nothing is input
            try:
                vy0 = float(input("""|                             Please input the initial y velocity of the rocket.                            |
|                                   (press enter for default number, 170)                                   |
|-----------------------------------------------------------------------------------------------------------|""").strip() or 170)    
                break
            except ValueError:
                print(ErrMsg)
        RocketOrbit(t, G, m_e, m_m, dt, Numpoints, x0, y0, vx0, vy0)
        Menu()      
        
    elif Input == "q":
        print("x================ Thank you for using this Runge-Kutta derivative orbit calculation program. ===============x")
        pass
    
    # prints error message if no valid input is given
    else:
        print('\033[0;41;30m|                                  Please input "a", "b", "c", "d", or "q"                                  |\x1b[0m')
        Menu()


# Warning message that some extra image files are needed
print('''\033[1;36;40m                   Please note, for this program, "earth.png" and "moon.png" need to be in                   
                   the same directory as the program, these have been emailed to Dr hannah.                  \033[0m
''')

# welcome message
print("x==================== Welcome to this Runge-Kutta derivative orbit calculation program. ====================x")

# Initiate the program with menu function
Menu()
