#############################################
#   Created by Jacob Sickafoose - jsickafo  #
#############################################

import math
import sys
import ece163.Containers.Inputs as Inputs
import ece163.Containers.Controls as Controls
import ece163.Constants.VehiclePhysicalConstants as VPC
import ece163.Modeling.VehicleAerodynamicsModel as VAM

class PDControl:
    '''
    Functions which implement the PD control with saturation where the derivative
    is available as a separate input to the function.
    The output is: u = u_ref + Kp * error - Kd * dot{error} limited between
    lowLimit and highLimit.

    Parameters: kp – proportional gain
                kd – derivative gain
                trim – trim output (added the the loop computed output)
                lowLimit – lower limit to saturate control
                highLimit – upper limit to saturate control

    Returns:    None
    '''
    def __init__(self, kp=0.0, kd=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.kp = kp
        self.kd = kd
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit



    '''
    Function to set the gains for the PD control block (including the trim
    output and the limits)

    Parameters: kp – proportional gain
                kd – derivative gain
                trim – trim output (added the the loop computed output)
                lowLimit – lower limit to saturate control
                highLimit – upper limit to saturate control

    Returns:    None
    '''
    def setPDGains(self, kp=0.0, kd=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.kp = kp
        self.kd = kd
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit



    '''
    Calculates the output of the PD loop given the gains and limits from
    instantiation, and using the command, actual, and derivative inputs.
    Output is limited to between lowLimit and highLimit from instantiation.

    Parameters: command – reference command
                current – actual output (or sensor)
                derivative – derivative of the output or sensor

    Returns:    u [control] limited to saturation bounds
    '''
    def Update(self, command=0.0, current=0.0, derivative=0.0):
        error = command - current

        u = self.kp*error - derivative*self.kd + self.trim

        if u > self.highLimit:
            u = self.highLimit
        elif u < self.lowLimit:
            u = self.lowLimit

        self.prevError = error
        return u



class PIControl:
    '''
    Functions which implement the PI control with saturation where the
    integrator has both a reset and an anti-windup such that when output
    saturates, the integration is undone and the output forced the
    output to the limit. The output is: u = u_ref + Kp * error + Ki * integral{error}
    limited between lowLimit and highLimit.

    Parameters: dT – time step [s], required for integration
                kp – proportional gain
                ki – integral gain
                trim – trim input
                lowLimit – low saturation limit
                highLimit – high saturation limit

    Returns:    None
    '''
    def __init__(self, dT=VPC.dT, kp=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.dT = dT
        self.kp = kp
        self.ki = ki
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit

        self.accumulator = 0
        self.prevError = 0



    '''
    Function to set the gains for the PI control block (including
    the trim output and the limits)

    Parameters: dT – time step [s], required for integration
                kp – proportional gain
                ki – integral gain
                trim – trim input
                lowLimit – low saturation limit
                highLimit – high saturation limit

    Returns:    None
    '''
    def setPIGains(self, dT=VPC.dT, kp=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.dT = dT
        self.kp = kp
        self.ki = ki
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit

        self.accumulator = 0
        self.prevError = 0



    '''
    Calculates the output of the PI loop given the gains and limits
    from instantiation, and using the command and current or actual
    inputs. Output is limited to between lowLimit and highLimit from
    instantiation. Integration for the integral state is done using
    trapezoidal integration, and anti-windup is implemented such
    that if the output is out of limits, the integral state is not
    updated (no additional error accumulation).

    Parameters: command – reference command
                current – actual output (or sensor)

    Returns:    u [output] limited to saturation bounds
    '''
    def Update(self, command=0.0, current=0.0):
        error = command - current

        prevAccumulator = self.accumulator
        self.accumulator += self.dT*((error+self.prevError)/2)
        u = self.kp*error + self.accumulator*self.ki + self.trim

        if u > self.highLimit:
            u = self.highLimit
            self.accumulator = prevAccumulator
        elif u < self.lowLimit:
            u = self.lowLimit
            self.accumulator = prevAccumulator
        
        self.prevError = error
        return u



    '''
    Function to reset the integration state to zero, used when
    switching modes or otherwise resetting the integral state.

    Parameters: None

    Returns:    None
    '''
    def resetIntegrator(self):
        self.accumulator = 0
        self.prevError = 0



class PIDControl:
    '''
    Functions which implement the PID control with saturation where
    the integrator has both a reset and an anti-windup such that
    when output saturates, the integration is undone and the output
    forced the output to the limit. Function assumes that physical
    derivative is available (e.g.: roll and p), not a numerically
    derived one.
    The output is: u = u_ref + Kp * error - Kd * dot{error} + Ki * integral{error}
    limited between lowLimit and highLimit

    Parameters: dT – time step [s], required for integration
                kp – proportional gain
                kd – derivative gain
                ki – integral gain
                trim – trim input
                lowLimit – low saturation limit
                highLimit – high saturation limit

    Returns:    None
    '''
    def __init__(self, dT=VPC.dT, kp=0.0, kd=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.dT = dT
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit

        self.accumulator = 0
        self.prevError = 0



    '''
    Function to set the gains for the PID control block
    (including the trim output and the limits)

    Parameters: dT – time step [s], required for integration
                kp – proportional gain
                kd – derivative gain
                ki – integral gain
                trim – trim input
                lowLimit – low saturation limit
                highLimit – high saturation limit

    Returns:    None
    '''
    def setPIDGains(self, dT=VPC.dT, kp=0.0, kd=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.dT = dT
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit

        self.accumulator = 0
        self.prevError = 0



    '''
    Calculates the output of the PID loop given the gains and limits
    from instantiation, and using the command and current or actual
    inputs. Output is limited to between lowLimit and highLimit from
    instantiation. Integration for the integral state is done using
    trapezoidal integration, and anti-windup is implemented such that
    if the output is out of limits, the integral state is not updated
    (no additional error accumulation).
    u = u_ref + Kp * error - Kd * dot{error} + Ki * integral{error}

    Parameters: command – reference command
                current – current output or sensor
                derivative – derivative of the output or sensor

    Returns:    u [output] limited to saturation bounds
    '''
    def Update(self, command=0.0, current=0.0, derivative=0.0):
        error = command - current

        prevAccumulator = self.accumulator
        self.accumulator += self.dT*((error+self.prevError)/2)
        u = self.kp*error + self.accumulator*self.ki - derivative*self.kd + self.trim

        if u > self.highLimit:
            u = self.highLimit
            self.accumulator = prevAccumulator
        elif u < self.lowLimit:
            u = self.lowLimit
            self.accumulator = prevAccumulator
        
        self.prevError = error
        return u



    '''
    Function to reset the integration state to zero, used when
    switching modes or otherwise resetting the integral state

    Parameters: None

    Returns:    None
    '''
    def resetIntegrator(self):
        self.accumulator = 0
        self.prevError = 0



class VehicleClosedLoopControl:
    '''
    Class that implements the entire closed loop control using the successive
    loop closure method of Beard Chapter 6. The class contains everything
    from control loops (PD or PI loops) along with the gains, which when
    given the reference commands will compute the control surfaces, which
    will then (along with the state) dictate the forces and moments, which
    will them compute the next state. Contains the required state for the
    altitude hold state machine from the enumeration class in Controls.AltitudeStates

    Parameters: dT – time step [s], defaults to VehiclePhysicalParameters.dT
                rudderControlSource – Either “SIDESLIP” or “YAW”. Determines whether the rudder is controlled by sideslip angle (as in Beard) or by yaw angle.

    Returns:    None
    '''
    def __init__(self, dT=0.01, rudderControlSource='SIDESLIP'):
        ## Containers
        self.VAM = VAM.VehicleAerodynamicsModel()
        self.controlGains = Controls.controlGains()
        self.trimInputs = Inputs.controlInputs()
        self.outputControls = Inputs.controlInputs()
        self.mode = Controls.AltitudeStates.HOLDING

        ## From the optional inputs
        self.dT = dT
        self.rudderControlSource = rudderControlSource

        #### PIControl Objects
        self.rollFromCourse       = PIControl()
        self.rudderFromSideslip   = PIControl()
        self.throttleFromAirspeed = PIControl()
        self.pitchFromAltitude    = PIControl()
        self.pitchFromAirspeed    = PIControl()

        #### PDControl Object
        self.elevatorFromPitch = PDControl()

        #### PIDControl Object
        self.aileronFromRoll = PIDControl()



    '''
    Resets the module to run again. Does not overwrite control gains,
    but does reset the integral states of all of the PI control loops.

    Parameters: None

    Returns:    None
    '''
    def reset(self):
        ## Containers
        self.VAM = VAM.VehicleAerodynamicsModel()
        # self.trimInputs = Inputs.controlInputs()
        # self.outputControls = Inputs.controlInputs()
        # self.mode = Controls.AltitudeStates(HOLDING)

        ## From the optional inputs
        self.dT = 0.01
        self.rudderControlSource = 'SIDESLIP'

        #### PIControl Objects
        self.rollFromCourse.resetIntegrator()
        self.rudderFromSideslip.resetIntegrator()
        self.throttleFromAirspeed.resetIntegrator()
        self.pitchFromAltitude.resetIntegrator()
        self.pitchFromAirspeed.resetIntegrator()

        #### PIDControl Object
        self.aileronFromRoll.resetIntegrator()



    '''
    Wrapper function to extract control gains from the class.

    Parameters: None

    Returns:    controlGains - class from Controls.controlGains
    '''
    def getControlGains(self):
        return self.outputControls



    '''
    Function to set all of the gains from the controlGains previously
    computed to the correct places within the various control loops
    to do the successive loop closure (see Beard Chapter 6). Control
    loop limits are taken from the VehiclePhysicalConstants file,
    trim inputs are taken from self.trimInputs.

    Parameters: controlGains – controlGains class, has the PID loop gains for each loop

    Returns:    None
    '''
    def setControlGains(self, controlGains=Controls.controlGains()):
        #### PIControl Objects
        self.rollFromCourse.setPIGains(VPC.dT, controlGains.kp_course, controlGains.ki_course, 0, math.radians(-VPC.bankAngleLimit), math.radians(VPC.bankAngleLimit))
        self.rudderFromSideslip.setPIGains(VPC.dT, controlGains.kp_sideslip, controlGains.ki_sideslip, self.trimInputs.Rudder, VPC.minControls.Rudder, VPC.maxControls.Rudder)
        self.throttleFromAirspeed.setPIGains(VPC.dT, controlGains.kp_SpeedfromThrottle, controlGains.ki_SpeedfromThrottle, self.trimInputs.Throttle, VPC.minControls.Throttle, VPC.maxControls.Throttle)
        self.pitchFromAltitude.setPIGains(VPC.dT, controlGains.kp_altitude, controlGains.ki_altitude, 0, math.radians(-VPC.pitchAngleLimit), math.radians(VPC.pitchAngleLimit))
        self.pitchFromAirspeed.setPIGains(VPC.dT, controlGains.kp_SpeedfromElevator, controlGains.ki_SpeedfromElevator, 0, math.radians(-VPC.pitchAngleLimit), math.radians(VPC.pitchAngleLimit))

        #### PDControl Objects
        self.elevatorFromPitch.setPDGains(controlGains.kp_pitch, controlGains.kd_pitch, self.trimInputs.Elevator, VPC.minControls.Elevator, VPC.maxControls.Elevator)

        #### PIDControl Objects
        self.aileronFromRoll.setPIDGains(VPC.dT, controlGains.kp_roll, controlGains.kd_roll, controlGains.ki_roll, self.trimInputs.Aileron, VPC.minControls.Aileron, VPC.maxControls.Aileron)



    '''
    Wrapper function to extract vehicle state from the class.

    Parameters: None

    Returns:    vehicleState, class from States.vehicleState
    '''
    def getVehicleState(self):
        return self.VAM.VDM.state



    '''
    Wrapper function to inject vehicle state into the class.

    Parameters: state – from States.vehicleState class

    Returns:    None
    '''
    def setVehicleState(self, state):
        self.VAM.VDM.state = state



    '''
    Wrapper function to get the trim inputs from the class.

    Parameters: None

    Returns:    trimInputs - class from Inputs.controlInputs (Throttle, Elevator, Aileron, Rudder)
    '''
    def getTrimInputs(self):
        return self.trimInputs



    '''
    Wrapper function to inject the trim inputs into the class.

    Parameters: trimInputs – from Inputs.controlInputs (Throttle, Elevator, Aileron, Rudder)

    Returns:    None
    '''
    def setTrimInputs(self, trimInputs=Inputs.controlInputs(Throttle=0.5, Aileron=0.0, Elevator=0.0, Rudder=0.0)):
        self.trimInputs = trimInputs



    '''
    Wrapper function to extract the internal VehicleAerodynamicsModel in order to
    access the various function that are associated with the Aero model (such as
    setting and getting the wind state and model)

    Parameters: None

    Returns:    VehicleAerodynamicsModel - class from VehicleAerodynamicsModel
    '''
    def getVehicleAerodynamicsModel(self):
        return self.VAM



    '''
    Wrapper function to extract control outputs
    (Throttle, Aileron, Elevator, Rudder) from the class.

    Parameters: None

    Returns:    controlInputs - class from Inputs.controlInputs
    '''
    def getVehicleControlSurfaces(self):
        return self.outputControls



    '''
    Function that implements the full closed loop controls using the commanded
    inputs of airspeed, altitude, and course (chi). Calls all of the submodules
    below it to implement the full flight dynamics under closed loop control.
    Note that the internal commandedPitch and commandedRoll of the reference
    commands are altered by this function, and this is used to track the
    reference commands by the simulator.

    You will need to add or subtract 360 degrees (2*pi) from you internal course
    (chi) when the error is outside of +/- 180 degrees (pi radians). There is
    never a course error of more than 180 degrees, so if you do see such an
    error, it is because signed angles and reciprocal headings (e.g.: -180
    and +180 are pointed in the same direction). :param referenceCommands:
    high level autopilot commands (note: altered by function)

    Parameters: state – vehicle state (either actual or estimated)

    Returns:    controlSurfaceOutputs - vehicle control inputs from class Inputs->controlInputs
    '''
    def UpdateControlCommands(self, referenceCommands, state):
        outControls = Inputs.controlInputs() # Inits the output

        #### Aileron
        ## Keeps state.chi within +- 2pi
        if (referenceCommands.commandedCourse - state.chi) >= math.pi:
            state.chi += (2*math.pi)
        elif (referenceCommands.commandedCourse - state.chi) <= -math.pi:
            state.chi -= (2*math.pi)

        referenceCommands.commandedRoll =  self.rollFromCourse.Update(referenceCommands.commandedCourse, state.chi)
        outControls.Aileron = self.aileronFromRoll.Update(referenceCommands.commandedRoll, state.roll, state.p)

        #### Rudder
        outControls.Rudder = self.rudderFromSideslip.Update(0, state.beta)


        #### Elevator and Throttle
        upper_thresh = referenceCommands.commandedAltitude + VPC.altitudeHoldZone
        lower_thresh = referenceCommands.commandedAltitude - VPC.altitudeHoldZone
        ## Implements state machine
        if self.mode == Controls.AltitudeStates.HOLDING:
            referenceCommands.commandedPitch = self.pitchFromAltitude.Update(referenceCommands.commandedAltitude, (-state.pd))    # Pitch determined by altitude
            outControls.Throttle = self.throttleFromAirspeed.Update(referenceCommands.commandedAirspeed, state.Va)              # Throttle determined by airspeed
            # Determines if a change of state is necessary
            if -state.pd > upper_thresh:
                self.pitchFromAirspeed.resetIntegrator()
                self.mode = Controls.AltitudeStates.DESCENDING
            elif -state.pd < lower_thresh:
                self.pitchFromAirspeed.resetIntegrator()
                self.mode = Controls.AltitudeStates.CLIMBING

        if self.mode == Controls.AltitudeStates.DESCENDING:
            referenceCommands.commandedPitch = self.pitchFromAirspeed.Update(referenceCommands.commandedAirspeed, state.Va)      # Pitch determined by airspeed
            outControls.Throttle = VPC.minControls.Throttle
            # Determines if a change of state is necessary
            if lower_thresh < -state.pd and -state.pd < upper_thresh:
                self.pitchFromAltitude.resetIntegrator()
                self.mode = Controls.AltitudeStates.HOLDING

        if self.mode == Controls.AltitudeStates.CLIMBING:
            referenceCommands.commandedPitch = self.pitchFromAirspeed.Update(referenceCommands.commandedAirspeed, state.Va)      # Pitch determined by airspeed
            outControls.Throttle = VPC.maxControls.Throttle
            # Determines if a change of state is necessary
            if lower_thresh < -state.pd and -state.pd < upper_thresh:
                self.pitchFromAltitude.resetIntegrator()
                self.mode = Controls.AltitudeStates.HOLDING

        # Plugs in final commandedPitch for elevator controls
        outControls.Elevator = self.elevatorFromPitch.Update(referenceCommands.commandedPitch, state.pitch, state.q)


        ## Finally, returns the output controls
        return outControls



    '''
    Function that wraps the UpdateControlCommands and feeds it the correct state
    (estimated or otherwise). Updates the vehicle state internally using the
    vehicleAerodynamics.Update command

    Parameters: None

    Returns:    None
    '''
    def Update(self, referenceCommands=Controls.referenceCommands):
        # Pass the input referenceCommands and the current vehicle state into UpdateControlCommands()
        newControls = self.UpdateControlCommands(referenceCommands, self.VAM.VDM.state)
        # Pass the yielded control outputs to VehicleAerodynamicsModel.Update()
        self.VAM.Update(newControls)