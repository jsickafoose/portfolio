##  Git commit ID For this:
#   2efe0112eba0c8a970436bb304300f49076bfaa0
import numpy as np
import matplotlib.pyplot as plt
import math as m
import pdb

Mg = 400        # Newtons
OA = 0.5        # Meters
AB=BD=BC=0.25   # Meters
Psi = (m.pi)/6  # Radians
Theta_Dot = 0.5 # Radians/Second



# Implementation of equation for weight loading on point C
def func_C(t):
    Theta = t*Theta_Dot # First calculates the Theta angle at the current time step

    F_A = 426.8-(100*m.tan(Theta)) # Equation given in the homework
    return F_A

# Implementation of equation for weight loading on point B
def func_B(t):
    Theta = t*Theta_Dot

    ## Knowing that the answer is always 600N makes this feel sinful from an efficiency perspective
    #  but I'm already dividing things by floats instead of just multiplying by 2
    num = (OA+AB)*Mg
    den = OA
    return num/den

# Implementation of equation for weight loading on point D
def func_D(t):
    Theta = t*Theta_Dot

    r_OB = (OA+AB)*m.cos(Theta)
    r_DB = BD*m.sin(m.pi/2 - Theta - Psi)
    r_D = r_OB - r_DB

    r_A = OA*m.cos(Theta)

    F_A = (r_D*Mg)/r_A
    return F_A


## Creates plot
blend_fig = plt.figure("Force on A, in Z direction vs Time for different locations of the weight")

# Plotting C values
t = np.linspace (0, 1.5, 100)
C_Values = [func_C(i) for i in t]
plt.plot(t, C_Values, label="Load on C")

# Plotting B values
B_Values = [func_B(i) for i in t]
plt.plot(t, B_Values, label="Load on B")

# Plotting D values
D_Values = [func_D(i) for i in t]
plt.plot(t, D_Values, label="Load on D")


## Runs the plot
plt.xlabel('Time (Seconds)')
plt.ylabel('Force on A in z Direction (Newtons)')
plt.legend(loc = "lower left")
plt.tight_layout()
plt.show()