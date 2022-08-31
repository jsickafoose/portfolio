#############################################
#   Created by Jacob Sickafoose - jsickafo  #
#############################################

import ece163.Containers.States as states
import ece163.Containers.Inputs as inputs
import ece163.Constants.VehiclePhysicalConstants as VPC
import ece163.Modeling.VehicleAerodynamicsModel as VAM
import ece163.Controls.VehicleControlGains as VCG
import ece163.Controls.VehicleClosedLoopControl as VCLC
import ece163.Containers.Controls as Controls
import ece163.Containers.Linearized as Linearized

# Establishes the AerodynamicsModel object we will test
test = VAM.VehicleAerodynamicsModel()
testState = states.vehicleState(pn=6.9, pe=4.2, pd=1.0, u=9.0, v=2.0, w=8.0, yaw=1.0, pitch=4.0, roll=5.0, p=4.0, q=1.0, r=2.0)
test.setVehicleState(testState)
# Sets the how many tests there are, and initializes a counting variable for them
testTotal = 12
testsPassed = 0


########################################
# GaussMarkovXYZ() test 1
########################################
testsPassed1 = 0
print("\ntesting VehicleControlGains computeGains()")  # Announce which test we're on

# plug in random test variables
tune = Controls.controlTuning(2.12341234124, 6.2344, 7.737, 2.177276, 4.2347, 5.26773, 6.1562677, 7.1234, 2.54, 1.2345, 6.525, 4.5252, 1.7983, 3)
transfer = Linearized.transferFunctions(37, 55, 67, 94, 53, 80, 88, 64, 86, 83, 12, 44, 48, 73, 76, 75)
gainsOut = VCG.computeGains(tune, transfer)

# Check if each individual expected output variable is right. If it isn't, prints exp vs. obs
if gainsOut.kp_pitch!=-0.12709100012368144:
  print(f"\n    computeGains() test failed:\nexp: -0.12709100012368144 != obs: {gainsOut.kp_pitch}")
if gainsOut.kp_pitch!=-0.12709100012368144:
  print(f"    computeGains() test failed:\nexp: -0.12709100012368144 != obs: {gainsOut.kp_pitch}")
if gainsOut.ki_SpeedfromThrottle!=0.5602055921052632:
  print(f"    computeGains() test failed:\nexp: 0.5602055921052632 != obs: {gainsOut.ki_SpeedfromThrottle}")
else:     # If all tests check out, adds to total
  testsPassed+=1
  testsPassed1+=1


# GaussMarkovXYZ() test 2, does the same test again with different random variables
tune = Controls.controlTuning(72, 61, 92, 66, 47, 1, 15, 39, 22, 24, 90, 38, 6, 17)
transfer = Linearized.transferFunctions(85, 43, 27, 84, 89, 71, 4, 74, 25, 3, 70, 82, 20, 95, 52, 35)
gainsOut = VCG.computeGains(tune, transfer)

if gainsOut.kp_altitude!=19.547511312217196:
  print(f"\n    computeGains() test failed:\nexp: 19.547511312217196 != obs: {gainsOut.kp_altitude}")
if gainsOut.kd_roll!=118.64864864864865:
  print(f"    computeGains() test failed:\nexp: 118.64864864864865 != obs: {gainsOut.kd_roll}")
if gainsOut.ki_course!=73337.41080530071:
  print(f"    computeGains() test failed:\nexp: 73337.41080530071 != obs: {gainsOut.ki_course}")
else:
  testsPassed+=1
  testsPassed1+=1

print(f"  passed {testsPassed1}/2 tests")  # Prints out how many gravityForces() tests passed



########################################
# updateAccelsTrue() test 1
########################################
testsPassed2 = 0
print("testing VehicleControlGains computeTuningParameters()")
tuneParamsOut = VCG.computeTuningParameters(gainsOut, transfer)

if tuneParamsOut.Wn_roll!=72.0:
  print(f"\n    computeTuningParameters() test failed:\nexp: 72.0 != obs: {tuneParamsOut.Wn_roll}")
if tuneParamsOut.Wn_course!=92.0:
  print(f"    computeTuningParameters() test failed:\nexp: 92.0 != obs: {tuneParamsOut.Wn_course}")
if tuneParamsOut.Wn_pitch!=15.0:
  print(f"    computeTuningParameters() test failed:\nexp: 15.0 != obs: {tuneParamsOut.Wn_pitch}")
else:
  testsPassed+=1
  testsPassed2+=1


# updateAccelsTrue() test 2
transfer = Linearized.transferFunctions(37, 55, 67, 94, 53, 80, 88, 64, 86, 83, 12, 44, 48, 73, 76, 75)
tuneParamsOut = VCG.computeTuningParameters(gainsOut, transfer)

if tuneParamsOut.Zeta_roll!=57.36013696738427:
  print(f"\n    computeTuningParameters() test failed:\nexp: 57.36013696738427 != obs: {tuneParamsOut.Zeta_roll}")
if tuneParamsOut.Zeta_course!=100.03512896491425:
  print(f"    computeTuningParameters() test failed:\nexp: 100.03512896491425 != obs: {tuneParamsOut.Zeta_course}")
if tuneParamsOut.Zeta_altitude!=18.699579752933353:
  print(f"    computeTuningParameters() test failed:\nexp: 18.699579752933353 != obs: {tuneParamsOut.Zeta_altitude}")
else:
  testsPassed+=1
  testsPassed2+=1

print(f"  passed {testsPassed2}/2 tests")



########################################
#  updateGyrosTrue() test 1
########################################
testsPassed3 = 0
print("testing VehicleClosedLoopControl PIDControl()")

PID = VCLC.PIDControl(VPC.dT, 71, 4, 74, 25, 3, 70)
outPID = PID.Update(2, 3, 5)

if outPID!=3:
  print(f"\n    PIDControl() test failed:\nexp: 3 != obs: {outPID}")
else:
  testsPassed+=1
  testsPassed3+=1


# updateGyrosTrue() test 2
PID = VCLC.PIDControl(VPC.dT, 4, 56, 23, 64, 2, 26)
outPID = PID.Update(2.2, 13.2, 46.7)

if outPID!=2:
  print(f"\n    PIDControl() test failed:\nexp: 2 != obs: {outPID}")
else:
  testsPassed+=1
  testsPassed3+=1

print(f"  passed {testsPassed3}/2 tests")



########################################
#  updateMagsTrue() test 1
########################################
testsPassed4 = 0
print("testing VehicleClosedLoopControl PIControl()")

PI = VCLC.PIControl(VPC.dT, 71, 4, 74, 3, 70)
outPI = PI.Update(2, 3)

if outPI!=3:
  print(f"\n    PIControl() test failed:\nexp: 3 != obs: {outPI}")
else:
  testsPassed+=1
  testsPassed4+=1


# updateMagsTrue() test 2
PI = VCLC.PIControl(VPC.dT, 4, 56, 23, 64, 26)
outPI = PI.Update(2.2, 13.2)

if outPI!=64:
  print(f"\n    PIControl() test failed:\nexp: 64 != obs: {outPI}")
else:
  testsPassed+=1
  testsPassed4+=1

print(f"  passed {testsPassed4}/2 tests")



########################################
#  updateGPSTrue() test 1
########################################
testsPassed5 = 0
print("testing VehicleClosedLoopControl PDControl()")

PD = VCLC.PDControl(VPC.dT, 71, 4, 3, 70)
outPD = PD.Update(2, 3)

if outPD!=3.99:
  print(f"\n    PDControl() test failed:\nexp: 3.99 != obs: {outPD}")
else:
  testsPassed+=1
  testsPassed5+=1


# updateGPSTrue() test 2
PD = VCLC.PDControl(VPC.dT, 4, 23, 64, 26)
outPD = PD.Update(2.2, 13.2)

if outPD!=64:
  print(f"\n    PDControl() test failed:\nexp: 64 != obs: {outPD}")
else:
  testsPassed+=1
  testsPassed5+=1

print(f"  passed {testsPassed5}/2 tests")



########################################
# updatePressureSensorsTrue() test 1
########################################
testsPassed6 = 0
print("testing VehicleClosedLoopControl setControlGains()")
closedLoop = VCLC.VehicleClosedLoopControl()
gains = Controls.controlGains(139, 679, 477, 412, 931, 96, 763, 104, 519, 398, 503, 938, 725, 470, 182)

closedLoop.setControlGains(gains)

if closedLoop.rollFromCourse.kp!=96:
  print(f"\n    setControlGains() test failed:\nexp: 96 != obs: {closedLoop.rollFromCourse.kp}")
if closedLoop.rudderFromSideslip.kp!=412:
  print(f"    setControlGains() test failed:\nexp: 412 != obs: {closedLoop.rudderFromSideslip.kp}")
if closedLoop.pitchFromAltitude.kp!=398:
  print(f"    setControlGains() test failed:\nexp: 398 != obs: {closedLoop.pitchFromAltitude.kp}")

if closedLoop.elevatorFromPitch.kp!=104:
  print(f"    setControlGains() test failed:\nexp: 104 != obs: {closedLoop.elevatorFromPitch.kp}")
if closedLoop.aileronFromRoll.kp!=139:
  print(f"    setControlGains() test failed:\nexp: 139 != obs: {closedLoop.aileronFromRoll.kp}")
if closedLoop.throttleFromAirspeed.kp!=938:
  print(f"    setControlGains() test failed:\nexp: 938 != obs: {closedLoop.throttleFromAirspeed.kp}")
else:
  testsPassed+=1
  testsPassed6+=1

# updatePressureSensorsTrue Test 2
gains = Controls.controlGains(492, 817, 696, 755, 469, 484, 222, 428, 363, 708, 240, 284, 131, 743, 140)
closedLoop.setControlGains(gains)

if closedLoop.rollFromCourse.kp!=484:
  print(f"\n    setControlGains() test failed:\nexp: 484 != obs: {closedLoop.rollFromCourse.kp}")
if closedLoop.rudderFromSideslip.kp!=755:
  print(f"    setControlGains() test failed:\nexp: 755 != obs: {closedLoop.rudderFromSideslip.kp}")
if closedLoop.pitchFromAltitude.kp!=708:
  print(f"    setControlGains() test failed:\nexp: 708 != obs: {closedLoop.pitchFromAltitude.kp}")

if closedLoop.elevatorFromPitch.kp!=428:
  print(f"    setControlGains() test failed:\nexp: 428 != obs: {closedLoop.elevatorFromPitch.kp}")
if closedLoop.aileronFromRoll.kp!=492:
  print(f"    setControlGains() test failed:\nexp: 492 != obs: {closedLoop.aileronFromRoll.kp}")
if closedLoop.throttleFromAirspeed.kp!=284:
  print(f"    setControlGains() test failed:\nexp: 284 != obs: {closedLoop.throttleFromAirspeed.kp}")
else:
  testsPassed+=1
  testsPassed6+=1

print(f"  passed {testsPassed6}/2 tests")




# Prints the final total, as well as a statement if all tests were passed
print(f"\npassed {testsPassed}/{testTotal} tests")
if testsPassed == testTotal:
  print(f"  passed all {testTotal} tests")