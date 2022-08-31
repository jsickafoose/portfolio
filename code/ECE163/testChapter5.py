#############################################
#   Created by Jacob Sickafoose - jsickafo  #
#############################################

"""
This file is a test harness for the module ece163.Modeling.Rotations
It is meant to be run from the root directory of the repo with:

python testChapter4.py

at which point it will execute various tests on the Rotations module"""

#%% Initialization of test harness and helpers:

import ece163.Containers.States as states
import ece163.Containers.Inputs as inputs
import ece163.Constants.VehiclePhysicalConstants as VPC
import ece163.Modeling.VehicleAerodynamicsModel as VAM
import ece163.Controls.VehiclePerturbationModels as VPM

# Establishes the AerodynamicsModel object we will test
test = VAM.VehicleAerodynamicsModel()
testState = states.vehicleState(pn=6.9, pe=4.2, pd=1.0, u=9.0, v=2.0, w=8.0, yaw=1.0, pitch=4.0, roll=5.0, p=4.0, q=1.0, r=2.0)
test.setVehicleState(testState)
testWindState = states.windState(1, 43, 3, 2, 56, 7)
dryden = inputs.drydenParameters(VPC.DrydenHighAltitudeModerate)
# Sets the how many tests there are, and initializes a counting variable for them
testTotal = 12
testsPassed = 0


########################################
# windModel CreateTransferFcns() test 1
########################################
testsPassed1 = 0
print("\ntesting CreateTransferFcns()")  # Announce which test we're on

# plug in random test variables
test.Wind.CreateDrydenTransferFns(VPC.dT, VPC.InitialSpeed, VPC.DrydenHighAltitudeModerate)

# Check if each individual expected output variable is right. If it isn't, prints exp vs. obs
if test.Wind.Phi_u[0][0]!=0.9995310668315729:
  print(f"\n    CreateTransferFcns() test failed:\nexp: 0.9995310668315729 != obs: {test.Wind.Phi_u[0][0]}")
if test.Wind.Gamma_v[0][0]!=0.00999531066831573:
  print(f"    CreateTransferFcns() test failed:\nexp: 0.00999531066831573 != obs: {test.Gamma_v[0][0]}")
if test.Wind.H_w[0][0]!=0.6349117224157215:
  print(f"    CreateTransferFcns() test failed:\nexp: 0.6349117224157215 != obs: {test.H_w[0][0]}")
else:     # If all tests check out, adds to total
  testsPassed+=1
  testsPassed1+=1


# CreateDrydenTransferFns() test 2, does the same test again with different random variables
test.Wind.CreateDrydenTransferFns(VPC.dT, VPC.InitialSpeed, VPC.DrydenHighAltitudeLight)
if test.Wind.Phi_u[0][0]!=0.9995310668315729:
  print(f"\n    CreateDrydenTransferFns() test failed:\nexp: 0.9995310668315729 != obs: {test.Wind.Phi_u[0][0]}")
if test.Wind.Gamma_w[0][0]!=0.00999531066831573:
  print(f"    CreateDrydenTransferFns() test failed:\nexp: 0.00999531066831573 != obs: {test.Wind.Gamma_v[0][0]}")
if test.Wind.H_v[0][0]!=0.31745586120786073:
  print(f"    CreateDrydenTransferFns() test failed:\nexp: 0.31745586120786073 != obs: {test.Wind.H_w[0][0]}")
else:
  testsPassed+=1
  testsPassed1+=1

print(f"  passed {testsPassed1}/2 tests")  # Prints out how many gravityForces() tests passed



########################################
# windModel Update() test 1
########################################
testsPassed2 = 0
print("testing windModel Update()")
test.Wind.Update(1, 2, 3)

if test.Wind.Xu[0][0]!=0.009997655150865991:
  print(f"\n    Update() test failed:\nexp: 0.009997655150865991 != obs: {test.Wind.Xu[0][0]}")
if test.Wind.Xv[0][0]!=0.01999062133663146:
  print(f"    Update() test failed:\nexp: 0.01999062133663146 != obs: {test.Wind.Xv[0][0]}")
if test.Wind.Xw[0][0]!=0.02998593200494719:
  print(f"    Update() test failed:\nexp: 0.02998593200494719 != obs: {test.Wind.Xw[0][0]}")
else:
  testsPassed+=1
  testsPassed2+=1


# Update() test 2
alpha =  -0.89
test.Wind.Update(3, 2, 1)
if test.Wind.Xu[0][0]!=0.039985932371357225:
  print(f"\n    Update() test failed:\nexp: 0.039985932371357225 != obs: {test.Wind.Xu[0][0]}")
if test.Wind.Xv[0][0]!=0.03996249414245849:
  print(f"    Update() test failed:\nexp: 0.03996249414245849 != obs: {test.Wind.Xv[0][0]}")
if test.Wind.Xw[0][0]!=0.039953119877056284:
  print(f"    Update() test failed:\nexp: 0.039953119877056284 != obs: {test.Wind.Xw[0][0]}")
else:
  testsPassed+=1
  testsPassed2+=1

print(f"  passed {testsPassed2}/2 tests")



########################################
#  VAM CalculateAirspeed() test 1
########################################
testsPassed4 = 0
print("testing VAM CalculateAirspeed()")
VaTest, alphaTest, betaTest = test.CalculateAirspeed(testState, testWindState)

if VaTest!=64.6175582805875:
  print(f"\n    CalculateAirspeed() test failed:\nexp: 64.6175582805875 != obs: {VaTest}")
if alphaTest!=-1.444822947225264:
  print(f"    CalculateAirspeed() test failed:\nexp: -1.444822947225264 != obs: {alphaTest}")
if betaTest!=-0.498778777844346:
  print(f"    CalculateAirspeed() test failed:\nexp: -0.498778777844346 != obs: {betaTest}") 
else:
  testsPassed+=1
  testsPassed4+=1


# VAM CalculateAirspeed() test 2
VaTest, alphaTest, betaTest = test.CalculateAirspeed(testState, test.Wind.windState)
if VaTest!=12.2091904870715:
  print(f"\n    CalculateAirspeed() test failed:\nexp: 12.2091904870715 != obs: {VaTest}")
if alphaTest!=0.7270587933331709:
  print(f"    CalculateAirspeed() test failed:\nexp: 0.7270587933331709 != obs: {alphaTest}")
if betaTest!=0.1629556774952688:
  print(f"    CalculateAirspeed() test failed:\nexp: 0.1629556774952688 != obs: {betaTest}")
else:
  testsPassed+=1
  testsPassed4+=1

print(f"  passed {testsPassed4}/2 tests")



########################################
# VAM update() test 1
########################################
testsPassed5 = 0
print("testing VAM update()")
testState = states.vehicleState(pn=4, pe=2, pd=6, u=2, v=1, w=5, yaw=7, pitch=2, roll=6, p=8, q=9, r=3)
testControls = inputs.controlInputs(Throttle=0.2, Aileron=0.9, Elevator=6.9, Rudder=4.2)
out = test.controlForces(testState, testControls)

if out.Fx!=9.678816841575113:
  print(f"\n    update() test failed:\nexp: 9.678816841575113 != obs: {out.Fx}")
if out.Fy!=9.055423574999997:
  print(f"    update() test failed:\nexp: 9.055423574999997 != obs: {out.Fy}")
if out.Fz!=-4.390389929418083:
  print(f"    update() test failed:\nexp: -4.390389929418083 != obs: {out.Fz}")

if out.Mx!=4.8739584883314935:
  print(f"    update() test failed:\nexp: 4.8739584883314935 != obs: {out.Mx}")
if out.My!=-13.575080586770996:
  print(f"    update() test failed:\nexp: -13.575080586770996 != obs: {out.My}")
if out.Mz!=-9.079606107198:
  print(f"    update() test failed:\nexp: -9.079606107198 != obs: {out.Mz}")
else:
  testsPassed+=1
  testsPassed5+=1


# VAM update() test 2
testState = states.vehicleState(pn=6.9, pe=4.2, pd=1.0, u=9.0, v=2.0, w=8.0, yaw=1.0, pitch=4.0, roll=5.0, p=4.0, q=1.0, r=2.0)
testControls = inputs.controlInputs(Throttle=0.5, Aileron=1.9, Elevator=4.9, Rudder=1.2)
out = test.controlForces(testState, testControls)

if out.Fx!=29.683092610929634:
  print(f"\n    update() test failed:\nexp: 29.683092610929634 != obs: {out.Fx}")
if out.Fy!=19.252845397500003:
  print(f"    update() test failed:\nexp: 19.252845397500003 != obs: {out.Fy}")
if out.Fz!=-27.02400072180782:
  print(f"    update() test failed:\nexp: -27.02400072180782 != obs: {out.Fz}")

if out.Mx!=48.552068035135214:
  print(f"    update() test failed:\nexp: 48.552068035135214 != obs: {out.Mx}")
if out.My!=-47.880030610635316:
  print(f"    update() test failed:\nexp: -47.880030610635316 != obs: {out.My}")
if out.Mz!=-15.603572221571405:
  print(f"    update() test failed:\nexp: -15.603572221571405 != obs: {out.Mz}")
else:
  testsPassed+=1
  testsPassed5+=1

print(f"  passed {testsPassed5}/2 tests")



########################################
# Thrust partial div() test 1
########################################
testsPassed6 = 0
print("testing partial div()")

out = VPM.dThrust_dThrottle(25, 0.5)

if out!=62.55845796331059:
  print(f"\n    dThrust_dThrottle() test 1 failed:\nexp: 62.55845796331059 != obs: {out}")
else:
  testsPassed+=1
  testsPassed6+=1


# Thrust partial div() test 2
out = VPM.dThrust_dVa(32, 0.1)

if out!=-2.4486387395323987:
  print(f"\n    dThrust_dThrottle() test 2 failed:\nexp: -2.4486387395323987 != obs: {out}")
else:
  testsPassed+=1
  testsPassed6+=1

print(f"  passed {testsPassed6}/2 tests")



########################################
# VPM CreateTransferFunction() test 1
########################################
testsPassed7 = 0
print("testing VPM CreateTransferFunction()")

out = VPM.CreateTransferFunction(testState, testControls)

if out.gamma_trim!=3.2733576593182745:
  print(f"\n    CreateTransferFunction() test 1 failed:\nexp: 3.2733576593182745 != obs: {out.gamma_trim}")
if out.a_beta1!=0.3792686688809004:
  print(f"    CreateTransferFunction() test 2 failed:\nexp: 0.3792686688809004 != obs: {out.a_beta1}")
if out.a_theta1!=2.585220700206326:
  print(f"    CreateTransferFunction() test 3 failed:\nexp: 2.585220700206326 != obs: {out.a_theta1}")
else:
  testsPassed+=1
  testsPassed7+=1


# VPM CreateTransferFunction() test 2
if out.theta_trim!=4.0:
  print(f"\n    CreateTransferFunction() test 1 failed:\nexp: 4.0 != obs: {out.theta_trim}")
if out.a_phi2!=31.202668882748984:
  print(f"    CreateTransferFunction() test 2 failed:\nexp: 31.202668882748984 != obs: {out.a_phi2}")
if out.a_V1!=0.2250946887715597:
  print(f"    CreateTransferFunction() test 3 failed:\nexp: 0.2250946887715597 != obs: {out.a_V1}")
else:
  testsPassed+=1
  testsPassed7+=1

print(f"  passed {testsPassed7}/2 tests")

# Prints the final total, as well as a statement if all tests were passed
print(f"\npassed {testsPassed}/{testTotal} tests")
if testsPassed == testTotal:
  print(f"  passed all {testTotal} tests")