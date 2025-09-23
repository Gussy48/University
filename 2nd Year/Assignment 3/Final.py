#importing modules
import scipy
import numpy as np
import matplotlib.pyplot as plt



#defining variables

WaveLength=1E-6  #wavelength of the light
k=2*(scipy.pi/WaveLength)  #wave number, equal to 2pi times the reciprocol of the wavelength
E_0=1.0


def ChangeVars():
    """
    Defines Variables dependent on the input of the user

    RETURNS
    values for NumPoints, z, ApertureWidth,xprime_1,yprime_1,xprime_2,yprime_2,xArray,yArray,E1d,E2d,k

    """
    global NumPoints, z, ApertureWidth,xprime_1,yprime_1,xprime_2,yprime_2,xArray,yArray,E1d,E2d,k
    while True:   #takes user input for value for NumPoints variable, repeats until a valid input is given, outputting an error message if not
        try:
            NumPoints = int(input(
"""|---------------------------------------------------------------------------------------------------|
|                       How many points would you like the calculation over?                        |
|                           This will effect the resolution of the output.                          |
|                               (press enter for default number, 100)                               |""").strip() or 100)    
            break
        except ValueError:
           print("|                                  \033[0;31;40m Please input an integer value.\x1b[0m                                  |")
    xArray=yArray=np.linspace(-5E-3,5E-3,num=NumPoints)   #calculates values for xArray,yArray,E1d and E2d based on the new Numpoints value
    E1d=np.zeros(NumPoints,dtype=complex)
    E2d=np.zeros((NumPoints,NumPoints),dtype=complex)
    while True:    #takes user input for value for z (screen distance) variable, repeats until a valid input is given, outputting an error message if not
        try:
            z=float(input(
"""|---------------------------------------------------------------------------------------------------|
|                                What distance should the screen be?                                |
|                              (press enter for default number, 2E-2)                               |""").strip() or 2E-2)
            break
        except ValueError:
            print("|                                      \033[0;31;40mPlease input a decimal.\x1b[0m                                      |")
    while True:    #takes user input for value for ApertureWidth variable, repeats until a valid input is given, outputting an error message if not
        try:
            ApertureWidth=float(input(
"""|---------------------------------------------------------------------------------------------------|
|                             What Aperture width should the screen be?                             |
|                              (press enter for default number, 2E-5)                               |
|---------------------------------------------------------------------------------------------------|""").strip() or 2E-5)
            xprime_1=yprime_1=-ApertureWidth/2   #Calculates values for xprime_1,xprime_2,yprime_1 and yprime_2 for new ApertureWidth value
            xprime_2=yprime_2=ApertureWidth/2
            break
        except ValueError: #
            print("|                                      \033[0;31;40mPlease input a decimal.\x1b[0m                                      |")

def Menu():
    """
    Menu function
    
    
    
    recieves an input which determines which functions are called next according to wether they are in part a,b or c of the task
    
    """
    Input = input("""|       Would you like a 1 dimension calculation (a), 2 dimensions for a square aperture (b),       |
|               a rectangular aperture (c), a circular apereture (d), or to quit (q)                |""")   #takes input for menu function
    if Input == "a":   #if the input is for part a, the variable defining function is called followed by a 1d diffraction calculation
        ChangeVars()
        OneDimensionDiffraction()
        Menu()
    elif Input =="b":   #if the input is for part b, the variable defining function is called followed by a 2d diffraction calculation, integrating wrt x, then y
        ChangeVars()
        TwoDimensionDiffraction()
        Menu()
    elif Input =="c":   #if the input is for part c, the variable defining function is called followed by a 2d diffraction calculation for a rectangle, integrating wrt x then y
        ChangeVars()
        TwoDimensionRectangle()
        Menu()
    elif Input =="d":   #if the input is for part d, the variable defining function is called followed by a 2d diffraction calculation for a circle, integrating wrt x then y
        ChangeVars()
        TwoDimensionCircle()
        Menu()      
    elif Input =="q":   #ends the if statement and therefore the program if the user chooses to quit
        print("x======================= Thank you for using this Fresnel diffraction program. =====================x")
        pass
    else:
        print('''|---------------------------------------------------------------------------------------------------|
|                                 \033[0;31;40mplease type "a", "b", "c" or "q"\x1b[0m                                  |
|---------------------------------------------------------------------------------------------------|''')   #prints error message if no valid input is given
        Menu()

def OneDimensionDiffraction():
    """
    Calculates the diffraction integral over one dimension

    RETURNS
    plot of diffraction in 1d
    
    """
    global NumPoints, z, ApertureWidth,xprime_1,yprime_1,xprime_2,yprime_2,xArray,yArray,E1d,E2d,k,FigureSize   #calls global variables for editing
    for i in range(NumPoints):
        x=xArray[i]
        E1d[i] = ((k*E_0)/(2*np.pi*z)) * scipy.integrate.quad(lambda xprime: np.exp((1j*k)/(2*z)*(x-xprime)**2),xprime_1,xprime_2,complex_func=True)[0]   #calculates the integral from equation 4
    fig, (ax1) = plt.subplots(1)   #creates a plot with 1 subplot
    fig.set_size_inches(11.7,11.7)
    ax1.plot(xArray,abs(E1d)**2,'tab:red')   #plots the intensity vs distance to the subplot
    fontsize = 25    #variable to make adjusting font size fast for putting plots in LaTeX
    plt.setp(ax1.get_xticklabels(), fontsize=fontsize)
    plt.setp(ax1.get_yticklabels(), fontsize=fontsize)
    ax1.set_title('Diffraction pattern', fontsize=fontsize)
    ax1.set_xlabel('Screen Coordinate', fontsize=fontsize)
    ax1.set_ylabel('Relative Intensity', fontsize=fontsize)
    plt.show()   #plots the graph
    print("|---------------------------------------------------------------------------------------------------|")

def OneDimensionDiffractionVarCombinedPlot():
    """
    Similarly calculates the diffraction pattern in 1d but with varying values of z and aperture width in 2 plots

    RETURNS
    2 plots
  
    """
    global NumPoints, z, ApertureWidth,xprime_1,yprime_1,xprime_2,yprime_2,xArray,yArray,E1d,E2d,k   #call global variables for editing
    ApertureWidths = [1E-5,2E-5, 3E-5, 4E-5,5E-5,6E-6]  #list of values for ApertureWidth
    zs = [1E-2,2E-2, 3E-2, 4E-2,5E-2,6E-2]  #list of values for z
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))   #sets up a plot with 2 axese 
    for ApertureWidth in ApertureWidths:   #iterates over the number of aperture widths
        E1d = np.zeros(NumPoints, dtype=complex)   #creates an np array of the correct size full of zeros
        xprime_1 = -ApertureWidth / 2   #calculates xprime_1 and 2, the integration limits
        xprime_2 = ApertureWidth / 2
        for i in range(NumPoints):
            x = xArray[i]
            E1d[i] = ((k*E_0)/(2*np.pi*z)) * scipy.integrate.quad(lambda xprime: np.exp((1j*k)/(2*zs[0]) * (x-xprime)**2), xprime_1, xprime_2, complex_func=True)[0]   #calculates equation 4 over the integral limits
        ax1.plot(xArray, abs(E1d) ** 2, label=f"Aperture Width: {ApertureWidth}")   #plots the axese for the graph of varying ApertureWidth in 1d
        ax1.set_xlim([-0.001, 0.001])
    ax1.set_xlabel('Screen Coordinate')
    ax1.set_ylabel('Relative Intensity')
    ax1.set_title('Diffraction Patterns with varied Aperture width')
    ax1.legend()

    for z in zs:
        E1d = np.zeros(NumPoints, dtype=complex)   #creates an np array of the correct size full of zeros
        xprime_1 = -ApertureWidth / 2   #calculates xprime_1 and 2, the integration limits
        xprime_2 = ApertureWidth / 2
        for i in range(NumPoints):
            x = xArray[i]
            E1d[i] = ((k*E_0)/(2*np.pi*z)) * scipy.integrate.quad(lambda xprime: np.exp((1j*k)/(2*z)*(x-xprime)**2), xprime_1, xprime_2, complex_func=True)[0]   #calculates equation 4 over the integral limits
        ax2.plot(xArray, abs(E1d) ** 2, label=f"Distance: {z}")   #plots the axese for the graph of varying z in 1d
    ax2.set_xlabel('Screen Coordinate')
    ax2.set_ylabel('Relative Intensity')
    ax2.set_title('Diffraction Patterns with Varied screen distance')
    ax2.legend()
    plt.show()    #plots the data on the axese and prints them to the user
    print("|---------------------------------------------------------------------------------------------------|")

def TwoDimensionDiffraction():
    """
    Creates a diffraction pattern in 2d for a square aperture.

    RETURNS
    
    heatmap of intensity and screen coordinate
    
    """
    global NumPoints, z, ApertureWidth,xprime_1,yprime_1,xprime_2,yprime_2,xArray,yArray,E1d,E2d,k   #calling global variables for editing
    for i,x in enumerate(xArray):   #loops for the number of values in the xArray and yArray
        for j,y in enumerate(yArray):
            E2d[i,j] = ((k*E_0)/(2*np.pi*z)) * scipy.integrate.dblquad(lambda xprime, yprime: np.exp(((1j*k)/(2*z))*((x-xprime)**2+(y-yprime)**2)),xprime_1,xprime_2,lambda x:yprime_1,lambda x:yprime_2)[0]   #calculates the integral with y as a function of x
    fig, ax = plt.subplots(1)   #setus up a plot with 1 subplot
    fig.set_size_inches(11.7, 11.7)
    im = ax.imshow(abs(E2d) ** 2, extent=(xArray.min(), xArray.max(), yArray.min(), yArray.max()), cmap='hot', interpolation='nearest')   #plots heatmap of intensity
    cbar = plt.colorbar(im, label='Relative Intensity')   #adds colour bar

    fontsize = 10   #variable to be able to adjust font size to input to LaTeX and still be visibile.
    ax.tick_params(axis='both', which='major', labelsize=fontsize)
    ax.set_title('Diffraction pattern', fontsize=fontsize)
    ax.set_xlabel('Screen Coordinate', fontsize=fontsize)
    ax.set_ylabel('Relative Intensity', fontsize=fontsize)
    cbar.ax.yaxis.label.set_fontsize(fontsize)

    plt.show()   #prints the plot to user
    print("|---------------------------------------------------------------------------------------------------|")

def TwoDimensionRectangle():
    """
    Creates diffraction pattern in 2d for a rectangular aperture

    RETURNS 
    
    heatmap of intensity

    """
    global NumPoints, z, WaveLength, xArray, yArray, E2d   #calls global varibales for editing
    width = 2E-3  #define the dimensions of the rectangular aperture
    height = 1E-3  
    for i, x in enumerate(xArray):   #loops for number of values in xArray and yArray
        for j, y in enumerate(yArray):
            def aperture_function(xp, yp):  #define the rectangular aperture function to have value 1 when in rectangle and 0 when not
                if -width/2<=xp<=width/2 and -height/2<=yp<=height/2:
                    return 1
                else:
                    return 0
            E2d[i, j] = (1j/WaveLength*z)**(-1)*scipy.integrate.dblquad(lambda xp, yp: aperture_function(xp, yp)*np.exp(((1j*2*np.pi*z)/WaveLength)*np.sqrt((x-xp)**2+(y-yp)**2)), -width/2, width/2, lambda _: -height/2, lambda _: height/2)[0]   #calculates E values by integrating with y as a function of x
    fig, ax = plt.subplots(1)   #makes plot with 1 subplot
    fig.set_size_inches(11.7, 11.7)   #set size
    plt.imshow(abs(E2d)**2, extent=(xArray.min(), xArray.max(), yArray.min(), yArray.max()), cmap='hot', interpolation='nearest')   #add colourmap to plot
    plt.colorbar(label='Relative Intensity')   #add labels for axese
    plt.xlabel('Screen x-coordinate')
    plt.ylabel('Screen y-coordinate')
    plt.title('2D Diffraction Pattern for Rectangular Aperture')
    plt.show()   #print map to user
    print("|---------------------------------------------------------------------------------------------------|")

def TwoDimensionCircle():
    """
    Creates diffraction pattern in 2d for a circular aperture

    RETURNS
    heatmap of intensity

    """
    global NumPoints, z, WaveLength, xArray, yArray, E2d   #calls global variables for editing
    radius = 1E-3  #define variable for radius
    for i, x in enumerate(xArray):   #repeats for number of values in xArray and y Array
        for j, y in enumerate(yArray):
            def aperture_function(xp, yp):   #define circular aperture function to return 1 when in aperture and 0 otherwise
                if xp**2 + yp**2 <= radius**2:
                    return 1
                else:
                    return 0
            E2d[i, j] = (1j/WaveLength*z)**(-1)*scipy.integrate.dblquad(lambda xp, yp:aperture_function(xp, yp)*np.exp(((1j*2*np.pi*z)/WaveLength)*np.sqrt((x-xp)**2+(y-yp)**2)), -radius, radius, lambda _: -np.sqrt(radius**2-_**2), lambda _: np.sqrt(radius**2-_**2))[0]   #calculates integrand for values in E2d
    fig, ax = plt.subplots(1)   #create plot with 1 subplot
    fig.set_size_inches(11.7, 11.7)   #set size
    plt.imshow(abs(E2d)**2, extent=(xArray.min(), xArray.max(), yArray.min(), yArray.max()), cmap='hot', interpolation='nearest')   #add colour map to suplot 1
    plt.colorbar(label='Relative Intensity')  #add labels
    plt.xlabel('Screen x-coordinate')
    plt.ylabel('Screen y-coordinate')
    plt.title('2D Diffraction Pattern for Circular Aperture')
    plt.show()   #print the plot to user
    print("|---------------------------------------------------------------------------------------------------|")   #menu nice stuff


#greets user and begins program with menu function call
print("x=========================== Welcome to this Fresnel diffraction program ===========================x")
Menu()