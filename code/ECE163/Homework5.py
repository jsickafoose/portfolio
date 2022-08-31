from  ece163.Utilities  import  MatrixMath  as mm
from  matplotlib  import  pyplot  as plt
import ece163.Constants.VehiclePhysicalConstants as VPC
import  math
import random

accumulator = 0
accumulator2 = 0
prevError = 0
error = 0
# highLimit = 0
# lowLimit = 0
Xw = 0
yTrue = 0
kp = -10
ki = -1

a_1 = 0.79
a_2 = 4.19
b_2 = 4.19
A = [[-a_1 , -a_2],[1, 0]]
B = [[1],  [0]]
C = [[0,b_2]]

dT    = 0.01
tau   = 400
T_tot = 16
n_steps = int(T_tot/dT)

N_data    = [random.gauss(0, 0.0013) for i in range(n_steps)]
t_data    = [i*dT for i in range(n_steps)]
yaw_data  = [0    for i in range(n_steps)]
yGyro     = [0    for i in range(n_steps)]
wind_data = [(0 if t < 1 else  10* math.pi/180)  for t in t_data ]

yaw_dataest1 = [0    for i in range(n_steps)]
yaw_dataest2 = [0    for i in range(n_steps)]
yaw_dataest3 = [0    for i in range(n_steps)]

v = [0    for i in range(n_steps)]
x = [[0] ,[0]]

def Update(command=0.0, current=0.0, i=0, accumulator=0.0, prevError=0.0, error=0.0, Xw=0.0, yaw_dataest=[0]): # Implements the block diagram
    error = -yaw_dataest[i]

    accumulator += dT*((error+prevError)/2)
    Delta_r = kp*error + accumulator*ki

    u = Delta_r*(VPC.CndeltaR/VPC.Cnbeta) + Xw
    ## I'm not sure if we need the high/low limits because this transfer function doesn't control any UAV controls
    # if u > highLimit:
    #     u = highLimit
    #     accumulator = prevAccumulator
    # elif u < lowLimit:
    #     u = lowLimit
    #     accumulator = prevAccumulator
        
    prevError = error
    return u

for i in range(n_steps):
    # Set V[i] as sensor input
    yaw_data[i] = mm.multiply(C, x)[0][0]
    if i == 0:
        v[i] = 0
        yTrue = 0
    else:
        v[i] = math.exp(-dT/tau) * v[i-1] + N_data[i-1]
        yTrue = (yaw_data[i]-yaw_data[i-1])/dT
    #record our data
    yaw_dataest1[i] = yaw_data[i] + v[i]
    yGyro[i] = yTrue + v[i]
    if i != 0:
        accumulator2 += dT*((yGyro[i] + yGyro[i-1])/2)

    # I've heard differing things on which one we should use, my est2 or 3
    yaw_dataest2[i] = yGyro[i]*accumulator2
    yaw_dataest3[i] = yGyro[i]*dT

    #find u(t):
    u1 = wind_data[i]
    u = Update(0, yaw_data[i], i, accumulator, prevError, error, Xw, yaw_dataest1)
    #calculate derivative:
    x_dot = mm.add(mm.multiply(A,x), mm.scalarMultiply(u,B))
    #forward  euler  update:
    x = mm.add(x, mm.scalarMultiply(dT, x_dot))


# Graph for part a
fig, axs = plt.subplots(2)
# axs[1].set_title("Gauss-Markov, 2a")
axs[1].plot(t_data , v)
axs[1].set(xlabel="time (s)", ylabel="variable v")

# Subgraph for part b
axs[0].set_title('Gauss-Markov, 2b: kp = -10, ki = -1')
axs[0].plot(t_data , yaw_data, label = "yaw response")
axs[0].plot(t_data  , yaw_dataest1, label = "estimated yaw response")
axs[0].set(ylabel="response angle (rad)")
axs[0].legend()
plt.show()

# Graph for part c
fig , ax = plt.subplots()
ax.set_title('Gauss-Markov, 2c: kp = -10, ki = -1')
ax.plot(t_data , yaw_data, label = "yaw response")
ax.plot(t_data , yaw_dataest2, label = "estimated yaw response")
ax.set_xlabel("time (s)")
ax.set_ylabel("response angle (rad)")
ax.legend()
plt.show()

# Graph for another way of doing part c that im not sure is correct
fig , ax2 = plt.subplots()
ax2.set_title("2c: alternate way. I wasn't sure what the graph was supposed to look like")
ax2.plot(t_data , yaw_data, label = "yaw response")
ax2.plot(t_data , yaw_dataest3, label = "estimated yaw response")
ax2.set_xlabel("time (s)")
ax2.set_ylabel("response angle (rad)")
ax2.legend()
plt.show()