import ece163.Controls.VehicleClosedLoopControl as VCLC
import ece163.Containers.States as States
import ece163.Containers.Controls as Controls
import ece163.Constants.VehiclePhysicalConstants as VPC
import CameraSim as CS
import OrbitFollowPath as OFP
from  matplotlib  import  pyplot  as plt
import matplotlib.animation as animation
import math
import numpy 

## Inits the objects
vclc = VCLC.VehicleClosedLoopControl()
MAVState = vclc.getVehicleState()
TargetState = States.vehicleState(pn=-1000, pe=-3000, pd=0) # Records NED position of target, contains UpdateTarget() to change location
CameraSim = CS.CameraSim()
control_commands = Controls.referenceCommands(courseCommand=VPC.InitialYawAngle, altitudeCommand=100, airspeedCommand=VPC.InitialSpeed) #instance of reference commands

# Sets gains
vclc.setControlGains(Controls.controlGains(kp_roll = 3.0, kd_roll = 0.04, ki_roll = 0.001, kp_sideslip = 2.0, ki_sideslip = 2.0,
	kp_course = 5.0, ki_course = 2.0, kp_pitch = -10.0, kd_pitch = -0.8, kp_altitude = 0.08, ki_altitude = 0.03,
	kp_SpeedfromThrottle = 2.0, ki_SpeedfromThrottle = 1.0, kp_SpeedfromElevator = -0.5, ki_SpeedfromElevator = -0.1))

## Initial values for the orbitUpdate algorithm
orbit_radius 	   = 80 # m
rotation_direction = 1  # clockwise = 1, CCW = -1
k_orbit			   = 1  # Constant for how fast it aligns with follow path

## Initial time step values
simulation_time  = 600 # seconds
sim_steps = int(simulation_time/vclc.dT)

## Initializes arrays for each graph
time_record = [i*vclc.dT for i in range(sim_steps)] # X-axis

speed_record = []
course_record = []
pn_record = []
pe_record = []
height_record = []
commanded_course = []

camera_pn_record = []
camera_pe_record = []

targetLockFlag = False

target_pn_record = []
target_pe_record = []


for t in time_record:
	## If Camera is still searching
	if CameraSim.mode == 'Searching':
		# Calculate commanded course to target directly
		n_local = TargetState.pn - MAVState.pn
		e_local = TargetState.pe - MAVState.pe

		course = math.atan2(e_local, n_local)
	else:
		# Else, calculates commanded course using the FollowOrbit
		course  = OFP.FollowOrbit(TargetState, orbit_radius, rotation_direction, MAVState, k_orbit)[1]
	

	## Sets and updates the VCLC and CameraSim modules
	control_commands.commandedCourse = course
	vclc.Update(control_commands)
	CameraSim.Update(TargetState, MAVState)
	if(CameraSim.detectTarget(TargetState, MAVState) == True and targetLockFlag == False):
		targetLockFlag = True
		target_lock_pn = CameraSim.getGroundPoint(MAVState)[0]
		target_lock_pe = CameraSim.getGroundPoint(MAVState)[1]
	MAVState = vclc.getVehicleState()

	## Appends to our arrays for data to plot
	speed_record.append(MAVState.Va)
	course_record.append(MAVState.chi)
	pn_record.append(MAVState.pn)
	pe_record.append(MAVState.pe)
	height_record.append(-MAVState.pd)
	commanded_course.append(course)

	# Adds the dot for the camera center
	camera_coords = CameraSim.getGroundPoint(MAVState)
	camera_pn_record.append(camera_coords[0])
	camera_pe_record.append(camera_coords[1])


	## Vehicle starts moving after 150 seconds
	if(t > 250):
		TargetState.pe = TargetState.pe-.02
		TargetState.pn = TargetState.pn+.03
	else:
		TargetState.pe = TargetState.pe+.05
		TargetState.pn = TargetState.pn-.01

	if(t > 420):
		TargetState.pe = TargetState.pe+.02
		TargetState.pn = TargetState.pn+.03

	## Now we start plotting the target's location
	target_pe_record.append(TargetState.pe)
	target_pn_record.append(TargetState.pn)



## Graph commands
fig, axs = plt.subplots(2, 3, num="MAV State")
# Top row of plots
axs[0, 0].set_title("MAV Speed")
axs[0, 0].plot(time_record , speed_record)

axs[0, 1].set_title("MAV Course Angle")
axs[0, 1].plot(time_record , course_record)

axs[0, 2].set_title("Commanded Course Angle")
axs[0, 2].plot(time_record , commanded_course)

# Seconds row of plots
axs[1, 0].set_title("MAV Pn")
axs[1, 0].plot(time_record , pn_record)

axs[1, 1].set_title("MAV Pe")
axs[1, 1].plot(time_record , pe_record)

axs[1, 2].set_title("MAV Height")
axs[1, 2].plot(time_record , height_record)

## Plot course data 
fig2 = plt.figure("Course Test")
plt.title("Course Test")
plt.xlabel("East")
plt.ylabel("North")
plt.plot(pe_record, pn_record, label="UAV path")
plt.plot(target_pe_record, target_pn_record, label="Target")
plt.plot(MAVState.pe, MAVState.pn, 'bo')
plt.plot(TargetState.pe, TargetState.pn, 'yo')
plt.legend(loc = "best")

## Plot camera data 
fig3 = plt.figure("Camera Test")
plt.title("Camera Test")
plt.xlabel("East")
plt.ylabel("North")
plt.plot(target_pe_record, target_pn_record, 'g', label="Target")
plt.plot(camera_pe_record, camera_pn_record, ',', color='orange', label="Camera ground point")
plt.plot(target_lock_pe, target_lock_pn, '.', color='red', label="Target Lock")
plt.plot(pe_record, pn_record, 'b', label="UAV path")
plt.plot(MAVState.pe, MAVState.pn, 'bo')
plt.plot(TargetState.pe, TargetState.pn, 'go')
plt.legend(loc = "best")

# plots Three DD course data
plot3d = plt.figure("Course Test 3D")
plt.title("Course Test 3D")
ax = plt.axes(projection='3d')
ax.set_xlabel("East")
ax.set_ylabel("North")
ax.plot3D(pe_record, pn_record, height_record, label="UAV path")
ax.plot3D(target_pe_record, target_pn_record, TargetState.pd, label="Target")
ax.plot3D(MAVState.pe, MAVState.pn, -MAVState.pd, 'bo')
ax.plot3D(TargetState.pe, TargetState.pn, TargetState.pd, 'yo')
#ax.plot3D(loc = "best")

x_test = [TargetState.pe, MAVState.pe]
y_test = [TargetState.pn, MAVState.pn]
z_test = [TargetState.pd, -MAVState.pd]

ax.plot(x_test, y_test, z_test, 'r--')

#----------------------------------
# plots Three D course data with camera
plot3d = plt.figure("Course Test 3D and camera")
plt.title("Course Test 3D and camera")
axc = plt.axes(projection='3d')
axc.set_xlabel("East")
axc.set_ylabel("North")
axc.plot3D(pe_record, pn_record, height_record, 'b', label="UAV path")
axc.plot3D(target_pe_record, target_pn_record, TargetState.pd, 'g', label="Target")
axc.plot3D(camera_pe_record, camera_pn_record, 0, ',', color='orange', label="Camera ground point")
axc.plot3D(target_lock_pe, target_lock_pn, 0, '.', color='red', label="Target Lock")
axc.plot3D(MAVState.pe, MAVState.pn, -MAVState.pd, 'bo')
axc.plot3D(TargetState.pe, TargetState.pn, TargetState.pd, 'go')
#ax.plot3D(loc = "best")


plt.show()