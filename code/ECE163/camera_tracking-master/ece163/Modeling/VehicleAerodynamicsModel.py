import math
from ..Containers import States
from ..Containers import Inputs
from ..Modeling import VehicleDynamicsModel as VDM
from ..Modeling import WindModel
from ..Utilities import MatrixMath
from ..Utilities import Rotations
from ..Constants import VehiclePhysicalConstants as VPC

class VehicleAerodynamicsModel():
    #TA Meg Section / need pn pe pd u
    def __init__(self, initialSpeed=25.0, initialHeight=-100.0 ,wind = VPC.DrydenNoWind):
        self.VehicleDynamics = VDM.VehicleDynamicsModel()
        self.initialSpeed = initialSpeed
        self.initialHeight = initialHeight
        self.VehicleDynamics.state.pn = VPC.InitialNorthPosition
        self.VehicleDynamics.state.pe = VPC.InitialEastPosition
        self.VehicleDynamics.state.pd = VPC.InitialDownPosition
        self.VehicleDynamics.state.u = initialSpeed
        self.WindModel = WindModel.WindModel()
        
        return

    def CalculateAirspeed(self, state, wind):
        Wn = wind.Wn
        We = wind.We
        Wd = wind.Wd
        if (Wn == 0 and We == 0 and Wd == 0):
            Xw = 0
            Yw = 0
        else:
            Xw = math.atan2(We, Wn)
            Yw = -math.asin(Wd / (math.hypot(Wn, We, Wd)))
        #-----------------------------------------------------------------
        Xw1 = [math.cos(Xw), math.sin(Xw), 0]
        Xw2 = [-math.sin(Xw), math.cos(Xw), 0]
        Xw3 = [0, 0, 1]
        Xw33 = [Xw1, Xw2, Xw3]
        #-----------------------------------------------------------------
        Yw1 = [math.cos(Yw), 0, -math.sin(Yw)]
        Yw2 = [0, 1, 0]
        Yw3 = [math.sin(Yw), 0, math.cos(Yw)]
        Yw33 = [Yw1, Yw2, Yw3]
        #-----------------------------------------------------------------
        RAzimuthWElevation = MatrixMath.multiply(Yw33, Xw33)
        Wu = wind.Wu
        Wv = wind.Wv
        Ww = wind.Ww
        Wuvw = [[Wu], 
                [Wv], 
                [Ww]]
        #-----------------------------------------------------------------
        Wi = MatrixMath.multiply(MatrixMath.transpose(RAzimuthWElevation), Wuvw)
        Wned = [[Wn], [We], [Wd]]
        dcm = state.R
        WB = MatrixMath.multiply(dcm, MatrixMath.add(Wned, Wi))
        u = state.u
        v = state.v
        w = state.w
        U_r = u - WB[0][0]
        V_R = v - WB[1][0]
        W_R = w - WB[2][0]
        #-----------------------------------------------------------------
        Va = math.hypot(U_r, V_R, W_R)
        alpha = math.atan2(W_R, U_r)
        if (math.isclose(Va, 0)):
            beta = 0
        else:
            beta = math.asin(V_R / Va)

        return Va, alpha, beta
         
    def CalculateCoeff_alpha(self, alpha):
        # #----------------------------------------------------------------
       
        # #----------------------------------------------------------------
        CL_laminar = VPC.CL0 + (VPC.CLalpha * alpha)
        CD_laminar = VPC.CDp + (((VPC.CL0 + VPC.CLalpha * alpha) ** 2) / (math.pi * VPC.e * VPC.AR))
        CL_turbulent = 2*(math.sin(alpha)) * (math.cos(alpha))
        CD_turbulent = 2 * ((math.sin(alpha)) ** 2)

        sigmaNumer = 1 + math.exp(-VPC.M * (alpha - VPC.alpha0)) + math.exp(VPC.M * (alpha + VPC.alpha0))
        sigmaDenom = (1 + math.exp(-VPC.M * (alpha - VPC.alpha0))) * (1 + math.exp(VPC.M * (alpha + VPC.alpha0)))
        sigma = sigmaNumer / sigmaDenom

        CL_alpha = (1 - sigma) * CL_laminar + (sigma * CL_turbulent)
        CD_alpha = (1 - sigma) * CD_laminar + (sigma * CD_turbulent)
        CM_alpha = VPC.CM0 + (VPC.CMalpha * alpha)
       

        #----------------------------------------------------------------
        return CL_alpha, CD_alpha, CM_alpha

    def CalculatePropForces(self, Va, Throttle):

        #----------------------------------------------------------------
        KT = 60 / (2 * math.pi * VPC.KV)
        KE = KT
        Vin = VPC.V_max * Throttle

        a = (VPC.rho * (VPC.D_prop ** 5) * VPC.C_Q0) / (4 * (math.pi ** 2))
        b = ((VPC.rho * (VPC.D_prop ** 4) * Va * VPC.C_Q1) / (2 * math.pi)) + ((KT * KE) / VPC.R_motor)
        c = (VPC.rho * (VPC.D_prop ** 3) * (Va ** 2) * VPC.C_Q2) - (KT * (Vin / VPC.R_motor)) + (KT * VPC.i0)
        
        try:
            omega = (-b + math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
        except:
            omega = 100
        #----------------------------------------------------------------

        J = (2 * math.pi * Va) / (omega * VPC.D_prop) 

        CT_ordinary = VPC.C_T0 + (VPC.C_T1 * J) + (VPC.C_T2 * (J ** 2))
        CQ_ordinary = VPC.C_Q0 + (VPC.C_Q1 * J) + (VPC.C_Q2 * (J ** 2))

        FXPropForce = (VPC.rho * (omega ** 2) * (VPC.D_prop ** 4) * (CT_ordinary)) / (4 * (math.pi ** 2))
        MXPropForce = -(VPC.rho * (omega ** 2) * (VPC.D_prop ** 5) * (CQ_ordinary)) / (4 * (math.pi ** 2))
        #----------------------------------------------------------------
        return FXPropForce, MXPropForce

    def Update(self, controls):
        state = self.VehicleDynamics.state

        self.WindModel.Update() 
        wind = self.WindModel.Wind
        AllForce = self.updateForces(state, controls, wind)

        self.VehicleDynamics.Update(AllForce)

        return

    def aeroForces(self, state):
        Va = state.Va
        alpha = state.alpha 
        beta = state.beta

        # need? or not need? according to piazza?
        #Meg said theres two ways: 1.put divide entire thing by Va 2.make if function
        if (Va == 0):
            return Inputs.forcesMoments()
        #With Meg section/ she said we still need CM
        #------------------------------------------------------------------
        CL_alpha, CD_alpha, CM_alpha = self.CalculateCoeff_alpha(alpha)

        CX_alpha = (-CD_alpha * math.cos(alpha)) + (CL_alpha * math.sin(alpha))
        CXq_alpha = (-VPC.CDq * math.cos(alpha)) + (VPC.CLq * math.sin(alpha))
        CZ_alpha = (-CD_alpha * math.sin(alpha)) - (CL_alpha * math.cos(alpha))
        CZq_alpha = (-VPC.CDq * math.sin(alpha)) - (VPC.CLq * math.cos(alpha))

        FX = CX_alpha + (CXq_alpha * ((VPC.c / (2 * Va)) * state.q))
        FY = VPC.CY0 + (VPC.CYbeta * beta) + (VPC.CYp * ((VPC.b / (2 * Va)) * state.p)) + (VPC.CYr * ((VPC.b / (2 * Va)) * state.r))
        FZ = CZ_alpha + (CZq_alpha * ((VPC.c / (2 * Va)) * state.q))

        Cons = (1/2)*(VPC.rho)*(Va ** 2)*(VPC.S)

        FX_FY_FZ = [[FX],
                    [FY],
                    [FZ]]
        Final_FX_FY_FZ = MatrixMath.scalarMultiply(Cons, FX_FY_FZ)

        FinalFocre = Inputs.forcesMoments()
        FinalFocre.Fx = Final_FX_FY_FZ[0][0]
        FinalFocre.Fy = Final_FX_FY_FZ[1][0]
        FinalFocre.Fz = Final_FX_FY_FZ[2][0]
         #------------------------------------------------------------------
        MX = VPC.b * (VPC.Cl0 + (VPC.Clbeta * beta) + (VPC.Clp * ((VPC.b / (2 * Va)) * state.p)) + (VPC.Clr * ((VPC.b / (2 * Va)) * state.r)))
        MY = VPC.c * (VPC.CM0 + (VPC.CMalpha * alpha) + (VPC.CMq * ((VPC.c / (2 * Va)) * state.q)))
        MZ = VPC.b * (VPC.Cn0 + (VPC.Cnbeta * beta) + (VPC.Cnp * ((VPC.b / (2 * Va)) * state.p)) + (VPC.Cnr * ((VPC.b / (2 * Va)) * state.r)))   

        MX_MY_MZ = [[MX],
                    [MY],
                    [MZ]]

        Final_MX_MY_MZ = MatrixMath.scalarMultiply(Cons, MX_MY_MZ)

        FinalFocre.Mx = Final_MX_MY_MZ[0][0]
        FinalFocre.My = Final_MX_MY_MZ[1][0]
        FinalFocre.Mz = Final_MX_MY_MZ[2][0]
        
        return FinalFocre

    def controlForces(self, state, controls):

        
        Va = state.Va
        alpha = state.alpha
        beta = state.beta
        
        Delta_a = controls.Aileron
        Delta_e = controls.Elevator
        Delta_r = controls.Rudder
        Delta_t = controls.Throttle

        CX_Delta_e_alpha = (-VPC.CDdeltaE * math.cos(alpha)) + (VPC.CLdeltaE * math.sin(alpha))
        CZ_Delta_e_alpha = (-VPC.CDdeltaE * math.sin(alpha)) - (VPC.CLdeltaE * math.cos(alpha))

        FX = (CX_Delta_e_alpha * Delta_e)
        FY = (VPC.CYdeltaA * Delta_a) + (VPC.CYdeltaR * Delta_r)
        FZ = (CZ_Delta_e_alpha * Delta_e)

        Cons = Cons = (1/2)*(VPC.rho)*(Va ** 2)*(VPC.S)

        FX_FY_FZ = [[FX],
                    [FY],
                    [FZ]]

        Final_FX_FY_FZ = MatrixMath.scalarMultiply(Cons, FX_FY_FZ)
        
        FinalFocre = Inputs.forcesMoments()
        FinalFocre.Fx = Final_FX_FY_FZ[0][0]
        FinalFocre.Fy = Final_FX_FY_FZ[1][0]
        FinalFocre.Fz = Final_FX_FY_FZ[2][0]

        MX = VPC.b * ((VPC.CldeltaA * Delta_a) + (VPC.CldeltaR * Delta_r))
        MY = VPC.c * (VPC.CMdeltaE * Delta_e)
        MZ = VPC.b * ((VPC.CndeltaA * Delta_a) + (VPC.CndeltaR * Delta_r))

        MX_MY_MZ = [[MX],
                    [MY],
                    [MZ]]

        Final_MX_MY_MZ = MatrixMath.scalarMultiply(Cons, MX_MY_MZ)

        FinalFocre.Mx = Final_MX_MY_MZ[0][0]
        FinalFocre.My = Final_MX_MY_MZ[1][0]
        FinalFocre.Mz = Final_MX_MY_MZ[2][0]

        FXPropForce, MXPropForce = self.CalculatePropForces(Va, Delta_t)

        FinalFocre.Fx = FinalFocre.Fx + FXPropForce
        FinalFocre.Mx = FinalFocre.Mx + MXPropForce

        return FinalFocre

    def getVehicleDynamicsModel(self):
        return self.VehicleDynamics

    def getVehicleState(self):
        return self.VehicleDynamics.state

    
    def getWindModel(self):
        return self.WindModel

    def gravityForces(self, state):
        FM = Inputs.forcesMoments()

        #we can either use VPC.mass insdie matrix or outside since it's constant
        mg = [  [0],
                [0],
                [VPC.mass * VPC.g0]]

        GF = MatrixMath.multiply(state.R, mg)

        FM.Fx = GF[0][0]
        FM.Fy = GF[1][0]
        FM.Fz = GF[2][0]
        FM.Mx = 0
        FM.My = 0
        FM.Mz = 0

        return FM

    def reset(self):
        self.VehicleDynamics = VDM.VehicleDynamicsModel()
        self.initialSpeed = VPC.InitialSpeed
        self.initialHeight = VPC.InitialSpeed
        self.VehicleDynamics.state.pn = VPC.InitialNorthPosition
        self.VehicleDynamics.state.pe = VPC.InitialEastPosition
        self.VehicleDynamics.state.pd = VPC.InitialDownPosition
        self.VehicleDynamics.state.u = VPC.initialSpeed

        return

    def setVehicleState(self, state):
        self.VehicleDynamics.state = state

        return
   
    def setWindModel(self, windModel):
        self.WindModel = WindModel

        return

    def updateForces(self, state, controls, wind=None):
        #wind = none still?  
       
        state.Va = math.hypot(state.u, state.v, state.w)    
        state.alpha = math.atan2(state.w, state.u)        
        if math.isclose(state.Va, 0.0):                  
            state.beta = 0.0
        else:
            state.beta = math.asin(state.v/state.Va)

        if (wind != None):
            state.Va, state.alpha, state.beta = self.CalculateAirspeed(state, wind) 
      
        # state.Va = Va
        # state.alpha = alpha
        # state.beta = beta


        FG_update = self.gravityForces(state)
        FA_update = self.aeroForces(state)
        FC_update = self.controlForces(state, controls)

        FG_FA_DC_Total = Inputs.forcesMoments()


        #x,y,z total force all

        FG_FA_DC_Total.Fx = FG_update.Fx + FA_update.Fx + FC_update.Fx
        FG_FA_DC_Total.Fy = FG_update.Fy + FA_update.Fy + FC_update.Fy
        FG_FA_DC_Total.Fz = FG_update.Fz + FA_update.Fz + FC_update.Fz

        FG_FA_DC_Total.Mx = FA_update.Mx + FC_update.Mx
        FG_FA_DC_Total.My = FA_update.My + FC_update.My
        FG_FA_DC_Total.Mz = FA_update.Mz + FC_update.Mz


        return FG_FA_DC_Total

