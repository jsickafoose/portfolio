import math
import random
from ..Containers import Inputs as inputs
from ..Containers import States
from ..Utilities import MatrixMath
from ..Constants import VehiclePhysicalConstants as VPC

class WindModel:
    '''
    function to initialize the wind model code. Will load the appropriate constants
    that parameterize the wind gusts from the Dryden gust model. Creates the
    discrete transfer functions for the gust models that are used to update the
    local wind gusts in the wind frame. These are added to the inertial wind
    (Wn, We, Wd) that are simply constants. Discrete models are held in self and used
    in the Update function.

    To turn off gusts completely, use the DrydenNoGusts parameters.

    Parameters: dT – time step [s] for numerical integration of wind
                Va – nominal flight speed [m/s]
                drydenParamters – class from Inputs

    Returns: none
    '''
    def __init__(self, dT=0.01, Va=25.0, drydenParamters=inputs.drydenParameters(Lu=0.0, Lv=0.0, Lw=0.0, sigmau=0.0, sigmav=0.0, sigmaw=0.0)):
        ## Sets parameters as internal variables
        self.dT = dT
        self.Va = Va
        self.drydenParamters = drydenParamters

        ## Not obvious from the lab doc, but here initializes a WindState
        self.windState = States.windState()

        ## Sets internal vectors for Xu, Xv, and Xw
        self.Xu = [[0]]
        self.Xv = [[0], [0]]
        self.Xw = [[0], [0]]

        ## Sets internal variables for Phi, Gamma, and H in each wind axis
        self.Phi_u   = [[1]]
        self.Gamma_u = [[0]]
        self.H_u     = [[1]]

        self.Phi_v   = [[1, 0],
                        [0, 1]]
        self.Gamma_v =  [[0], [0]]
        self.H_v     =  [[1, 1]]

        self.Phi_w   = [[1, 0],
                        [0, 1]]
        self.Gamma_w =  [[0], [0]]
        self.H_w     =  [[1, 1]]

        ## Finally, creates the starting DrydenTransferFuncs
        self.CreateDrydenTransferFns(dT, Va, drydenParamters)



    '''
    Wrapper function that resets the wind model code (but does not reset the
    model chosen for wind. To change the model transfer functions you need to
    use CreateDrydenTranferFns

    Returns: none
    '''
    def reset(self):
        self.dT = VPC.dT
        self.Va = VPC.InitialSpeed
        self.drydenParamters = inputs.drydenParameters(VPC.DrydenNoWind)
        self.windState = States.windState()
        ## Sets internal vectors for Xu, Xv, and Xw
        self.Xu = [[0]]
        self.Xv = [[0], [0]]
        self.Xw = [[0], [0]]

        ## Sets internal variables for Phi, Gamma, and H in each wind axis
        # self.CreateDrydenTransferFns(self.dT, self.Va, inputs.drydenParameters(VPC.DrydenNoWind))




    '''
    Wrapper function that allows for injecting constant wind and gust values into
    the class windState from vehicleStates with inertial constant
    wind and wind frame gusts

    Returns: none
    '''
    def setWind(self, windState):
        self.windState = windState



    '''
    Wrapper function to return the wind state from the module

    Returns: windState class
    '''
    def getWind(self):
        return self.windState



    '''
    Wrapper function that will inject constant winds and gust parameters into
    the wind model using the constant wind in the inertial frame (steady wind)
    and gusts that are stochastically derived in the body frame using the
    Dryden wind gust models.

    Parameters: Wn – Steady wind in inertial North direction [m/s]
                We – Steady wind in inertial East direction [m/s]
                Wd – Steady wind in inertial Down direction [m/s], should usually be zero
                drydenParamters – model of Dryden parameters taken from constants

    Returns: none
    '''
    def setWindModelParameters(self, Wn=0.0, We=0.0, Wd=0.0, drydenParamters=inputs.drydenParameters(Lu=0.0, Lv=0.0, Lw=0.0, sigmau=0.0, sigmav=0.0, sigmaw=0.0)):
        self.windState.Wn = Wn
        self.windState.We = We
        self.windState.Wd = Wd
        self.drydenParamters = drydenParamters
        self.CreateDrydenTransferFns(self.dT, self.Va, drydenParamters)



    '''
    Function creates the Dryden transfer functions in discrete form. These
    are used in generating the gust models for wind gusts (in wind frame).

    Parameters: dT – time step [s]
                Va – nominal flight speed [m/s]
                drydenParamters – Dryden Wing Gust Model from VehiclePhysicalConstants

    Returns: none
    '''
    def CreateDrydenTransferFns(self, dT, Va, drydenParamters):
        ##### Takes care of the case of Va being 0 to avoid divide by 0 #####
        if math.isclose(Va, 0.0):
            self.Phi_u   = [[1]]    # Sets each Phi, Gamma, H to what they would be on initialization
            self.Gamma_u = [[0]]
            self.H_u     = [[1]]

            self.Phi_v   = [[1, 0],
                            [0, 1]]
            self.Gamma_v =  [[0], [0]]
            self.H_v     =  [[1, 1]]

            self.Phi_w   = [[1, 0],
                            [0, 1]]
            self.Gamma_w =  [[0], [0]]
            self.H_w     =  [[1, 1]]
        else:
        #### U component
        #### As long as Va != 0, moves on to make sure Lu, Lv, and/or Lw aren't either
            if math.isclose(drydenParamters.Lu, 0): # Sets each Phi, Gamma, H to what they would be on initialization if respective L = 0
                self.Phi_u   = [[1]]
                self.Gamma_u = [[0]]
                self.H_u     = [[1]]
            else:                       # Else, does the crazy math
                self.Phi_u[0][0] = math.exp(-(Va/drydenParamters.Lu)*dT)
                self.Gamma_u[0][0] = (drydenParamters.Lu/Va) * (1-(math.exp(-(Va/drydenParamters.Lu)*dT)))
                self.H_u[0][0] = drydenParamters.sigmau * (math.sqrt((2*Va)/(math.pi*drydenParamters.Lu)))

        #### V component
            if math.isclose(drydenParamters.Lv, 0):
                self.Phi_v   = [[1, 0],
                                [0, 1]]
                self.Gamma_v =  [[0], [0]]
                self.H_v     =  [[1, 1]]
            else:
                FirstPart_v = (math.exp((-Va/drydenParamters.Lv)*dT)) # I calculate the first exp((-Va/Lv)*dT)) to be slightly more efficient
                Phi_v_m   = [[(1-(Va/drydenParamters.Lv)*dT), (-((Va/drydenParamters.Lv)**2)*dT)],
                             [(dT), (1+(Va/drydenParamters.Lv)*dT)]]
                Gamma_v_m = [[dT], [((drydenParamters.Lv/Va)**2)*((math.exp((Va/drydenParamters.Lv)*dT))-1)-((drydenParamters.Lv/Va)*dT)]]
                H_v_m = [[1, (Va/(math.sqrt(3)*drydenParamters.Lv))]]
                self.Phi_v = MatrixMath.scalarMultiply(FirstPart_v, Phi_v_m)
                self.Gamma_v = MatrixMath.scalarMultiply(FirstPart_v, Gamma_v_m)
                self.H_v = MatrixMath.scalarMultiply(drydenParamters.sigmav*math.sqrt((3*Va) / (math.pi*drydenParamters.Lv)), H_v_m)

        #### W component
            if math.isclose(drydenParamters.Lw, 0):
                self.Phi_w   = [[1, 0],
                                [0, 1]]
                self.Gamma_w =  [[0], [0]]
                self.H_w     =  [[1, 1]]
            else:
                FirstPart_w = (math.exp((-Va/drydenParamters.Lw)*dT))
                Phi_w_m = [[(1-(Va/drydenParamters.Lw)*dT), (-((Va/drydenParamters.Lw)**2)*dT)],
                           [(dT), (1+(Va/drydenParamters.Lw)*dT)]]
                Gamma_w_m = [[dT], [((drydenParamters.Lw/Va)**2)*((math.exp((Va/drydenParamters.Lw)*dT))-1)-((drydenParamters.Lw/Va)*dT)]]
                H_w_m = [[1, (Va/(math.sqrt(3)*drydenParamters.Lw))]]
                self.Phi_w = MatrixMath.scalarMultiply(FirstPart_w, Phi_w_m)
                self.Gamma_w = MatrixMath.scalarMultiply(FirstPart_w, Gamma_w_m)
                self.H_w = MatrixMath.scalarMultiply(drydenParamters.sigmaw * math.sqrt((3*Va) / (math.pi*drydenParamters.Lw)), H_w_m)



    '''
    Wrapper function to return the internals of the Dryden Transfer function
    in order to be able to test the code without requiring consistent
    internal names. Returns the discretized version of the Drydem gust model
    as outlined in the ECE163_DrydenWindModel handout
    (Phi_u, Gamma_u, H_u, Phi_v, Gamma_v, H_v, Phi_w, Gamma_w, H_w).

    Parameters: none

    Returns: Phi_u, Gamma_u, H_u, Phi_v, Gamma_v, H_v, Phi_w, Gamma_w, H_w
    '''
    def getDrydenTransferFns(self):
        return self.Phi_u, self.Gamma_u, self.H_u, self.Phi_v, self.Gamma_v, self.H_v, self.Phi_w, self.Gamma_w, self.H_w



    '''
    Function that updates the wind gusts and inserts them back into the .Wind
    portion of self. This is done by running white noise [Gaussian(0,1)]
    through the coloring filters of the Dryden Wind Gust model.

    Parameters: uu – optional argument for injecting input to Hu(s), defaults to None
                uv – optional argument for injecting input to Hv(s), defaults to None
                uw – optional argument for injecting input to Hw(s), defaults to None

    Returns: none, gust values are updated internally
    '''
    def Update(self, uu=None, uv=None, uw=None):
        ## If no u, v or w value is given, make's it a random Gauss
        if uu is None:
            uu = random.gauss(0, 1)
        if uv is None:
            uv = random.gauss(0, 1)
        if uw is None:
            uw = random.gauss(0, 1)

        ## Updates X, then sets W using the new X
        self.Xu = [[self.Phi_u[0][0]*self.Xu[0][0] + self.Gamma_u[0][0]*uu]]
        self.windState.Wu = self.H_u[0][0]*self.Xu[0][0]

        self.Xv = [[self.Phi_v[0][0]*self.Xv[0][0] + self.Phi_v[0][1]*self.Xv[1][0] + self.Gamma_v[0][0]*uv],
                   [self.Phi_v[1][0]*self.Xv[0][0] + self.Phi_v[1][1]*self.Xv[1][0] + self.Gamma_v[1][0]*uv]]
        self.windState.Wv = self.H_v[0][0]*self.Xv[0][0] + self.H_v[0][1]*self.Xv[1][0]

        self.Xw = [[self.Phi_w[0][0]*self.Xw[0][0] + self.Phi_w[0][1]*self.Xw[1][0] + self.Gamma_w[0][0]*uw],
                   [self.Phi_w[1][0]*self.Xw[0][0] + self.Phi_w[1][1]*self.Xw[1][0] + self.Gamma_w[1][0]*uw]]
        self.windState.Ww = self.H_w[0][0]*self.Xw[0][0] + self.H_w[0][1]*self.Xw[1][0]