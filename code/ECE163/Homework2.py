from  matplotlib  import  pyplot  as plt
from scipy.optimize import curve_fit
# from math import sin, cos
import  numpy  as np

def  sigma(a, a0, M):
    num = (1 + np.exp(-M*(a-a0)) + np.exp(M*(a+a0)))
    den = (1 + np.exp(-M*(a-a0)))*(1 + np.exp(M*(a+a0)))
    return  num/den

## Plotting  several  values  of M
#plot  100  points  from  -3.2 to 3.2:
blend_fig = plt.figure("Sigma  vs  Alpha  for  several  values  of M")
a = np.linspace (-3.2, 3.2, 100)
for M in np.logspace (-1,2,5):
    a0 = 1.5
    sigma_vals = [sigma(ai,a0, M) for ai in a]
    plt.plot(a, sigma_vals , label=f"M={M:0.2f}")
plt.legend(loc = "lower left")
plt.show()


## Plotting several different values of a0
blend_fig2 = plt.figure("Sigma  vs  Alpha  for  several  values  of a0")
for a0 in np.logspace (-1,2,5):
    M = 1.5
    sigma_vals = [sigma(ai,a0, M) for ai in a]
    plt.plot(a, sigma_vals , label=f"a0={a0:0.2f}")
plt.legend(loc = "lower left")
plt.show()

########## Part C
blend_fig3 = plt.figure("Plot of Cl and Cd points")
alpha = [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0,21.0,22.0,23.0,24.0,25.0,26.0,27.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0,80.0,85.0,90.0,95.0,100.0,105.0,110.0,115.0,120.0,125.0,130.0,135.0,140.0,145.0,150.0,155.0,160.0,165.0,170.0,175.0,180.0]
C_L = [0.0,0.11,0.22,0.33,0.44,0.55, 0.66,    0.77,  0.8504,  0.9387,1.0141,  1.0686,  1.0971,  1.0957,  1.0656,  1.0145,  0.9356,  0.8996,  0.8566,  0.8226,0.8089,  0.8063,  0.8189,  0.8408,  0.8668,  0.9023,  0.9406,  0.9912,   0.855,    0.98,1.035,    1.05,    1.02,   0.955,   0.875,    0.76,    0.63,     0.5,   0.365,    0.23,0.09,   -0.05,  -0.185,   -0.32,   -0.45,  -0.575,   -0.67,   -0.76,   -0.85,   -0.93,-0.98,    -0.9,   -0.77,   -0.67,  -0.635,   -0.68,   -0.85,   -0.66,     0.0]
C_D = [0.0074,  0.0075,  0.0076,  0.0079,  0.0083,  0.0091,  0.0101,  0.0111,  0.0126,  0.0138,0.0152,  0.0168,  0.0186,  0.0205,  0.0225,  0.0249,  0.0275,  0.0303,   0.145,    0.26,0.282,   0.305,   0.329,   0.354,   0.379,   0.405,   0.432,    0.46,    0.57,   0.745,0.92,   1.075,   1.215,   1.345,    1.47,   1.575,   1.665,   1.735,    1.78,     1.8,1.8,    1.78,    1.75,     1.7,   1.635,   1.555,   1.465,    1.35,   1.225,   1.085,0.925,   0.755,   0.575,    0.42,0.32,0.23,0.14,0.055,0.025]

plt.plot(alpha, C_L, 'b--', label='C lift')
plt.plot(alpha, C_D, 'r--', label='C drag')

plt.xlabel('alpha')
plt.ylabel('C_L and C_D')
plt.legend()
plt.show()