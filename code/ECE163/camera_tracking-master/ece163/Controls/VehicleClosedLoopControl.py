"""
Duseok Choi
"""
import math
import sys
import ece163.Containers.Inputs as Inputs
import ece163.Containers.Controls as Controls
import ece163.Constants.VehiclePhysicalConstants as VPC
import ece163.Modeling.VehicleAerodynamicsModel as VehicleAerodynamicsModule

class PDControl():
    def __init__(self, kp=0.0, kd=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):

        self.kp = kp
        self.kd = kd
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit

        return

    
    def Update(self, command=0.0, current=0.0, derivative=0.0):
        
        err = command - current
        u = (self.kp * err) - (self.kd * derivative) + self.trim
        if (u < self.lowLimit):
            u = self.lowLimit
        elif (u > self.highLimit):
            u = self.highLimit

        return u


    def setPDGains(self, kp=0.0, kd=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):

        self.kp = kp
        self.kd = kd
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit

        return


class PIControl():
    
    def __init__(self, dT=VPC.dT, kp=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):

        self.dT = dT
        self.kp = kp
        self.ki = ki
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        self.accumulator = 0.0
        self.prevError = 0.0

        return



    def Update(self, command=0.0, current=0.0):

       
        err = command - current
        self.accumulator += ((1/2) * self.dT * (err + self.prevError))
        u = (self.kp * err) + (self.ki * self.accumulator) + self.trim

        if (u < self.lowLimit):
            u = self.lowLimit
            self.accumulator -= (1/2) * self.dT * (err + self.prevError)
        elif (u > self.highLimit):
            u = self.highLimit
            self.accumulator -= (1/2) * self.dT * (err + self.prevError)

        self.prevError = err

        return u


    def resetIntegrator(self):

        self.accumulator = 0.0
        self.prevError = 0.0

        return



    def setPIGains(self, dT=VPC.dT, kp=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):

        self.dT = dT
        self.kp = kp
        self.ki = ki
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit

        return

    
class PIDControl():
    
    def __init__(self, dT=VPC.dT, kp=0.0, kd=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):

        self.dT = dT
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        self.accumulator = 0.0
        self.prevError = 0.0

        return

    def Update(self, command=0.0, current=0.0, derivative=0.0):

        
        err = command - current
        self.accumulator += (1/2) * self.dT * (err + self.prevError)
        u = (self.kp * err) - (self.kd * derivative) + (self.ki * self.accumulator) + self.trim 

        if (u < self.lowLimit):
            u = self.lowLimit
            self.accumulator -= (1/2) * self.dT * (err + self.prevError)
        elif (u > self.highLimit):
            u = self.highLimit
            self.accumulator -= (1/2) * self.dT * (err + self.prevError)
        self.prevError = err

        return u


    def resetIntegrator(self):

        self.accumulator = 0.0
        self.prevError = 0.0

        return

    def setPIDGains(self, dT=VPC.dT, kp=0.0, kd=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):

        self.dT = dT
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit

        return

class VehicleClosedLoopControl():

    def __init__(self, dT=0.01, rudderControlSource='SIDESLIP'):

        self.VAM = VehicleAerodynamicsModule.VehicleAerodynamicsModel()
        self.dT = self.VAM.VehicleDynamics.dT
        self.VAM.VehicleDynamics.dT = dT
        self.rollFromCourse = PIControl()
        self.rudderFromSideslip = PIControl()
        self.throttleFromAirspeed = PIControl()
        self.pitchFromAltitude = PIControl()
        self.pitchFromAirspeed = PIControl()
        self.elevatorFromPitch = PDControl()
        self.aileronFromRoll = PIDControl()
        self.controlGain = Controls.controlGains()
        self.trimInputs = Inputs.controlInputs()
        self.consurOutputs = Inputs.controlInputs()
        self.mode = Controls.AltitudeStates.HOLDING
        #self.rudderControlSource = ? lab6
        return


    def Update(self, referenceCommands=Controls.referenceCommands()):
        
        updatecontrolcommand = self.UpdateControlCommands(referenceCommands,self.VAM.VehicleDynamics.state)   
        self.VAM.Update(updatecontrolcommand)
        return


    def UpdateControlCommands(self, referenceCommands, state):
        controlSurfaceOutput = Inputs.controlInputs()
 
        pd = state.pd
        pitch = state.pitch
        roll = state.roll
        p = state.p
        q = state.q
        Va = state.Va
        beta = state.beta
        chi = state.chi
        altitude = -state.pd
        
        #is it < or <=?
        courseError = referenceCommands.commandedCourse - chi
        if  courseError >= math.pi:
            chi += (2 * math.pi)
        elif courseError <= -math.pi:
             chi -= (2 * math.pi)
        
        rollCommand = self.rollFromCourse.Update(referenceCommands.commandedCourse, chi)
        aileronCommand = self.aileronFromRoll.Update(rollCommand, roll, p)
        rudderCommand = self.rudderFromSideslip.Update(0.0, beta)
        
        if altitude > (referenceCommands.commandedAltitude + VPC.altitudeHoldZone):
            if self.mode is not Controls.AltitudeStates.DESCENDING:
                self.mode = Controls.AltitudeStates.DESCENDING
                self.pitchFromAirspeed.resetIntegrator()

            throttleCmd = VPC.minControls.Throttle
            pitchCommand = self.pitchFromAirspeed.Update(referenceCommands.commandedAirspeed, Va)

        
        elif altitude < (referenceCommands.commandedAltitude - VPC.altitudeHoldZone):
            if self.mode is not Controls.AltitudeStates.CLIMBING:
                self.mode = Controls.AltitudeStates.CLIMBING
                self.pitchFromAirspeed.resetIntegrator()

            throttleCmd = VPC.maxControls.Throttle
            pitchCommand = self.pitchFromAirspeed.Update(referenceCommands.commandedAirspeed, Va)

        elif ((referenceCommands.commandedAltitude - VPC.altitudeHoldZone) < altitude < (referenceCommands.commandedAltitude + VPC.altitudeHoldZone)):
            if self.mode is not Controls.AltitudeStates.HOLDING:
                self.mode = Controls.AltitudeStates.HOLDING
                self.pitchFromAltitude.resetIntegrator()

            throttleCmd = self.throttleFromAirspeed.Update(referenceCommands.commandedAirspeed, Va)
            pitchCommand = self.pitchFromAltitude.Update(referenceCommands.commandedAltitude, altitude)

        
        elevatorCmd = self.elevatorFromPitch.Update(pitchCommand, pitch, q)
        controlSurfaceOutput.Throttle = throttleCmd
        controlSurfaceOutput.Rudder = rudderCommand
        controlSurfaceOutput.Elevator = elevatorCmd
        controlSurfaceOutput.Aileron = aileronCommand
        referenceCommands.commandedRoll = rollCommand
        referenceCommands.commandedPitch = pitchCommand

        return controlSurfaceOutput

    def getControlGains(self):

        return self.controlGain

    def getTrimInputs(self):

        return self.trimInputs

    def getVehicleAerodynamicsModel(self):

        return self.VAM

    def getVehicleControlSurfaces(self):

        return self.consurOutputs

    def getVehicleState(self):

        return self.VAM.VehicleDynamics.state

    def reset(self):

        self.VAM.reset()
        self.aileronFromRoll.resetIntegrator()
        self.rollFromCourse.resetIntegrator()
        self.rudderFromSideslip.resetIntegrator()
        self.throttleFromAirspeed.resetIntegrator()
        self.pitchFromAltitude.resetIntegrator()
        self.pitchFromAirspeed.resetIntegrator()

        return

    def setControlGains(self, controlGains=Controls.controlGains()):

        self.controlGain = controlGains
        self.aileronFromRoll.setPIDGains(self.dT, self.controlGain.kp_roll, self.controlGain.kd_roll, self.controlGain.ki_roll, self.trimInputs.Aileron, VPC.minControls.Aileron, VPC.maxControls.Aileron)
        self.rollFromCourse.setPIGains(self.dT, self.controlGain.kp_course, self.controlGain.ki_course, 0.0, -math.radians(VPC.bankAngleLimit), math.radians(VPC.bankAngleLimit))
        self.rudderFromSideslip.setPIGains(self.dT, self.controlGain.kp_sideslip, self.controlGain.ki_sideslip, self.trimInputs.Rudder, VPC.minControls.Rudder, VPC.maxControls.Rudder)
        self.elevatorFromPitch.setPDGains(self.controlGain.kp_pitch, self.controlGain.kd_pitch, self.trimInputs.Elevator, VPC.minControls.Elevator, VPC.maxControls.Elevator)
        self.throttleFromAirspeed.setPIGains(self.dT, self.controlGain.kp_SpeedfromThrottle, self.controlGain.ki_SpeedfromThrottle, self.trimInputs.Throttle, VPC.minControls.Throttle, VPC.maxControls.Throttle)
        self.pitchFromAltitude.setPIGains(self.dT, self.controlGain.kp_altitude, self.controlGain.ki_altitude, 0.0, -math.radians(VPC.pitchAngleLimit), math.radians(VPC.pitchAngleLimit))
        self.pitchFromAirspeed.setPIGains(self.dT, self.controlGain.kp_SpeedfromElevator, self.controlGain.ki_SpeedfromElevator, 0.0, -math.radians(VPC.pitchAngleLimit), math.radians(VPC.pitchAngleLimit))

        return

    def setTrimInputs(self, trimInputs=Inputs.controlInputs(Throttle=0.5, Aileron=0.0, Elevator=0.0, Rudder=0.0)):

        self.trimInputs = trimInputs

        return

    def setVehicleState(self,state):
       
        self.VAM.VehicleDynamics.state = state

        return