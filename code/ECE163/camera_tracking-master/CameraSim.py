## Imports
import math

class CameraSim:
    '''
     Stores the camera object. Keeps track of it's pitch and yaw angles. The object also points the camera around,
     differently depending on search vs tracking mode. Finally, capable of calculating what point on the ground the
     camera is pointing at and seeing if the target vehicle is within the scope.
    '''
    def __init__(self, yaw=0, pitch=1, mode='Searching', camera_radius=20): # Store yaw and pitch angles (degrees) for the camera
        self.yaw = yaw
        self.pitch = pitch
        self.mode = mode
        self.camera_radius = camera_radius

    def reset(self):
        self.yaw = 0
        self.pitch = 0
        self.mode = 'Searching'

    '''
    Update camera. The method of updating, changes depending on the internal mode value.
    Also calls getGroundPoint and detectTarget to internally change the mode. This makes it
    so the main only needs to call CameraSim.update()

    In search mode, the camera at [0, 0] yaw and pitch is pointing straight down. It increments pitch up
    by either 1, or an amount calculated based on what altitude the MAV is at.

    In Tracking mode, the camera just calculates yaw and pitch required to be pointing at the target. This also 
    should account for the MAV's current attitude


    Parameters: TargetState - stores [n, e, d] of the target
                MAVState - stores [n, e, d] of our MAV, as well as how to counteract it's current yaw, pitch, roll

    Returns:    None

    '''
    def Update(self, TargetState, MAVState):
        ## First check what mode we are in
        if self.mode == 'Following':
            # Calculate pitch and yaw using target [n, e, d] and MAV [n, e, d]
            
            n_local = TargetState.pn - MAVState.pn
            e_local = TargetState.pe - MAVState.pe

            R = math.sqrt(n_local**2 + e_local**2)

            self.pitch = math.atan2(R, -MAVState.pd)
            self.yaw = math.atan2(e_local, n_local)

            return 

        else: #move camera in circular motion
            if(self.yaw == 360):
                self.yaw = 0
                if(self.pitch == 25):
                    self.pitch = 0
                else:
                    self.pitch = self.pitch + .1
            else:
                self.yaw = self.yaw + .1
            self.detectTarget(TargetState, MAVState)
            return

    def getGroundPoint(self, MAVState):
        R = -MAVState.pd * math.tan(self.pitch) #calculate magnatude of ground distance between UAV and target
        N = R*math.cos(self.yaw) #calculate north distnce of UAV to target
        E = R*math.sin(self.yaw) #calculate east distance of UAV to target

        n_global = N + MAVState.pn #calculate the global north point of the camera ground point
        e_global = E + MAVState.pe #calculate the global east point of the camera ground point
        return n_global, e_global


    def detectTarget(self, TargetState, MAVState):
        cameraPoint = self.getGroundPoint(MAVState)

        if(((cameraPoint[0] - TargetState.pn)**2 + (cameraPoint[1] - TargetState.pe)**2) < self.camera_radius**2):
            self.mode = 'Following'
            #print("target found")
            return True
        else:
            self.mode = 'Searching'
            return False