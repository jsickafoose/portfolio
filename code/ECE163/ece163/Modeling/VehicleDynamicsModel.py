#############################################
#   Created by Jacob Sickafoose - jsickafo  #
#############################################

import math
from ..Containers import States
from ..Utilities import MatrixMath as mm
from ..Utilities import Rotations
from ..Constants import VehiclePhysicalConstants as VPC
"""
state – the current state of the vehicle, as an instance of States.vehicleState
dot – the current time-derivative of the state, as an instance of States.vehicleState
dT – the timestep that this object uses when Update()ing.
"""
class VehicleDynamicsModel:
    """
    Initializes the class, and sets the time step (needed for Rexp and integration).
    Instantiates attributes for vehicle state, and time derivative of vehicle state.

    Parameters: dT - defaults to VPC.dT
    
    Returns: None
    """
    def __init__(self, dT = 0.01):
        self.dT = dT

        self.state = States.vehicleState()
        self.dot = States.vehicleState()


    """
    Reset the Vehicle state to initial conditions

    Returns: None
    """
    def reset(self):
        ## Someone on the internet said it was best practice to set each variable back to the defaults manually
        self.dT = 0.01

        self.state = States.vehicleState()
        self.dot = States.vehicleState()
        # self.state.pn = 0.0
        # self.state.pe = 0.0
        # self.state.pd = 0.0
        # self.state.u = 0.0
        # self.state.v = 0.0
        # self.state.w = 0.0
        # self.state.yaw = 0.0
        # self.state.pitch = 0.0
        # self.state.roll = 0.0
        # self.state.p = 0.0
        # self.state.q = 0.0
        # self.state.r = 0.0
        # self.state.dcm = None

        # self.dot.pn = 0.0
        # self.dot.pe = 0.0
        # self.dot.pd = 0.0
        # self.dot.u = 0.0
        # self.dot.v = 0.0
        # self.dot.w = 0.0
        # self.dot.yaw = 0.0
        # self.dot.pitch = 0.0
        # self.dot.roll = 0.0
        # self.dot.p = 0.0
        # self.dot.q = 0.0
        # self.dot.r = 0.0
        # self.dot.dcm = None



    """
    Setter method to write the vehicle state

    Parameters: state – state to be set ( an instance of Containers.States.vehicleState)
    
    Returns: None
    """
    def setVehicleState(self, state):
        self.state = state


    """
    Getter method to read the vehicle state

    Returns: state (from class vehicleState)
    """    
    def getVehicleState(self):
        return self.state


    """
    Setter method to write the vehicle state time derivative

    Parameters: state – dot to be set (should be an instance of Containers.States.vehicleState)
    
    Returns: None
    """
    def setVehicleDerivative(self, dot):
        self.dot = dot


    """
    Getter method to read the vehicle state time derivative

    Returns: dot  ( an instance of Containers.States.vehicleState)
    """
    def getVehicleDerivative(self):
        return self.dot


    """
    Function that implements the integration such that the state is updated using the
    forces and moments passed in as the arguments (dT is internal from the member).
    State is updated in place (self.state is updated). Use getVehicleState to retrieve state.
    Time step is defined in VehiclePhyscialConstants.py

    Parameters: forcesMoments – forces [N] and moments [N-m] defined in forcesMoments class
    
    Returns: None
    """
    def Update(self, forcesMoments):
        self.dot = self.derivative(self.state, forcesMoments)
        self.state = self.IntegrateState(self.dT, self.state, self.dot)


################################################
#               PRIVATE FUNCTIONS              #
################################################

    """
    Function to compute the time-derivative of the state given body frame forces and moments

    Parameters: state – state to differentiate, as a States.vehicleState object
                forcesMoments – forces [N] and moments [N-m] as an Inputs.forcesMoments object
    
    Returns: The current time derivative, in the form of a States.vehicleState.object
    """
    def derivative(self, state, forcesMoments):
        currDer = States.vehicleState() # New vehicle state to return

        ## Finds the derivative of Pn, Pe, and Pd
        rT = mm.transpose(state.R)
        nedDer = [rT[0][0]*state.u+rT[0][1]*state.v+rT[0][2]*state.w, # I had to keep manually
                  rT[1][0]*state.u+rT[1][1]*state.v+rT[1][2]*state.w, # multiplying because the
                  rT[2][0]*state.u+rT[2][1]*state.v+rT[2][2]*state.w] # mm.multiply() wouldn't work on floats

        ## Finds the derivative of u, v, and w
        forces = [(1/VPC.mass) * forcesMoments.Fx,
                  (1/VPC.mass) * forcesMoments.Fy,
                  (1/VPC.mass) * forcesMoments.Fz]
        uvwDer = [(state.r*state.v) - (state.q*state.w),
                  (state.p*state.w) - (state.r*state.u),
                  (state.q*state.u) - (state.p*state.v)]
        uvwDer = [forces[0]+uvwDer[0],
                  forces[1]+uvwDer[1],
                  forces[2]+uvwDer[2]]

        ## Finds the derivative of yaw, pitch, and roll
        yprT = [[1, math.sin(state.roll)*math.tan(state.pitch), math.cos(state.roll)*math.tan(state.pitch)],
                [0, math.cos(state.roll), -math.sin(state.roll)],
                [0, (math.sin(state.roll)/math.cos(state.pitch)), (math.cos(state.roll)/math.cos(state.pitch))]]
        yprDer = [yprT[0][0]*state.p+yprT[0][1]*state.q+yprT[0][2]*state.r,
                  yprT[1][0]*state.p+yprT[1][1]*state.q+yprT[1][2]*state.r,
                  yprT[2][0]*state.p+yprT[2][1]*state.q+yprT[2][2]*state.r]

        ## Finds derivatives of p, q, and r
        gamma = VPC.Jdet        # Establishes all the gammas
        gamma1 = VPC.Gamma1
        gamma2 = VPC.Gamma2
        gamma3 = VPC.Jzz / gamma
        gamma4 = VPC.Jxz / gamma
        gamma5 = (VPC.Jzz - VPC.Jxx) / VPC.Jyy
        gamma6 = VPC.Jxz / VPC.Jyy
        gamma7 = VPC.Gamma7
        gamma8 = VPC.Jxx / gamma

        matrix1 = [gamma1*state.p*state.q - gamma2*state.q*state.r,                     # Does the math for both matrices
                 gamma5*state.p*state.r - gamma6*(state.p**2 - state.r**2),
                 gamma7*state.p*state.q - gamma1*state.q*state.r]

        matrix2 = [gamma3*forcesMoments.Mx + gamma4*forcesMoments.Mz,
                   1/VPC.Jyy * forcesMoments.My,
                   gamma4*forcesMoments.Mx + gamma8*forcesMoments.Mz]

        rDer = [matrix1[0]+matrix2[0], matrix1[1]+matrix2[1], matrix1[2]+matrix2[2]]    # Adds both matrices together

        ## Sets all variables of currDer
        currDer.pn    = nedDer[0]
        currDer.pe    = nedDer[1]
        currDer.pd    = nedDer[2]
        currDer.u     = uvwDer[0]
        currDer.v     = uvwDer[1]
        currDer.w     = uvwDer[2]
        currDer.yaw   = yprDer[0]
        currDer.pitch = yprDer[1]
        currDer.roll  = yprDer[2]
        currDer.p     = rDer[0]
        currDer.q     = rDer[1]
        currDer.r     = rDer[2]
        return currDer


    """
    Function to do the simple forwards integration of the state using the derivative
    function. State is integrated using the update formula X_{k+1} = X_{k} + dX/dt * dT.
    The updated state is returned by the function. The state is held internally as an
    attribute of the class.

    Parameters: dT – the timestep over which to forward integrate
                state – the initial state to integrate, as an instance of State.vehicleState
                dot – the time-derivative of the state for performing integration, as an instance of State.vehicleState

    Returns:    new state, advanced by a timestep of dT (defined in States.vehicleState class)
    """
    def ForwardEuler(self, dT, state, dot):
        forward = States.vehicleState()

        # Implements the given equation, line by line
        forward.pn    = state.pn + (dT*dot.pn)
        forward.pe    = state.pe + (dT*dot.pe)
        forward.pd    = state.pd + (dT*dot.pd)
        forward.u     = state.u + (dT*dot.u)
        forward.v     = state.v + (dT*dot.v)
        forward.w     = state.w + (dT*dot.w)
        forward.p     = state.p + (dT*dot.p)
        forward.q     = state.q + (dT*dot.q)
        forward.r     = state.r + (dT*dot.r)
        return forward


    """
    Calculates the matrix exponential exp(-dT*[omega x]), which can be used in the
    closed form solution for the DCM integration from body-fixed rates.

    See the document (ECE163_AttitudeCheatSheet.pdf) for details.

    Parameters: dT – time step [sec]
                state – the vehicle state, in the form of a States.vehicleState object
                dot – the state derivative, in the form of a States.vehicleState object
    
    Returns: Rexp: the matrix exponential to update the state                
    """
    def Rexp(self, dT, state, dot):
        ## Finds the half time step between
        p = state.p + ((dT/2)*dot.p)
        q = state.q + ((dT/2)*dot.q)
        r = state.r + ((dT/2)*dot.r)

        ## Sets up the variables I, wMagnitude, wX, and wX^2 we will need for later
        I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        wMagnitude = math.hypot(p, q, r)
        wX = [[0, -r, q],
              [r, 0, -p],
              [-q, p, 0]]
        wXSquared = mm.multiply(wX, wX)

        ## Implements the given equations depending on MacLauren
        if wMagnitude <= 0.2: # Checks if it's close to zero, approximates by MacLauren series
            SinSide = dT - (dT**3 * wMagnitude**2)/6 + (dT**5 * wMagnitude**4)/120
            CosSide = (dT**2/2) - (dT**4 * wMagnitude**2)/24 + (dT**6 * wMagnitude**4)/720
        else:
            SinSide = (math.sin(wMagnitude * dT))/wMagnitude
            CosSide = (1 - math.cos(wMagnitude * dT))/wMagnitude**2

        SinSide = mm.scalarMultiply(SinSide, wX)
        CosSide = mm.scalarMultiply(CosSide, wXSquared)

        Rexp = mm.add(mm.subtract(I, SinSide), CosSide)
        return Rexp

    """
    Updates the state given the derivative, and a time step. Attitude propagation is
    implemented as a DCM matrix exponential solution, all other state params are
    advanced via forward euler integration [x]k+1 = [x]k + xdot*dT. The integrated state 
    is returned from the function. All derived variables in the state (e.g.: Va, alpha, beta, chi)
    should be copied from the input state to the returned state.

    Parameters: dT – Time step [s]
                state – the initial state to integrate, as an instance of State.vehicleState
                dot – the time-derivative of the state for performing integration, as an instance of State.vehicleState
    
    Returns:    new state, advanced by a timestep of dT, returned as an instance of the States.vehicleState class
    """
    def IntegrateState(self, dT, state, dot):
        # 2. Foward-Euler for Pn, Pe, Pd, u, v, w, p, q, and r
        newState = self.ForwardEuler(dT, state, dot)

        # 1. Matrix-exponential technique for R
        newState.R = mm.multiply(self.Rexp(dT,state, dot),  state.R)

        # 3. yaw, pitch, roll, and chi derived from the above
        ypr = Rotations.dcm2Euler(newState.R)

        newState.yaw   = ypr[0]
        newState.pitch = ypr[1]
        newState.roll  = ypr[2]

        # 4. Va, alpha, beta, and chi based on the given lines
        newState.Va = state.Va
        newState.alpha = state.alpha
        newState.beta = state.beta

        newState.chi = math.atan2(dot.pe, dot.pn)
        return newState