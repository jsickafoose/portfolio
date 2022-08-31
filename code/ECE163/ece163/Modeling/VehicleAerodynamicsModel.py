#############################################
#   Created by Jacob Sickafoose - jsickafo  #
#############################################

import math
from ..Containers import States
from ..Containers import Inputs
from ..Modeling import VehicleDynamicsModel
from ..Modeling import WindModel
from ..Utilities import MatrixMath as mm
from ..Utilities import Rotations
from ..Constants import VehiclePhysicalConstants as VPC

class VehicleAerodynamicsModel:
    '''
    Initialization of the internal classes which are used to track the vehicle
    aerodynamics and dynamics.

    Parameters: initialSpeed - defaults to VPC.InitialSpeed
                initialHeight - defaults to VPC.InitialDownPosition

    Returns:    None
    '''
    def __init__(self, initialSpeed = 25.0, initialHeight = -100.0, Wind=VPC.DrydenNoWind):
        ## Sets variables  to the ones in the header
        self.initialSpeed = initialSpeed
        self.initialHeight = initialHeight

        ## Creates a new VehicleDynamicsModel object internally
        self.VDM = VehicleDynamicsModel.VehicleDynamicsModel()
        
        ## Initializes the object to some values listed in VPC
        self.VDM.state.pn = VPC.InitialNorthPosition
        self.VDM.state.pe = VPC.InitialEastPosition
        self.VDM.state.pd = VPC.InitialDownPosition
        self.VDM.state.u = initialSpeed

        self.Wind = WindModel.WindModel(0.01, 25.0, Wind)


    '''
    Resets module to its original state so it can run again

    Returns:    None
    '''
    def reset(self):
        self.initialSpeed = VPC.InitialSpeed()
        self.initialHeight = VPC.InitialDownPosition()

        self.VDM.reset()
        self.VDM.state.pn = VPC.InitialNorthPosition
        self.VDM.state.pe = VPC.InitialEastPosition
        self.VDM.state.pd = VPC.InitialDownPosition
        self.VDM.state.u  = VPC.initialSpeed

        self.Wind.reset()


    '''
    Wrapper function to set the vehicle state from outside module

    Parameters: state – class of vehicleState

    Returns:    None
    '''
    def setVehicleState(self, state):
        self.VDM.state = state


    '''
    Wrapper function to return vehicle state form module

    Returns:    vehicle state class
    '''
    def getVehicleState(self):
        return self.VDM.state


    '''
    Wrapper function to return the vehicle dynamics model handle

    Returns:    vehicleDynamicsModel, from VehicleDynamicsModel class
    '''
    def getVehicleDynamicsModel(self):
        return self.VDM


    '''
    Wrapper function to set the windModel

    Parameters: windModel – from windModel class

    Returns:    None
    '''
    def setWindModel(self, windModel):
        self.Wind = windModel


    '''
    Wrapper function to return the windModel

    Returns:    windModel, from windModel class
    '''
    def getWindModel(self):
        return self.Wind


    '''
    Function that uses the current state (internal), wind (internal), and controls (inputs) to
    calculate the forces, and then do the integration of the full 6-DOF non-linear equations
    of motion. Wraps the VehicleDynamicsModel class as well as the windState internally.
    The Wind and the vehicleState are maintained internally.

    Parameters: controls – controlInputs class (Throttle, Elevator, Aileron, Rudder)

    Returns:    None, state is updated internally
    '''   
    def Update(self, controls):
        self.Wind.Update()
        forces = self.updateForces(self.VDM.state, controls, self.Wind.getWind()) # Runs the internal updateForces function
        self.VDM.Update(forces)                              # Uses forces to update VehicleDynamicsModel



################################################
#          START OF PRIVATE FUNCTIONS          #
################################################


    '''
    Function to project gravity forces into the body frame. Uses the gravity constant
    g0 from physical constants and the vehicle mass. Fg = m * R * [0 0 g0]. It then
    stores the resulting vector in the linear parts of a Containers.Inputs.forcesMoments
    object.

    Parameters: state – current vehicle state (need the rotation matrix)

    Returns:    gravity forces, forcesMoments class
    '''
    def gravityForces(self, state):
        ## Rotates the gravity acceleration matrix
        firstVal = [state.R[0][0]*0+state.R[0][1]*0+state.R[0][2]*VPC.g0, # I had to keep manually
                    state.R[1][0]*0+state.R[1][1]*0+state.R[1][2]*VPC.g0, # multiplying because the
                    state.R[2][0]*0+state.R[2][1]*0+state.R[2][2]*VPC.g0] # matrixMultiply() func doesnt work
        forces   = [VPC.mass*firstVal[0], VPC.mass*firstVal[1], VPC.mass*firstVal[2]] # This does F = m*a
        
        ## Creates forcesMoments object and sets it properly for returning
        out = Inputs.forcesMoments()
        out.Fx = forces[0]
        out.Fy = forces[1]
        out.Fz = forces[2]

        return out


    '''
    Function to calculate the Coefficient of Lift and Drag as a function of angle of attack.
    Angle of attack (alpha) in [rad] is contained within the state.alpha and updated within
    the CalculateAirspeed function. For the coefficient of drag, we are using the parabolic
    form: CD = CDp + (CLalpha)^2/(pi*AR*e)

    Parameters: alpha - Angle of Attack [rad]

    Returns:    Coefficient of Lift, CL_alpha (unitless), Coefficient of Drag,
                CD_alpha (unitless), Coefficoent of Moment, CM_alpha (unitless)
    '''
    def CalculateCoeff_alpha(self, alpha):
        ## Fat equation to find sigma value
        sigma = (1 + math.exp(-VPC.M*(alpha - VPC.alpha0)) + math.exp(VPC.M*(alpha + VPC.alpha0)))\
        / ((1 + math.exp(-VPC.M*(alpha - VPC.alpha0)))*(1 + math.exp(VPC.M*(alpha + VPC.alpha0))))

        ## Finds CL and CD laminar
        CL_Laminar = VPC.CL0 + (VPC.CLalpha*alpha)
        CD_Laminar = VPC.CDp + ((CL_Laminar**2)/(math.pi * VPC.e * VPC.AR))

        ## Finds CL and CD turbulent
        CL_Turbulent = 2 * math.sin(alpha) * math.cos(alpha)
        CD_Turbulent = 2 * math.sin(alpha) * math.sin(alpha)

        ## Finds the final constants for output
        C_L = ((1 - sigma)*CL_Laminar) + (sigma*CL_Turbulent)
        C_D = ((1 - sigma)*CD_Laminar) + (sigma*CD_Turbulent)
        C_M = VPC.CM0 + (VPC.CMalpha*alpha)

        return C_L, C_D, C_M


    '''
    Function to calculate the Aerodynamic Forces and Moments using the
    linearized simplified force model and the stability derivatives
    in VehiclePhysicalConstants.py file. Specifically does not include
    forces due to control surface deflection. Requires airspeed (Va)
    in [m/s], angle of attack (alpha) in [rad] and sideslip angle (beta)
    in [rad] from the state.
        Uses Beard 4.6, 4.7, 4.14, 4.15, and 4.16 equatiions

    Parameters: state – current vehicle state (need the velocities)

    Returns:    Aerodynamic forces, forcesMoments class
    '''
    def aeroForces(self, state):
        ## Stops the 0 case in it's tracks by returning a default, 0'd value forceMoment object
        if state.Va == 0:
            return Inputs.forcesMoments()

        a = state.alpha    # Extracts alpha at the start, just to make everything cleaner
        C_L, C_D, C_M = self.CalculateCoeff_alpha(a)    # Extracts the constants
        
        CX  = -C_D*math.cos(a) + C_L*math.sin(a)
        CXq = -VPC.CDq*math.cos(a) + VPC.CLq*math.sin(a)

        CZ  = -C_D*math.sin(a) - C_L*math.cos(a)
        CZq = -VPC.CDq*math.sin(a) - VPC.CLq*math.cos(a)

        ## First part is just the first part of all the equations. I find it separately for optimization
        # I figured the fastest way to find it was divide the whole number by 2 after, rather than multiply by 0.5 like I did originally
        firstPart = (VPC.rho*(state.Va**2)*VPC.S)/2
        VaX2      = 2*state.Va

        ## Finally computes all the Forces and Moments right into the object
        out = Inputs.forcesMoments()
        out.Fx = firstPart * (CX + CXq*(VPC.c/VaX2)*state.q)
        out.Fy = firstPart * (VPC.CY0 + VPC.CYbeta*state.beta + VPC.CYp*(VPC.b/VaX2)*state.p + VPC.CYr*(VPC.b/VaX2)*state.r)
        out.Fz = firstPart * (CZ + CZq*(VPC.c/VaX2)*state.q)

        out.Mx = firstPart * (VPC.b*(VPC.Cl0 + (VPC.Clbeta*state.beta) + (VPC.Clp*(VPC.b/VaX2)*state.p) + (VPC.Clr*(VPC.b/VaX2)*state.r)))
        out.My = firstPart * (VPC.c*(VPC.CM0 + (VPC.CMalpha*state.alpha) + (VPC.CMq*(VPC.c/VaX2)*state.q)))
        out.Mz = firstPart * (VPC.b*(VPC.Cn0 + (VPC.Cnbeta*state.beta) + (VPC.Cnp*(VPC.b/VaX2)*state.p) + (VPC.Cnr*(VPC.b/VaX2)*state.r)))

        return out


    '''
    Function to calculate the propeller forces and torques on the aircraft. Uses the fancy
    propeller model that parameterizes the torque and thrust coefficients of the propeller
    using the advance ratio. See ECE163_PropellerCheatSheet.pdf for details.

    Parameters: Va – the vehicle airspeed [m/s]
                Throttle – Throttle input [0-1]

    Returns:    Fx_prop [N], Mx_prop [N-m]
    '''    
    def CalculatePropForces(self, Va, Throttle):
        ## Starts out by finding all the pieces
        K = 60 / (2*math.pi*VPC.KV)
        Vin = VPC.V_max * Throttle
        a = (VPC.rho*(VPC.D_prop**5)*VPC.C_Q0) / (4*(math.pi**2))
        b = (VPC.rho*(VPC.D_prop**4)*Va*VPC.C_Q1) / (2*math.pi) + (K**2) / (VPC.R_motor)
        c = (VPC.rho*(VPC.D_prop**3)*(Va**2)*VPC.C_Q2) - (K*(Vin/VPC.R_motor)) + (K*VPC.i0)

        try:
            Omega = (-b + math.sqrt((b**2) - (4*a*c)))/(2*a)
        except:
            Omega = 100
        
        J = (2*math.pi*Va)/(Omega*VPC.D_prop)
        CT = VPC.C_T0 + VPC.C_T1*J + VPC.C_T2*(J**2)
        CQ = VPC.C_Q0 + VPC.C_Q1*J + VPC.C_Q2*(J**2)

        ## Finally finds t he propeller force, and moment
        Fx_prop =  (VPC.rho*(Omega**2)*(VPC.D_prop**4)*CT) / (4*(math.pi**2))
        Mx_prop = -(VPC.rho*(Omega**2)*(VPC.D_prop**5)*CQ) / (4*(math.pi**2))

        return Fx_prop, Mx_prop


    '''
    Function to calculate aerodynamic forces from control surface deflections
    (including throttle) using the linearized aerodynamics and simplified
    thrust model. Requires airspeed (Va) in [m/s] and angle of attack (alpha)
    in [rad] both from state.Va and state.alpha respectively.

    Parameters: state – current vehicle state (need the velocities)
                controls – inputs to aircraft - controlInputs()

    Returns:    Aerodynamic forces, forcesMoments class
    '''
    def controlForces(self, state, controls):
        ## Starts by finding the beginning pieces
        a = state.alpha
        Va = state.Va
        
        CXde = -VPC.CDdeltaE*math.cos(a) + VPC.CLdeltaE*math.sin(a)
        CZde = -VPC.CDdeltaE*math.sin(a) - VPC.CLdeltaE*math.cos(a)

        ## Using the same firstPart as with aeroForces
        firstPart = (VPC.rho*(Va**2)*VPC.S)/2

        Fx_prop, Mx_prop = self.CalculatePropForces(Va, controls.Throttle)

        out = Inputs.forcesMoments()
        out.Fx = firstPart * (CXde*controls.Elevator) + Fx_prop
        out.Fy = firstPart * (VPC.CYdeltaA*controls.Aileron + VPC.CYdeltaR*controls.Rudder)
        out.Fz = firstPart * (CZde*controls.Elevator)

        out.Mx = firstPart * VPC.b *((VPC.CldeltaA*controls.Aileron) + (VPC.CldeltaR*controls.Rudder)) + Mx_prop
        out.My = firstPart * VPC.c * (VPC.CMdeltaE*controls.Elevator)
        out.Mz = firstPart * VPC.b * ((VPC.CndeltaA*controls.Aileron) + (VPC.CndeltaR*controls.Rudder))

        return out


    '''
    Function to update all of the aerodynamic, propulsive, and gravity forces and
    moments. All calculations required to update the forces are included. state
    is updated with new values for airspeed, angle of attack, and sideslip angles
    (see class definition for members)

    Parameters: state – current vehicle state
                controls – current vehicle control surface deflections
                wind – current environmental wind. If not specified, defaults to 0 windspeed

    Returns:    total forces, forcesMoments class
    '''
    def updateForces(self, state, controls, wind=None):
        ## First need to calculate Va, alpha, and beta
        # This code was just copied from state
        if wind == None:
            state.Va = math.hypot(state.u, state.v, state.w)
            state.alpha = math.atan2(state.w, state.u)
            if math.isclose(state.Va, 0.0):
                state.beta = 0.0
            else:
                state.beta = math.asin(state.v/state.Va)
        else:
            state.Va, state.alpha, state.beta = self.CalculateAirspeed(state, wind)

        ## Creates forceMoment objects for each type of force
        gForces = self.gravityForces(state)
        aForces = self.aeroForces(state)
        cForces = self.controlForces(state, controls)
        
        ## Creates the output, then adds them all together
        out = Inputs.forcesMoments()
        out.Fx = gForces.Fx + aForces.Fx + cForces.Fx
        out.Fy = gForces.Fy + aForces.Fy + cForces.Fy
        out.Fz = gForces.Fz + aForces.Fz + cForces.Fz

        out.Mx = gForces.Mx + aForces.Mx + cForces.Mx
        out.My = gForces.My + aForces.My + cForces.My
        out.Mz = gForces.Mz + aForces.Mz + cForces.Mz

        return out


    '''
    Calculates the total airspeed, as well as angle of attack and side-slip angles from
    the wind and current state. Needed for further aerodynamic force calculations. Va,
    wind speed [m/s], alpha, angle of attack [rad], and beta, side-slip angle [rad]
    are returned from the function. The state must be updated outside this function.

    Parameters: state - current vehicle state (need the velocities)
                wind - current wind state (global and gust)

    Returns:    Va, wind speed [m/s], alpha, angle of attack [rad], and beta,
                side-slip angle [rad]
    '''
    def CalculateAirspeed(self, state, wind):
        Ws = math.hypot(wind.Wn, wind.We, wind.Wd)
        Xw = math.atan2(wind.We, wind.Wn)
        if math.isclose(Ws, 0.0):
            Yw = 0
        else:
            Yw = -math.asin(wind.Wd / Ws)

        Rwind  = Rotations.euler2DCM(Xw, Yw, 0) ##### Third variable is 0
        wind_i = mm.add((mm.multiply(mm.transpose(Rwind), [[wind.Wu], [wind.Wv], [wind.Ww]])), [[wind.Wn], [wind.We], [wind.Wd]])
        Vr = mm.subtract([[state.u], [state.v], [state.w]], mm.multiply(state.R, wind_i))
        
        # Calculates Va, alpha, and beta using the Va matrix
        Va = math.hypot(Vr[0][0], Vr[1][0], Vr[2][0])
        alpha = math.atan2(Vr[2][0], Vr[0][0])
        if math.isclose(Va, 0.0):
            beta = 0.0
        else:
            beta = math.asin(Vr[1][0]/Va)

        return Va, alpha, beta