from  ece163.Utilities  import  MatrixMath  as mm
from  matplotlib  import  pyplot  as plt
import  math

a_1 = 3.18
a_2 = 35.98
b_2 = -11.15

A = [[-a_1 , -a_2],[1, 0]]
B = [[1],  [0]]
C = [[0,b_2]]

dT = 0.01
T_tot = 6
n_steps = int(T_tot/dT)

t_data   = [i*dT for i in range(n_steps)]
pitch_data = [0    for i in range(n_steps)]
pitch_data2 = [0    for i in range(n_steps)]

pitchCommanded_data = [(0 if t < 1 else  5.73* math.pi/180)  for t in t_data ]

x  = [[0] ,[0]]
x2  = [[0] ,[0]]
for i in range(n_steps):
    #record  our  data
    pitch_data[i] = mm.multiply(C, x)[0][0]
    pitch_data2[i] = mm.multiply(C, x2)[0][0]
    #find u(t):
    u  = pitchCommanded_data[i]
    u2 = pitchCommanded_data[i] + (-1)*rudder_data[i]
    #calculate  derivative:
    x_dot = mm.add(mm.multiply(A,x), mm.scalarMultiply(u,B))
    x_dot2 = mm.add(mm.multiply(A,x2), mm.scalarMultiply(u2,B))
    #forward  euler  update:
    x = mm.add(x, mm.scalarMultiply(dT, x_dot))
    x2 = mm.add(x2, mm.scalarMultiply(dT, x_dot2))


plt.close("all")
fig , ax = plt.subplots()
ax.plot(t_data , pitchCommanded_data, label = "wind  angle")
ax.plot(t_data , pitch_data, label = "yaw  response")
ax.set_xlabel("time (s)")
ax.set_ylabel("angle (rad)")
ax.legend()
plt.show()

fig2 , ax2 = plt.subplots()
ax2.plot(t_data , pitchCommanded_data, label = "wind angle")
ax2.plot(t_data , pitch_data2, label = "yaw  response")
ax2.set_xlabel("time (s)")
ax2.set_ylabel("angle (rad)")
ax2.legend()
plt.show()