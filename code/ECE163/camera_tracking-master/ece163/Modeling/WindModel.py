import math
import random
from ..Containers import States
from ..Utilities import MatrixMath
from ..Constants import VehiclePhysicalConstants as VPC

class WindModel():

    def __init__(self, dT=VPC.dT, Va=VPC.InitialSpeed, drydenParamters=VPC.DrydenNoWind):

        self.dT = dT
        self.Va = Va
        self.drydenParamters = drydenParamters
        self.Wind = States.windState()
        #-----------------------------------------
        self.x_u = [[0]]
        self.Phi_u = [[1]]
        self.Gamma_u = [[0]] 
        self.H_u = [[1]]  
        #-----------------------------------------
        self.x_v = [[0], 
                    [0]]
        self.Phi_v = [[1, 0], 
                      [0, 1]]  
        self.Gamma_v = [[0], 
                        [0]]
        self.H_v = [[1, 1]]            
        #-----------------------------------------
        self.x_w = [[0], 
                    [0]]
        self.Phi_w = [[1, 0], 
                      [0, 1]]
        self.Gamma_w = [[0], 
                        [0]]
        self.H_w = [[1, 1]]  
        self.CreateDrydenTransferFns(dT, Va, drydenParamters)

        return
    
    def getWind(self):

        return self.Wind

    def setWind(self, windState):
        self.Wind = windState

        return

    def reset(self):
        self.dT = VPC.dT
        self.Va = VPC.InitialSpeed
        self.drydenParamters = VPC.DrydenNoWind
        self.Wind = States.windState()
        self.x_u = [[0]] 
        self.x_v = [[0], 
                    [0]] 
        self.x_w = [[0], 
                    [0]] 
        return
    
    def setWindModelParameters(self, Wn=0.0, We=0.0, Wd=0.0, drydenParamters=VPC.DrydenNoWind):
        self.Wind.Wn = Wn
        self.Wind.We = We
        self.Wind.Wd = Wd
        self.drydenParamters = drydenParamters
        self.CreateDrydenTransferFns(self.dT, VPC.InitialSpeed, drydenParamters)
        return

    def getDrydenTransferFns(self):
        return self.Phi_u, self.Gamma_u, self.H_u, self.Phi_v, self.Gamma_v, self.H_v, self.Phi_w, self.Gamma_w, self.H_w

    
    def CreateDrydenTransferFns(self, dT, Va, drydenParamters):
        if (drydenParamters == VPC.DrydenNoWind):
            self.Phi_u = [[1]] # 1x1
            self.Gamma_u = [[0]] # 1x1
            self.H_u = [[1]] # 1x1
            self.Phi_v = [[1, 0], [0, 1]] # 2x2
            self.Gamma_v = [[0], [0]] # 2x1
            self.H_v = [[1, 1]] # 1x2

            self.Phi_w = [[1, 0], [0, 1]] # 2x2
            self.Gamma_w = [[0], [0]] # 2x1
            self.H_w = [[1, 1]] # 1x2

            return
        Lu = drydenParamters.Lu
        Lv = drydenParamters.Lv
        Lw = drydenParamters.Lw
        sigmau = drydenParamters.sigmau
        sigmav = drydenParamters.sigmav
        sigmaw = drydenParamters.sigmaw
        #------------------------------------------------------------------------------------------
        self.Phi_u[0][0] = math.exp(-(Va / Lu) * dT)
        self.Gamma_u[0][0] = (Lu / Va) * (1 - (math.exp(-(Va / Lu) * dT)))
        self.H_u[0][0] = sigmau * math.sqrt((2 * Va) / (math.pi * Lu))
        #------------------------------------------------------------------------------------------
        self.Phi_v = [[ 1 - ((Va / Lv) * dT), -((Va / Lv) ** 2) * dT],
                      [dT,1 + ((Va / Lv) * dT)]]
        self.Phi_v = MatrixMath.scalarMultiply(math.exp(-(Va / Lv) * dT), self.Phi_v)
        self.Gamma_v = [[dT],
                        [(((Lv / Va) ** 2) * (math.exp((Va / Lv) * dT) - 1)) - ((Lv / Va) * dT)]]
        self.Gamma_v = MatrixMath.scalarMultiply(math.exp(-(Va / Lv) * dT), self.Gamma_v)
        self.H_v = [[1, Va / (math.sqrt(3) * Lv)]]
        self.H_v = MatrixMath.scalarMultiply(sigmav * math.sqrt((3 * Va) / (math.pi * Lv)), self.H_v)
        #------------------------------------------------------------------------------------------
        self.Phi_w = [[1 - ((Va / Lw) * dT), -((Va / Lw) ** 2) * dT],
                      [ dT, 1 + ((Va / Lw) * dT)]]
        self.Phi_w = MatrixMath.scalarMultiply(math.exp(-(Va / Lw) * dT), self.Phi_w)
        self.Gamma_w = [[dT],
                        [(((Lw / Va) ** 2) * (math.exp((Va / Lw) * dT) - 1)) - ((Lw / Va) * dT)]]
        self.Gamma_w = MatrixMath.scalarMultiply(math.exp(-(Va / Lw) * dT), self.Gamma_w)
        self.H_w = [[1, Va / (math.sqrt(3) * Lw)]]
        self.H_w = MatrixMath.scalarMultiply(sigmaw * math.sqrt((3 * Va) / (math.pi * Lw)), self.H_w)
        #-----------------------------------------------------------------------------------------
        return

    def Update(self, uu=None, uv=None, uw=None):
        if (uu == None):
            uu = random.gauss(0, 1)
        if (uv == None):
            uv = random.gauss(0, 1)
        if (uw == None):
            uw = random.gauss(0, 1)

        U1 = MatrixMath.multiply(self.Phi_u, self.x_u)
        U2 = MatrixMath.scalarMultiply(uu, self.Gamma_u)
        self.x_u = MatrixMath.add(U1, U2)
        #------------------------------------------------------------------------------------------
        V1 = MatrixMath.multiply(self.Phi_v, self.x_v)
        V2 = MatrixMath.scalarMultiply(uv, self.Gamma_v)
        self.x_v = MatrixMath.add(V1, V2)
        #------------------------------------------------------------------------------------------
        W1 = MatrixMath.multiply(self.Phi_w, self.x_w)
        W2 = MatrixMath.scalarMultiply(uw, self.Gamma_w)
        self.x_w = MatrixMath.add(W1, W2)
        #------------------------------------------------------------------------------------------
        self.Wind.Wu = MatrixMath.multiply(self.H_u, self.x_u)[0][0]
        self.Wind.Wv = MatrixMath.multiply(self.H_v, self.x_v)[0][0]
        self.Wind.Ww = MatrixMath.multiply(self.H_w, self.x_w)[0][0]
        
        return

        

    
   
