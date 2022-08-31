import math
from ece163.Modeling import VehicleAerodynamicsModel as VAM
from ece163.Constants import VehiclePhysicalConstants as VPC
from ece163.Containers import States
from ece163.Containers import Inputs
from ece163.Containers import Linearized
from ece163.Utilities import MatrixMath
   
def CreateTransferFunction(trimState, trimInputs):
    tf = Linearized.transferFunctions()
    tf.Va_trim = trimState.Va
    tf.alpha_trim = trimState.alpha

    if (math.isclose(trimState.Va, 0)):
        tf.beta_trim = math.copysign(math.pi / 2, trimState.u)
    else:
        tf.beta_trim = math.asin(trimState.v / trimState.Va)

    tf.gamma_trim = trimState.pitch - trimState.alpha
    tf.theta_trim = trimState.pitch
    tf.phi_trim = trimState.roll
    VaStar = trimState.Va
    AlphaStar = trimState.alpha
    ThetaStar = trimState.pitch
    DeltaE_Star = trimInputs.Elevator
    DeltaT_star = trimInputs.Throttle

 
    tf.a_phi1 = -1/2 * VPC.rho * (VaStar ** 2) * VPC.S * VPC.b * VPC.Cpp * (VPC.b / (2 * VaStar))
    tf.a_phi2 = 1/2 * VPC.rho * (VaStar ** 2) * VPC.S * VPC.b * VPC.CpdeltaA

    tf.a_beta1 = -(VPC.rho * VaStar * VPC.S) / (2 * VPC.mass) * VPC.CYbeta
    tf.a_beta2 = (VPC.rho * VaStar * VPC.S) / (2 * VPC.mass) * VPC.CYdeltaR

    tf.a_theta1 = -(VPC.rho * (VaStar ** 2) * VPC.c * VPC.S) / (2 * VPC.Jyy) * VPC.CMq * (VPC.c / (2 * VaStar))
    tf.a_theta2 = -(VPC.rho * (VaStar ** 2) * VPC.c * VPC.S) / (2 * VPC.Jyy) * VPC.CMalpha
    tf.a_theta3 = (VPC.rho * (VaStar ** 2) * VPC.c * VPC.S) / (2 * VPC.Jyy) * VPC.CMdeltaE

    tf.a_V1 = ((VPC.rho * VaStar * VPC.S) / (VPC.mass)) * (VPC.CD0 + (VPC.CDalpha * AlphaStar) + (VPC.CDdeltaE * DeltaE_Star)) - ((1 / VPC.mass) * dThrust_dVa(VaStar, DeltaT_star))
    tf.a_V2 = (1 / VPC.mass) * dThrust_dThrottle(VaStar, DeltaT_star)
    tf.a_V3 = VPC.g0 * math.cos(ThetaStar - AlphaStar)

    return tf

def dThrust_dThrottle(Va, Throttle, epsilon=0.01):
    VehicleAerodynamics = VAM.VehicleAerodynamicsModel()
    Fx1, Mx1 = VehicleAerodynamics.CalculatePropForces(Va, Throttle)
    Fx2, Mx2 = VehicleAerodynamics.CalculatePropForces(Va, Throttle + epsilon)
    dTdDeltaT = (Fx2 - Fx1) / epsilon

    return dTdDeltaT

def dThrust_dVa(Va, Throttle, epsilon=0.5):
    VehicleAerodynamics = VAM.VehicleAerodynamicsModel()
    Fx1, Mx1 = VehicleAerodynamics.CalculatePropForces(Va, Throttle)
    Fx2, Mx2 = VehicleAerodynamics.CalculatePropForces(Va + epsilon, Throttle)
    dTdVa = (Fx2 - Fx1) / epsilon

    return dTdVa