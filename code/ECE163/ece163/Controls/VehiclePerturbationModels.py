import math
from ece163.Modeling import VehicleAerodynamicsModel
from ece163.Constants import VehiclePhysicalConstants as VPC
from ece163.Containers import States
from ece163.Containers import Inputs
from ece163.Containers import Linearized
from ece163.Utilities import MatrixMath


'''
Function to fill the transfer function parameters used for the successive loop
closure from the given trim state and trim inputs. Note that these parameters
will be later used to generate actual control loops. Vehicle Perturbation
models are developed using the trim state and inputs. Models for transfer
function parameters and state space implementations are calculated using
constants in VehiclePhysicalParameters and the input trim state and trim
control inputs. Results are returned as a Linearized.transferFunction class.

Parameters: trimState – vehicle trim state, as calculated in VehicleTrim code
            trimInputs – vehicle trim inputs, as calculated in VehicleTrim code

Returns:    transferFunction, from Linearized.transferFunctions class
'''
def CreateTransferFunction(trimState, trimInputs):
    out = Linearized.transferFunctions() # Trim for Va, and alpha just copied from input
    out.Va_trim = trimState.Va
    out.alpha_trim = trimState.alpha

    if (math.isclose(trimState.Va, 0)): # Beta trim if Va negative
        out.beta_trim = math.copysign(math.pi/2, trimState.u) # Needs to be sign of u, pi/2
    else:
        out.beta_trim = math.asin(trimState.v/trimState.Va)   # Else, sin(v/Va)

    out.gamma_trim = trimState.pitch - trimState.alpha # Gamma trim just theta-alpha
    out.theta_trim = trimState.pitch    # Just pitch
    out.phi_trim = trimState.roll       # Just roll
    
    # Equations 5.25, 24, 28, and from the supplementary textbook
    out.a_phi1 = (-1/2)*VPC.rho*(trimState.Va ** 2) *VPC.S*VPC.b*VPC.Cpp*(VPC.b / (2*trimState.Va))
    out.a_phi2 =  (1/2)*VPC.rho*(trimState.Va ** 2) *VPC.S*VPC.b*VPC.CpdeltaA

    out.a_beta1 = -(VPC.rho*trimState.Va*VPC.S) / (2*VPC.mass)*VPC.CYbeta
    out.a_beta2 =  (VPC.rho*trimState.Va*VPC.S) / (2*VPC.mass)*VPC.CYdeltaR

    out.a_theta1 = -(VPC.rho*(trimState.Va ** 2) *VPC.c*VPC.S) / (2*VPC.Jyy)*VPC.CMq*(VPC.c / (2*trimState.Va))
    out.a_theta2 = -(VPC.rho*(trimState.Va ** 2) *VPC.c*VPC.S) / (2*VPC.Jyy)*VPC.CMalpha
    out.a_theta3 =  (VPC.rho*(trimState.Va ** 2) *VPC.c*VPC.S) / (2*VPC.Jyy)*VPC.CMdeltaE

    out.a_V1 = ((VPC.rho*trimState.Va*VPC.S) / (VPC.mass)) * (VPC.CD0 + VPC.CDalpha*trimState.alpha + VPC.CDdeltaE*trimInputs.Elevator) - ((1/VPC.mass)*dThrust_dVa(trimState.Va, trimInputs.Throttle))
    out.a_V2 = (1 / VPC.mass) * dThrust_dThrottle(trimState.Va, trimInputs.Throttle)
    out.a_V3 = VPC.g0*math.cos(trimState.pitch - trimState.alpha)

    return out



'''
def dThrust_dThrottle(Va, Throttle, epsilon=0.01): Function to calculate
the numerical partial derivative of propeller thrust to change in throttle
setting using the actual prop function from complex propeller model
(inside the VehicleAerodynamicsModel class)

Parameters: Va – vehicle trim airspeed [m/s]
            Throttle – trim throttle setting [0-1]
            epsilon – step to take for perturbation in throttle setting

Returns:    dTdDeltaT: partial derivative [N/PWM]
'''
def dThrust_dThrottle(Va, Throttle, epsilon=0.01):
    vam = VehicleAerodynamicsModel.VehicleAerodynamicsModel()
    F1, M1 = vam.CalculatePropForces(Va, Throttle)
    F2, M2 = vam.CalculatePropForces(Va, Throttle + epsilon)
    out = (F2 - F1)/epsilon

    return out



'''
def dThrust_dVa(Va, Throttle, epsilon=0.5): Function to calculate the
numerical partial derivative of propeller thrust to change in airspeed
using the actual prop function from complex propeller model
(inside the VehicleAerodynamicsModel class)

Parameters: Va – vehicle trim airspeed [m/s]
            Throttle – trim throttle setting [0-1]
            epsilon – step to take for perturbation in Velocity

Returns:    dTdVa: partial derivative [N-s/m]
'''
def dThrust_dVa(Va, Throttle, epsilon=0.5):
    vam = VehicleAerodynamicsModel.VehicleAerodynamicsModel()
    F1, M1 = vam.CalculatePropForces(Va, Throttle)
    F2, M2 = vam.CalculatePropForces(Va + epsilon, Throttle)
    out = (F2 - F1)/epsilon

    return out