import numpy as np
from math import atan
from prettytable import PrettyTable

def MyArcTan(x,N):
    '''
    Purpose
    -------
    Calculates ArcTan of X using eq(1) with N terms in the sequence.
    
    Parameters
    ----------
    x : float
        The Value for which ArcTan will be found.
    N : Int
        Number of iterations of the summation

    Returns
    -------
    sum : Float
        ArcTan of x

    '''
    sum = 0.0
    for n in range (N):
        sum+=(((-1)**n)/(2*n+1))*(x**(2*n+1))
    return sum



def MyArcTanImproved(x,N):
    '''
    Purpose
    -------
    An improved version of MyArcTan which works for all x values

    Parameters
    ----------
    x : Float
        The value for which ArcTan will be found.
    N : Int
        Numberof iterations of the summation.

    Returns
    -------
    Float
    ArcTan of x.

    '''
    if x<=1 and x>=-1:
        return MyArcTan(x,N)
    elif x>1:
        return (np.pi/2)-MyArcTan(1/x, N)
    elif x<-1:
        return -1*(np.pi/2)-MyArcTan(1/x, N)
    else:
        return ("ERROR")

            
#Menu for choosing which task to check

MyInput = '0'
while MyInput != 'q':
    MyInput = input('Enter a choice, "a", "b", "c", "d" or "q" to quit: ')
    print('You entered the choice: ',MyInput)


#menu option (a)
    if MyInput == 'a':
        print('You have chosen part (a)')
        x = float(input('Enter a value for x (floating point number): ')) #assigning values of x and N 
        N = int(input('Enter a value for N (positive integer): '))
        print('ArcTan('+ str(x) + ") is: ",MyArcTanImproved(x,N)) #calls MyArcTanImproved which is a modified version of MyArcTan to calculate ArcTan(x)
            
#Menu option (b)            
    elif MyInput == 'b':
        print('You have chosen part (b)')
        NoIncrements = int(input('Enter a value for x (number of increments in output)')) #assigning values for the number of increments in the table and value of N 
        N = input('Enter a value for N (positive integer): ')
        if N.isnumeric() == True: #Checking N is an integer and formatting as int data type
            print ("N is an integer, printing table:")
            N = int(N)           
        elif N.isnumeric() == False:
            print ("ERR: N is not an integer")

        table = PrettyTable(["x","MyArcTan(x)","ArcTan(x)","Difference"]) #formatting for table output, note you will need prettytable installed using pip
        x=-2.0
        while x < 2.0: #creates table with x, MyArcTan, atan and the difference between atan and MyArcTan using a while loop between -2 and 2
            table.add_row([x,MyArcTanImproved(x, N),atan(x),abs(atan(x)-MyArcTanImproved(x, N))])
            x+=4/NoIncrements
        print(table)

#menu option (c)        
    elif MyInput == 'c':
        print('You have chosen part (c), please wait...')
        N=9999999 #note this is one value of the np value, i tried many high numbers and i was not able to acheive the same as np
        PiOverFour=round(MyArcTan(1,N),7) #assigning value for pi/4 using arctan(1) = pi/4
        print("Our calculated pi/4 is:",PiOverFour,"\nThis gives us", 4*PiOverFour, "as our value of pi to 7 significant figures.\nNumpy's calculation of pi is ", round(np.pi,7),"to 7 significant figures\nThe required value of N was 9999999.")

#menu option (d)
    elif MyInput == 'd':   
        N=18 #minimum N for correct output
        PiOverFourImproved = MyArcTan(0.5, N) + MyArcTan(0.2, N) + MyArcTan(0.125, N) #calculates pi/4 using the more efficient method in eq(3)
        print ("The improved method gives:\n"+ str(round(PiOverFourImproved,12))+"\nthe initial method gives\n"+str(round(MyArcTan(1,N),12))+"\nWith N = 18") #ouputs the different methods with the same N value, rounded to 12 sigfig
        
    elif MyInput != 'q':
        print('This is not a valid choice')
    
#end of menu
print('You have chosen to finish - goodbye.')
