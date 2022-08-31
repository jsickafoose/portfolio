'''
Duseok Choi

'''

import math
from ..Containers import States
from ..Utilities import MatrixMath
from ..Utilities import Rotations
from ..Constants import VehiclePhysicalConstants as VPC


class VehicleDynamicsModel():

    def __init__(self, dT= 0.01):
        self.dT = dT
        self.state = States.vehicleState()
        self.dot = States.vehicleState()

        # return         

    def getVehicleState(self):

        return self.state

    def getVehicleDerivative(self):

        return self.dot
    
    
    def reset(self):

        self.state = States.vehicleState()
       
        # return

    def setVehicleState(self, state):

        self.state = state

        # return
    
    def setVehicleDerivative(self, state):

        self.dot = state 
        

        # return

    def Update(self,forcesMoments):

        self.dot = self.derivative(self.state,forcesMoments)
        self.state = self.IntegrateState(self.dT,self.state,self.dot)

 
    def derivative(self, state, forcesMoments):

        dot = States.vehicleState()

        pn = state.pn
        pe = state.pe
        pd = state.pd
        u = state.u
        v = state.v
        w = state.w

        dcm = state.R
        dcmTranspose = MatrixMath.transpose(dcm)
        Vb= [[u],[v],[w]]
        R_i_To_b = MatrixMath.multiply(dcmTranspose,Vb)

        dot.pn = R_i_To_b[0][0]
        dot.pe = R_i_To_b[1][0]
        dot.pd = R_i_To_b[2][0]

        #--------------------------------------------------------------
        yaw = state.yaw
        pitch = state.pitch
        roll = state.roll
        fx = forcesMoments.Fx
        fy = forcesMoments.Fy
        fz = forcesMoments.Fz
        p = state.p
        q = state.q
        r = state.r

        mat_0 = [[(r * v) - (q * w)], 
                [(p * w) - (r * u)], 
                [(q * u) - (p * v)]]
        f = [[fx], [fy], [fz]]
        mat_uvw = MatrixMath.add(mat_0, MatrixMath.scalarMultiply(1/VPC.mass, f))

        dot.u = mat_uvw[0][0]
        dot.v = mat_uvw[1][0]
        dot.w = mat_uvw[2][0]
        #-----------------------------------------------------------------

        mat_1 = [[1, math.sin(roll) * math.tan(pitch), math.cos(roll) * math.tan(pitch)], 
                [0, math.cos(roll), -math.sin(roll)], 
                [0, math.sin(roll)/math.cos(pitch), math.cos(roll)/math.cos(pitch)]]
        PQR_rate = [[p], [q], [r]]
        RPY_rate = MatrixMath.multiply(mat_1, PQR_rate)

        dot.roll = RPY_rate[0][0]
        dot.pitch = RPY_rate[1][0]
        dot.yaw = RPY_rate[2][0]

        #---------------------------------------------------------------------

        Jx = VPC.Jxx
        Jy = VPC.Jyy
        Jz = VPC.Jzz
        Jxz = VPC.Jxz
        Gamma = VPC.Jdet
        Gamma1 = VPC.Gamma1
        Gamma2 = VPC.Gamma2
        Gamma3 = Jz / Gamma
        Gamma4 = Jxz / Gamma
        Gamma5 = (Jz - Jx) / Jy
        Gamma6 = Jxz / Jy
        Gamma7 = VPC.Gamma7
        Gamma8 = Jx / Gamma
        l = forcesMoments.Mx
        m = forcesMoments.My
        n = forcesMoments.Mz

        mat_2 = [[(Gamma1 * p * q) - (Gamma2 * q * r)], 
                [(Gamma5 * p * r) - (Gamma6 * (p ** 2 - r ** 2))], 
                [(Gamma7 * p * q) - (Gamma1 * q * r)]]
        mat_3 = [[(Gamma3 * l) + (Gamma4 * n)], 
                [(1/Jy) * m], 
                [(Gamma4 * l) + (Gamma8 * n)]]

        Derivative_PQR_rate = MatrixMath.add(mat_2, mat_3)
        dot.p = Derivative_PQR_rate[0][0]
        dot.q = Derivative_PQR_rate[1][0]
        dot.r = Derivative_PQR_rate[2][0]   

        #----------------------------------------------------------------------------------------
        
        dotR = MatrixMath.scalarMultiply(-1, MatrixMath.multiply(MatrixMath.skew(p, q, r), dcm))
        dot.R = dotR
  
        dot.Va = state.Va
        dot.alpha = state.alpha
        dot.beta = state.beta
        dot.chi = math.atan2(dot.pe,dot.pn)

        return dot

    def Rexp(self,dT,state,dot):

        #------------------------------------------------------------------------------
        pk = state.p
        qk = state.q
        rk = state.r
        Dot_pk = dot.p
        Dot_qk = dot.q
        Dot_rk = dot.r

        pqr_k = [[pk],[qk],[rk]]
        Dot_pqr_k = [[Dot_pk],[Dot_qk],[Dot_rk]]

        w_BodyFixedRotation = MatrixMath.add(pqr_k, MatrixMath.scalarMultiply(dT/2,Dot_pqr_k ))

        p = w_BodyFixedRotation[0][0]
        q = w_BodyFixedRotation[1][0]
        r = w_BodyFixedRotation[2][0]

           

        wMagnitude= math.hypot(p, q, r)
        w_skew = MatrixMath.skew(p,q,r)
        I_matrix = [[1, 0, 0], 
                    [0, 1, 0], 
                    [0, 0, 1]]
            
        if (wMagnitude < 0.1):
            case1 = dT - (((dT ** 3) * (wMagnitude ** 2)) / 6) + (((dT ** 5) * (wMagnitude ** 4)) / 120) 
            case2 = ((dT ** 2) / 2) - (((dT ** 4) * (wMagnitude ** 2)) / 24) + (((dT ** 6) * (wMagnitude ** 4)) / 720) 
        else:
            case1 = math.sin(wMagnitude * dT) / wMagnitude
            case2 = (1 - math.cos(wMagnitude * dT)) / (wMagnitude ** 2)

        Equation24_Attitude = MatrixMath.scalarMultiply(case1, w_skew)
        Equation25_Attitude = MatrixMath.scalarMultiply(case2, MatrixMath.multiply(w_skew, w_skew))

        newRexp = MatrixMath.add(MatrixMath.subtract(I_matrix, Equation24_Attitude), Equation25_Attitude)

            #----------------------------------------------------------------
        
        return newRexp

            #-------------------------
    def ForwardEuler(self, dT,state,dot):
        newState = States.vehicleState()

        newState.pn = state.pn + (dot.pn * dT)
        newState.pe = state.pe + (dot.pe * dT)
        newState.pd = state.pd + (dot.pd * dT)
        
        newState.u = state.u + (dot.u * dT)
        newState.v = state.v + (dot.v * dT)
        newState.w = state.w + (dot.w * dT)

        newState.p = state.p + (dot.p * dT)
        newState.q = state.q + (dot.q * dT)
        newState.r = state.r + (dot.r * dT)
        
        return newState

    #from lecture ECE163_Lecture02_KinematicsDynamics_and_ForcesMoments_2020-10-15.mp4 14:29 not working?
    def IntegrateState(self, dT, state, dot):
        
        newState = States.vehicleState()
   

        newState =  self.ForwardEuler(dT,state,dot)

        newState.R = MatrixMath.multiply(self.Rexp(dT, state, dot), state.R) 

        EulerYPR = Rotations.dcm2Euler(newState.R)

        newState.yaw = EulerYPR[0]
        newState.pitch = EulerYPR[1]
        newState.roll = EulerYPR[2]

        newState.alpha = state.alpha
        newState.beta = state.beta
        newState.Va = state.Va
        newState.chi = math.atan2(dot.pe,dot.pn)

        return newState
    
           