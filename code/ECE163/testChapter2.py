"""This file is a test harness for the module ece163.Utilities.Rotations,
and for the method ece163.Modeling.VehicleGeometry.getNewPoints(). 

 It is meant to be run from the root directory of the repo with:

python testChapter2.py

at which point it will execute various tests on the Rotations module"""

#%% Initialization of test harness and helpers:

import math
import ece163.Utilities.MatrixMath as mm
import ece163.Utilities.Rotations as Rotations
import ece163.Modeling.VehicleGeometry as VG

"""math.isclose doesn't work well for comparing things near 0 unless we 
use an absolute tolerance, so we make our own isclose:"""
isclose = lambda  a,b : math.isclose(a, b, abs_tol= 1e-12)

def compareVectors(a, b):
	"""A quick tool to compare two vectors"""
	el_close = [isclose(a[i][0], b[i][0]) for i in range(3)]
	return all(el_close)

#of course, you should test your testing tools too:
assert(compareVectors([[0], [0], [-1]],[[1e-13], [0], [-1+1e-9]]))
assert(not compareVectors([[0], [0], [-1]],[[1e-11], [0], [-1]]))
assert(not compareVectors([[1e8], [0], [-1]],[[1e8+1], [0], [-1]]))



failed = []
passed = []
def evaluateTest(test_name, boolean):
	"""evaluateTest prints the output of a test and adds it to one of two 
	global lists, passed and failed, which can be printed later"""
	if boolean:
		print(f"   passed {test_name}")
		passed.append(test_name)
	else:
		print(f"   failed {test_name}")
		failed.append(test_name)
	return boolean


#%% Euler2dcm():
print("Beginning testing of Rotations.euler2DCM()")

cur_test = "Euler2DCM yaw test 1"
#we know that rotating [1,0,0] by 90 degrees about Z should produce [0,-1,0], so
R = Rotations.euler2DCM(90*math.pi/180, 0, 0)
orig_vec = [[1],[0],[0]]
expected_vec = [[0],[-1],[0]]
actual_vec = mm.matrixMultiply(R, orig_vec)
if not evaluateTest(cur_test, compareVectors(expected_vec, actual_vec) ):
	print(f"{expected_vec} != {actual_vec}")


#%%  

"""
Students, add more tests here.  
You aren't required to use the testing framework we've started here, 
but it will work just fine.
"""
#%% euler2DCM():
print("Beginning testing of Rotations.dcm2Euler()")

cur_test = "DCM2Euler yaw test 1"
dcm = [[4, 1, 0.5],
       [3, 2, 1],
       [1, 1, 3]]

R = Rotations.dcm2Euler(dcm)
expected_vec = [0.24497866312686414, -0.5235987755982989, 0.3217505543966422]
if not evaluateTest(cur_test, R == expected_vec):
	print(f"{expected_vec} != {actual_vec}")



#%% ned2enu():
print("Beginning testing of Rotations.ned2enu()")

cur_test = "NED2ENU yaw test 1"
ned = [[4, 1, 0.5],
       [3, 2, 1],
       [1, 1, 3]]
R = Rotations.ned2enu(ned)
expected_vec = [[1.0, 4.0, -0.5],
       			[2, 3, -1],
       			[1, 1, -3]]
if not evaluateTest(cur_test, R == expected_vec):
	print(f"{expected_vec} != {actual_vec}")



#%% Print results:

total = len(passed) + len(failed)
print(f"\n---\nPassed {len(passed)}/{total} tests")
[print("   " + test) for test in passed]

if failed:
	print(f"Failed {len(failed)}/{total} tests:")
	[print("   " + test) for test in failed]