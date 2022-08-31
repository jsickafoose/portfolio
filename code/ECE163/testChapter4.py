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
import ece163.Modeling.VehicleAerodynamicsModel as VAM

# Establishes the AerodynamicsModel object we will test
test = VAM.VehicleAerodynamicsModel()
testState = states.vehicleState(pn=6.9, pe=4.2, pd=1.0, u=9.0, v=2.0, w=8.0, yaw=1.0, pitch=4.0, roll=5.0, p=4.0, q=1.0, r=2.0)
test.setVehicleState(testState)

# Sets the how many tests there are, and initializes a counting variable for them
testTotal = 14
testsPassed = 0


########################################
# gravityForces() test 1
########################################
gravityTest = 0                     # Test variable for specifically gravity tests
print("\ntesting gravityForces()")  # Announce which test we're on

# plug in random test variables
forces = test.gravityForces(testState)

# Check if each individual expected output variable is right. If it isn't, prints exp vs. obs
if forces.Fx!=81.66655726867853:
  print(f"\n    gravityForces() test failed:\nexp Fx: 81.66655726867853 != obs: {forces.Fx}")
if forces.Fy!=67.63741985652904:
  print(f"    gravityForces() test failed:\nexp Fy: 67.63741985652904 != obs: {forces.Fy}")
if forces.Fz!=-20.00802236687227:
  print(f"    gravityForces() test failed:\nexp Fz: -20.00802236687227 != obs: {forces.Fz}")
else:     # If all tests check out, adds to total
  testsPassed+=1
  gravityTest+=1


# gravityForces() test 2, does the same test again with different random variables
testState = states.vehicleState(pn=4, pe=2, pd=6, u=2, v=1, w=5, yaw=7, pitch=2, roll=6, p=8, q=9, r=3)
forces = test.gravityForces(testState)

if forces.Fx!=-98.12228532875932:
  print(f"\n    gravityForces() test failed:\nexp Fx: -98.12228532875932 != obs: {forces.Fx}")
if forces.Fy!=12.547545562225295:
  print(f"    gravityForces() test failed:\nexp Fy: 12.547545562225295 != obs: {forces.Fy}")
if forces.Fz!=-43.11779588783993:
  print(f"    gravityForces() test failed:\nexp Fz: -43.11779588783993 != obs: {forces.Fz}")
else:
  testsPassed+=1
  gravityTest+=1

print(f"  passed {gravityTest}/2 tests")  # Prints out how many gravityForces() tests passed



########################################
# CalculateCoeff_alpha() test 1
########################################
coeffTest = 0
print("testing CalculateCoeff_alpha()")
alpha = -2.9670597283903604
out = test.CalculateCoeff_alpha(alpha)

if out[0]!=0.3420201433256686:
  print(f"\n    CalculateCoeff_alpha() test failed:\nexp C_L: 0.3420201433256686 != obs: {out[0]}")
if out[1]!=0.060307379214091565:
  print(f"    CalculateCoeff_alpha() test failed:\nexp C_D: 0.060307379214091565 != obs: {out[1]}")
if out[2]!=8.143243655789588:
  print(f"    CalculateCoeff_alpha() test failed:\nexp C_M: 8.143243655789588 != obs: {out[2]}")
else:
  testsPassed+=1
  coeffTest+=1


# CalculateCoeff_alpha() test 2
alpha =  -0.89
out = test.CalculateCoeff_alpha(alpha)
(-0.9781966098612083, 1.2076810010591086, 2.4521)
if out[0]!=-0.9781966098612083:
  print(f"\n    CalculateCoeff_alpha() test failed:\nexp C_L: -0.9781966098612083 != obs: {out[0]}")
if out[1]!=1.2076810010591086:
  print(f"    CalculateCoeff_alpha() test failed:\nexp C_D: 1.2076810010591086 != obs: {out[1]}")
if out[2]!=2.4521:
  print(f"    CalculateCoeff_alpha() test failed:\nexp C_M: 2.4521 != obs: {out[2]}")
else:
  testsPassed+=1
  coeffTest+=1

print(f"  passed {coeffTest}/2 tests")



########################################
# aeroForces() test 1
########################################
aeroTest = 0
print("testing aeroForces()")
testState = states.vehicleState(pn=4, pe=2, pd=6, u=2, v=1, w=5, yaw=7, pitch=2, roll=6, p=8, q=9, r=3)
out = test.aeroForces(testState)

if out.Fx!=12.051695537150257:
  print(f"\n    aeroForces() test failed:\nexp Fx: 12.051695537150257 != obs: {out.Fx}")
if out.Fy!=-1.8825648081818322:
  print(f"    aeroForces() test failed:\nexp Fy: -1.8825648081818322 != obs: {out.Fy}")
if out.Fz!=-24.249331514641412:
  print(f"    aeroForces() test failed:\nexp Fz: -24.249331514641412 != obs: {out.Fz}")

if out.Mx!=-27.390006916298503:
  print(f"    aeroForces() test failed:\nexp Mx: -27.390006916298503 != obs: {out.Mx}")
if out.My!=-18.304056375262817:
  print(f"    aeroForces() test failed:\nexp My: -18.304056375262817 != obs: {out.My}")
if out.Mz!=2.5442118089942256:
  print(f"    aeroForces() test failed:\nexp Mz: 2.5442118089942256 != obs: {out.Mz}")
else:
  testsPassed+=1
  aeroTest+=1


# aeroForces() test 2
testState = states.vehicleState(pn=6.9, pe=4.2, pd=1.0, u=9.0, v=2.0, w=8.0, yaw=1.0, pitch=4.0, roll=5.0, p=4.0, q=1.0, r=2.0)
out = test.aeroForces(testState)

if out.Fx!=2.1357453108915876:
  print(f"\n    aeroForces() test failed:\nexp Fx: 2.1357453108915876 != obs: {out.Fx}")
if out.Fy!=-8.381701992246455:
  print(f"    aeroForces() test failed:\nexp Fy: -8.381701992246455 != obs: {out.Fy}")
if out.Fz!=-71.44927556737264:
  print(f"    aeroForces() test failed:\nexp Fz: -71.44927556737264 != obs: {out.Fz}")

if out.Mx!=-30.703592069328593:
  print(f"    aeroForces() test failed:\nexp Mx: -30.703592069328593 != obs: {out.Mx}")
if out.My!=-22.452419924207724:
  print(f"    aeroForces() test failed:\nexp My: -22.452419924207724 != obs: {out.My}")
if out.Mz!=3.342697613487905:
  print(f"    aeroForces() test failed:\nexp Mz: 3.342697613487905 != obs: {out.Mz}")
else:
  testsPassed+=1
  aeroTest+=1

print(f"  passed {aeroTest}/2 tests")



########################################
# CalculatePropForces() test 1
########################################
propTest = 0
print("testing CalculatePropForces()")
Va = 30
Throttle = 0
out = test.CalculatePropForces(Va, Throttle)

if out[0]!=-32.76725410628669:
  print(f"\n    CalculatePropForces() test failed:\nexp Fx: -32.76725410628669 != obs: {out[0]}")
if out[1]!=2.441466592348481:
  print(f"    CalculatePropForces() test failed:\nexp Mx: 2.441466592348481 != obs: {out[1]}")
else:
  testsPassed+=1
  propTest+=1


# CalculatePropForces() test 2
Va = 12
Throttle = .8
out = test.CalculatePropForces(Va, Throttle)

if out[0]!=39.656685106597735:
  print(f"\n    CalculatePropForces() test failed:\nexp Fx: 39.656685106597735 != obs: {out[0]}")
if out[1]!=-1.57646832257723:
  print(f"    CalculatePropForces() test failed:\nexp Mx: -1.57646832257723 != obs: {out[1]}")
else:
  testsPassed+=1
  propTest+=1

print(f"  passed {propTest}/2 tests")



########################################
# controlForces() test 1
########################################
controlTest = 0
print("testing controlForces()")
testState = states.vehicleState(pn=4, pe=2, pd=6, u=2, v=1, w=5, yaw=7, pitch=2, roll=6, p=8, q=9, r=3)
testControls = inputs.controlInputs(Throttle=0.2, Aileron=0.9, Elevator=6.9, Rudder=4.2)
out = test.controlForces(testState, testControls)

if out.Fx!=9.678816841575113:
  print(f"\n    controlForces() test failed:\nexp Fx: 9.678816841575113 != obs: {out.Fx}")
if out.Fy!=9.055423574999997:
  print(f"    controlForces() test failed:\nexp Fy: 9.055423574999997 != obs: {out.Fy}")
if out.Fz!=-4.390389929418083:
  print(f"    controlForces() test failed:\nexp Fz: -4.390389929418083 != obs: {out.Fz}")

if out.Mx!=4.8739584883314935:
  print(f"    controlForces() test failed:\nexp Mx: 4.8739584883314935 != obs: {out.Mx}")
if out.My!=-13.575080586770996:
  print(f"    controlForces() test failed:\nexp My: -13.575080586770996 != obs: {out.My}")
if out.Mz!=-9.079606107198:
  print(f"    controlForces() test failed:\nexp Mz: -9.079606107198 != obs: {out.Mz}")
else:
  testsPassed+=1
  controlTest+=1


# controlForces() test 2
testState = states.vehicleState(pn=6.9, pe=4.2, pd=1.0, u=9.0, v=2.0, w=8.0, yaw=1.0, pitch=4.0, roll=5.0, p=4.0, q=1.0, r=2.0)
testControls = inputs.controlInputs(Throttle=0.5, Aileron=1.9, Elevator=4.9, Rudder=1.2)
out = test.controlForces(testState, testControls)

if out.Fx!=29.683092610929634:
  print(f"\n    controlForces() test failed:\nexp Fx: 29.683092610929634 != obs: {out.Fx}")
if out.Fy!=19.252845397500003:
  print(f"    controlForces() test failed:\nexp Fy: 19.252845397500003 != obs: {out.Fy}")
if out.Fz!=-27.02400072180782:
  print(f"    controlForces() test failed:\nexp Fz: -27.02400072180782 != obs: {out.Fz}")

if out.Mx!=48.552068035135214:
  print(f"    controlForces() test failed:\nexp Mx: 48.552068035135214 != obs: {out.Mx}")
if out.My!=-47.880030610635316:
  print(f"    controlForces() test failed:\nexp My: -47.880030610635316 != obs: {out.My}")
if out.Mz!=-15.603572221571405:
  print(f"    controlForces() test failed:\nexp Mz: -15.603572221571405 != obs: {out.Mz}")
else:
  testsPassed+=1
  controlTest+=1

print(f"  passed {controlTest}/2 tests")



########################################
# updateForces() test 1
########################################
updateTest = 0
print("testing updateForces()")

testState = states.vehicleState(pn=6.9, pe=4.2, pd=1.0, u=9.0, v=2.0, w=8.0, yaw=1.0, pitch=4.0, roll=5.0, p=4.0, q=1.0, r=2.0)
testControls = inputs.controlInputs(Throttle=0.5, Aileron=1.9, Elevator=4.9, Rudder=1.2)
out = test.updateForces(testState, testControls)

if out.Fx!=113.48539519049976:
  print(f"\n    updateForces() test failed:\nexp Fx: 113.48539519049976 != obs: {out.Fx}")
if out.Fy!=78.50856326178258:
  print(f"    updateForces() test failed:\nexp Fy: 78.50856326178258 != obs: {out.Fy}")
if out.Fz!=-118.48129865605273:
  print(f"    updateForces() test failed:\nexp Fz: -118.48129865605273 != obs: {out.Fz}")

if out.Mx!=17.84847596580662:
  print(f"    updateForces() test failed:\nexp Mx: 17.84847596580662 != obs: {out.Mx}")
if out.My!=-70.33245053484305:
  print(f"    updateForces() test failed:\nexp My: -70.33245053484305 != obs: {out.My}")
if out.Mz!=-12.2608746080835:
  print(f"    updateForces() test failed:\nexp Mz: -12.2608746080835 != obs: {out.Mz}")
else:
  testsPassed+=1
  updateTest+=1


# updateForces() test 2
testState = states.vehicleState(pn=4, pe=2, pd=6, u=2, v=1, w=5, yaw=7, pitch=2, roll=6, p=8, q=9, r=3)
testControls = inputs.controlInputs(Throttle=0.2, Aileron=0.9, Elevator=6.9, Rudder=4.2)
out = test.updateForces(testState, testControls)

if out.Fx!=-76.39177295003395:
  print(f"\n    updateForces() test failed:\nexp Fx: -76.39177295003395 != obs: {out.Fx}")
if out.Fy!=19.72040432904346:
  print(f"    updateForces() test failed:\nexp Fy: 19.72040432904346 != obs: {out.Fy}")
if out.Fz!=-71.75751733189942:
  print(f"    updateForces() test failed:\nexp Fz: -71.75751733189942 != obs: {out.Fz}")

if out.Mx!=-22.51604842796701:
  print(f"    updateForces() test failed:\nexp Mx: -22.51604842796701 != obs: {out.Mx}")
if out.My!=-31.87913696203381:
  print(f"    updateForces() test failed:\nexp My: -31.87913696203381 != obs: {out.My}")
if out.Mz!=-6.535394298203775:
  print(f"    updateForces() test failed:\nexp Mz: -6.535394298203775 != obs: {out.Mz}")
else:
  testsPassed+=1
  updateTest+=1

print(f"  passed {updateTest}/2 tests")



########################################
# Update() test 1
########################################
finalTest = 0
print("testing Update()")

testControls = inputs.controlInputs(Throttle=0.5, Aileron=1.9, Elevator=4.9, Rudder=1.2)
test.Update(testControls)

if test.VDM.state.pn!=6.797451627537033:
  print(f"\n    Update() test failed:\nexp pn: 6.79745162753703 != obs: {test.VDM.state.pn}")
if test.VDM.state.pe!=4.192773870771712:
  print(f"    Update() test failed:\nexp pe: 4.192773870771712 != obs: {test.VDM.state.pe}")
if test.VDM.state.pd!=1.0658150010375487:
  print(f"    Update() test failed:\nexp pd: 1.0658150010375487 != obs: {test.VDM.state.pd}")

if test.VDM.state.u!=9.063168541082273:
  print(f"    Update() test failed:\nexp u: 9.063168541082273 != obs: {test.VDM.state.u}")
if test.VDM.state.v!=2.211371421147075:
  print(f"    Update() test failed:\nexp v: 2.211371421147075 != obs: {test.VDM.state.v}")
if test.VDM.state.w!=7.902289728494497:
  print(f"    Update() test failed:\nexp w: 7.902289728494497 != obs: {test.VDM.state.w}")

if test.VDM.state.p!=4.197771812927773:
  print(f"    Update() test failed:\nexp p: 4.197771812927773 != obs: {test.VDM.state.p}")
if test.VDM.state.q!=0.4334762067414709:
  print(f"    Update() test failed:\nexp q: 0.4334762067414709 != obs: {test.VDM.state.q}")
if test.VDM.state.r!=1.9354013531527396:
  print(f"    Update() test failed:\nexp r: 1.9354013531527396 != obs: {test.VDM.state.r}")
else:
  testsPassed+=1
  finalTest+=1


# Update() test 2
testControls = inputs.controlInputs(Throttle=0.2, Aileron=0.9, Elevator=6.9, Rudder=4.2)
test.Update(testControls)

if test.VDM.state.pn!=6.695421652097118:
  print(f"\n    Update() test failed:\nexp pn: 6.695421652097118 != obs: {test.VDM.state.pn}")
if test.VDM.state.pe!=4.185366464870001:
  print(f"    Update() test failed:\nexp pe: 4.185366464870001 != obs: {test.VDM.state.pe}")
if test.VDM.state.pd!=1.1327683542133051:
  print(f"    Update() test failed:\nexp pd: 1.1327683542133051 != obs: {test.VDM.state.pd}")

if test.VDM.state.u!=9.168867960295495:
  print(f"    Update() test failed:\nexp u: 9.168867960295495 != obs: {test.VDM.state.u}")
if test.VDM.state.v!=2.4594824742027894:
  print(f"    Update() test failed:\nexp v: 2.4594824742027894 != obs: {test.VDM.state.v}")
if test.VDM.state.w!=7.730431852577511:
  print(f"    Update() test failed:\nexp w: 7.730431852577511 != obs: {test.VDM.state.w}")

if test.VDM.state.p!=4.056206874529368:
  print(f"    Update() test failed:\nexp p: 4.056206874529368 != obs: {test.VDM.state.p}")
if test.VDM.state.q!=-0.29173694650262694:
  print(f"    Update() test failed:\nexp q: -0.29173694650262694 != obs: {test.VDM.state.q}")
if test.VDM.state.r!=1.6868770192578526:
  print(f"    Update() test failed:\nexp r: 1.6868770192578526 != obs: {test.VDM.state.r}")
else:
  testsPassed+=1
  finalTest+=1

print(f"  passed {finalTest}/2 tests")

# Prints the final total, as well as a statement if all tests were passed
print(f"\npassed {testsPassed}/{testTotal} tests")
if testsPassed == testTotal:
  print(f"  passed all {testTotal} tests")