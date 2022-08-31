from  matplotlib  import  pyplot  as plt
import random
import math
import  numpy  as np

##### Constants #####
Lu = 200
Lv = 200
Lw = 50
sigmaU = 1.06
sigmaV = 1.06
sigmaW = 0.7
Va = 25
dT = 0.01


##### Phi, Gamma, and H #####
#### V component
Phi_u   = math.exp(-(Va/Lu)*dT)
Gamma_u = (Lu/Va) * (1-(math.exp(-(Va/Lu)*dT)))
H_u     = sigmaU * (math.sqrt((2*Va)/(math.pi*Lu)))

## Solves for the matrix half of the equation for the Phi, Gamma, and H of the v component
Phi_v_m   = [[(1-(Va/Lv)*dT), (-((Va/Lv)**2)*dT)],
           [(dT), (1+(Va/Lv)*dT)]]
Gamma_v_m = [(dT), (((Lv/Va)**2)*((math.exp((Va/Lv)*dT))-1)-((Lv/Va)*dT))]
H_v_m     = [1, (Va/(math.sqrt(3)*Lv))]

# Calculating first part of Phi and Gamma equation separately since it's the same
FirstPart_v = (math.exp((-Va/Lv)*dT))

## Solves for Phi, Gamma, and H of the v component
Phi_v   = [[FirstPart_v*Phi_v_m[0][0], FirstPart_v*Phi_v_m[0][1]],
           [FirstPart_v*Phi_v_m[1][0], FirstPart_v*Phi_v_m[1][1]]]
Gamma_v = [FirstPart_v*Gamma_v_m[0], FirstPart_v*Gamma_v_m[1]]
H_v     = [(sigmaV*(math.sqrt((3*Va)/(math.pi*Lv))))*H_v_m[0], (sigmaV*(math.sqrt((3*Va)/(math.pi*Lv))))*H_v_m[1]]


#### W component
## Solves for the matrix half of the equation for the Phi, Gamma, and H of the w component
Phi_w_m   = [[(1-(Va/Lw)*dT), (-((Va/Lw)**2)*dT)],
           [(dT), (1+(Va/Lw)*dT)]]
Gamma_w_m = [(dT), (((Lw/Va)**2)*((math.exp((Va/Lw)*dT))-1)-((Lw/Va)*dT))]
H_w_m     = [1, (Va/(math.sqrt(3)*Lw))]

# # Calculating first part of Phi and Gamma equation separately since it's the same
FirstPart_w = (math.exp((-Va/Lw)*dT))

## Solves for Phi, Gamma, and H of the w component
Phi_w   = [[FirstPart_w*Phi_w_m[0][0], FirstPart_w*Phi_w_m[0][1]],
           [FirstPart_w*Phi_w_m[1][0], FirstPart_w*Phi_w_m[1][1]]]
Gamma_w = [FirstPart_w*Gamma_w_m[0], FirstPart_w*Gamma_w_m[1]]
H_w     = [(sigmaW*(math.sqrt((3*Va)/(math.pi*Lw))))*H_w_m[0], (sigmaV*(math.sqrt((3*Va)/(math.pi*Lw))))*H_w_m[1]]



##### Coloring filters #####
# H_u = sigmaU*(math.sqrt((2*Va)/(math.pi*Lu))*(1/(s+(Va/Lu))))
# H_v = sigmaV*(math.sqrt((3*Va)/(math.pi*Lv))*((s+((Va)/(math.sqrt(3)*Lv)))/((s+(Va/Lu)))**2))
# H_w = sigmaW*(math.sqrt((3*Va)/(math.pi*Lw))*((s+((Va)/(math.sqrt(3)*Lw)))/((s+(Va/Lw)))**2))



##### Start of Wv solving functions #####
def Wv_partA(u):
    Wv = u * 0.059
    return Wv

def Wv_partB(x_prev, u):
    A = [[(-2*(Va/Lv)), (-(Va**2)/(Lv**2))],
         [1, 0]]
    B =  [1, 0]
    C = [sigmaV*(math.sqrt((3*Va)/(math.pi*Lv))),
        (sigmaV*(math.sqrt((3*Va)/(math.pi*Lv))))*(Va/((math.sqrt(3))*Lv))]

    x = [(x_prev[0])*A[0][0] + x_prev[1]*A[0][1] + B[0]*u,
         (x_prev[0])*A[1][0] + x_prev[1]*A[1][1] + B[1]*u]
    x = [x_prev[0]+dT*x[0],
         x_prev[1]+dT*x[1]]

    Wv = C[0]*x[0] + C[1]*x[1]
    return Wv, x

def Wv_partC(x_prev, u):
    x = [Phi_v[0][0]*x_prev[0] + Phi_v[0][1]*x_prev[1] + Gamma_v[0]*u,
         Phi_v[1][0]*x_prev[0] + Phi_v[1][1]*x_prev[1] + Gamma_v[1]*u]
    Wv = x[0]*H_v[0] + x[1]*H_v[1]
    return Wv, x


##### Plotting #####
blend_fig = plt.figure("u vs Wv")
u_series = [random.gauss(0,1) for i in range(1000)] # Creates random gauss variables in a len = 1000 array

## Runs each gauss array value through the Wv functions
x_b = [0, 0]
x_c = [0, 0]

# Finds Wv for part A
Wv_partA_vals = [Wv_partA(ui) for ui in u_series]

# Finds Wv for part B and C
Wv_partB_vals = [1]*len(u_series)
Wv_partC_vals = [1]*len(u_series)
for i in range(len(u_series)):
    Wv_b, x_b = Wv_partB(x_b, u_series[i])
    Wv_partB_vals[i] = Wv_b

    Wv_c, x_c = Wv_partC(x_c, u_series[i])
    Wv_partC_vals[i] = Wv_c


plt.plot(u_series, Wv_partA_vals, label="Part A")
plt.scatter(u_series, Wv_partB_vals, label="Part B")
plt.scatter(u_series, Wv_partC_vals, label="Part C")
plt.legend(loc = "lower left")
plt.show()