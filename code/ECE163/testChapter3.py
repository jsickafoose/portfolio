#############################################
#   Created by Jacob Sickafoose - jsickafo  #
#############################################

"""This file is a test harness for the module ece163.Utilities.Rotations,
and for the method ece163.Modeling.VehicleGeometry.getNewPoints(). 

 It is meant to be run from the root directory of the repo with:

python testChapter3.py

at which point it will execute various tests on the Rotations module"""

#%% Initialization of test harness and helpers:

import math
import ece163.Utilities.MatrixMath as mm
import ece163.Constants.VehiclePhysicalConstants as VPC
import ece163.Containers.States as states
import ece163.Containers.Inputs as inputs
import ece163.Modeling.VehicleDynamicsModel as VDM

testState = states.vehicleState(pn=6.9, pe=4.2, pd=1.0, u=9.0, v=2.0, w=8.0, yaw=1.0, pitch=4.0, roll=5.0, p=4.0, q=1.0, r=2.0)
test = VDM.VehicleDynamicsModel()
testFm = inputs.forcesMoments(Fx=2.0, Fy=3.0, Fz=1.0, Mx=0.0, My=2.0, Mz=1.0)

testDot = test.derivative(testState, testFm)
print("Test 1: Derivative test")
pn = -10.254837246296779
pe = -0.7226129228287452
pd = 6.581500103754857
u = -3.8181818181818183
v = 14.272727272727273
w = 1.0909090909090908
yaw = 3.5465972972876187
pitch = 2.2015107347895033
roll = 0.5991030758003779
p = -0.979556923367035
q = 7.076651982378854
r = -0.3417502294334229
if pn == testDot.pn and testDot.pe == pe and testDot.pd == pd and testDot.u == u and testDot.v == v and testDot.w == w and testDot.yaw == yaw and testDot.pitch == pitch and testDot.roll == roll and testDot.p == p and testDot.q == q and testDot.r == r:
    print("Test1 Passed")
else:
    print("Test1 Failed")



testOutState = test.ForwardEuler(test.dT, testState, testDot)
pn = 6.797451627537033
pe = 4.192773870771712
pd = 1.0658150010375487
u = 8.961818181818181
v = 2.1427272727272726
w = 8.010909090909092
p = 3.9902044307663296
q = 1.0707665198237886
r = 1.9965824977056659
print("\nTest 2: Forward Euler test")
if pn == testOutState.pn and testOutState.pe == pe and testOutState.pd == pd and testOutState.u == u and testOutState.v == v and testOutState.w == w and testOutState.p == p and testOutState.q == q and testOutState.r == r:
    print("Test2 Passed")
else:
    print("Test2 Failed")



testOutState = test.Rexp(test.dT, testState, testDot)
rexp_expected = [[0.9997467850516959, 0.02018269739809591, -0.00995110569409421],
                 [-0.01976912367527641, 0.9990024743204048, 0.04004045517749168],
                 [0.010749303601153304, -0.03983359169653154, 0.9991485062014777]]
print("\nTest 3: Rexp test")
if rexp_expected == testOutState:
    print("Test3 Passed")
else:
    print("Test3 Failed")

testOutState = test.IntegrateState(test.dT, testState, testDot)
r_expected = [[-0.3407956012576111, -0.5378227999579874, 0.7711063441632509],
              [0.12328819855310474, 0.7875562010699146, 0.6037841089775835],
              [-0.9320184430905827, 0.3008352805135641, -0.20208848492017453]]
yaw = -2.135597250080029
pitch = -0.8805769330541259
roll = 1.893779271293161
Va = 12.206555615733704
alpha = 0.7266423406817256
beta = 0.16458847786253597
chi = -3.0712433699951247

print("\nTest 4: IntegrateState test")
if r_expected == testOutState.R and yaw == testOutState.yaw and pitch == testOutState.pitch and roll == testOutState.roll and Va == testOutState.Va and alpha == testOutState.alpha and beta == testOutState.beta and chi == testOutState.chi:
    print("Test4 Passed")
else:
    print("Test4 Failed")