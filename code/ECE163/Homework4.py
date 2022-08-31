from  ece163.Utilities  import  MatrixMath  as mm
from  matplotlib  import  pyplot  as plt
import  math

a_1 = 0.79
a_2 = 4.19
b_2 = 4.19

A = [[-a_1 , -a_2],[1, 0]]
B = [[1],  [0]]
C = [[0,b_2]]

dT = 0.01
T_tot = 16
n_steps = int(T_tot/dT)

t_data   = [i*dT for i in range(n_steps)]
yaw_data = [0    for i in range(n_steps)]
yaw_data2 = [0    for i in range(n_steps)]
yaw_data3 = [0    for i in range(n_steps)]
rudder_data = [0    for i in range(n_steps)]
rudder_data2 = [0    for i in range(n_steps)]

wind_data = [(0 if t < 1 else  10* math.pi/180)  for t in t_data ]

x  = [[0] ,[0]]
x2 = [[0] ,[0]]
x3 = [[0] ,[0]]
for i in range(n_steps):
    #record  our  data
    yaw_data[i] = mm.multiply(C, x)[0][0]
    yaw_data2[i] = mm.multiply(C, x2)[0][0]
    yaw_data3[i] = mm.multiply(C, x3)[0][0]
    rudder_data[i]  = (-yaw_data2[i])*(-0.7)
    rudder_data2[i] = (-yaw_data3[i])*(-0.7) + (-yaw_data3[i])*(-0.9)
    #find u(t):
    u  = wind_data[i]
    u2 = wind_data[i] + (-1)*rudder_data[i]
    u3 = wind_data[i] + (-1)*rudder_data[i]
    #calculate  derivative:
    x_dot = mm.add(mm.multiply(A,x), mm.scalarMultiply(u,B))
    x_dot2 = mm.add(mm.multiply(A,x2), mm.scalarMultiply(u2,B))
    x_dot3 = mm.add(mm.multiply(A,x3), mm.scalarMultiply(u3,B))
    #forward  euler  update:
    x = mm.add(x, mm.scalarMultiply(dT, x_dot))
    x2 = mm.add(x2, mm.scalarMultiply(dT, x_dot2))
    x3 = mm.add(x2, mm.scalarMultiply(dT, x_dot3))


plt.close("all")
fig , ax = plt.subplots()
ax.plot(t_data , wind_data, label = "wind  angle")
ax.plot(t_data , yaw_data, label = "yaw  response")
# ax.plot(t_data , rudder_data, label = "rudder reponse")
ax.set_xlabel("time (s)")
ax.set_ylabel("angle (rad)")
ax.legend()
plt.show()

fig2 , ax2 = plt.subplots()
ax2.plot(t_data , wind_data, label = "wind angle")
ax2.plot(t_data , yaw_data2, label = "yaw  response")
ax2.plot(t_data , rudder_data, label = "rudder reponse")
ax2.set_xlabel("time (s)")
ax2.set_ylabel("angle (rad)")
ax2.legend()
plt.show()

fig3 , ax3 = plt.subplots()
ax3.plot(t_data , wind_data, label = "wind angle")
ax3.plot(t_data , yaw_data3, label = "yaw  response")
ax3.plot(t_data , rudder_data2, label = "rudder reponse")
ax3.set_xlabel("time (s)")
ax3.set_ylabel("angle (rad)")
ax3.legend()
plt.show()