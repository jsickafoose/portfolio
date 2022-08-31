"""
Duseok Choi
"""
import math
import random
from ece163.Modeling import VehicleAerodynamicsModel
from ece163.Utilities import MatrixMath
from ..Containers import Sensors
from ..Constants import VehiclePhysicalConstants as VPC
from ..Constants import VehicleSensorConstants as VSC
from ..Modeling import VehicleAerodynamicsModel

class GaussMarkov():
    def __init__(self, dT=VPC.dT, tau=1000000.0, eta=0.0):
        self.dT = dT
        self.tau = tau
        self.eta = eta
        self.v = 0

        return
 
    def reset(self):
        self.dT = 0.01
        self.tau = 1000000.0
        self.eta = 0.0 
        self.v = 0

        return

    def update(self, vnoise=None):
        if (vnoise == None):
            vnoise = random.gauss(0, self.eta)
        self.v = (math.exp(-self.dT / self.tau) * self.v) + vnoise

        return self.v

class GaussMarkovXYZ():
    def __init__(self, dT=0.01, tauX=1000000.0, etaX=0.0, tauY=None, etaY=None, tauZ=None, etaZ=None):

        self.dT = dT
        self.tauX = tauX
        self.etaX = etaX
        self.tauY = tauY
        self.etaY = etaY
        self.tauZ = tauZ
        self.etaZ = etaZ

        self.GM_X = GaussMarkov(dT, tauX, etaX)    
        if tauY is None:                       
            self.GM_Y = GaussMarkov(dT, tauX, etaX)
            self.GM_Z = GaussMarkov(dT, tauX, etaX)
        elif tauZ is None:                      
            self.GM_Y = GaussMarkov(dT, tauY, etaY)
            self.GM_Z = GaussMarkov(dT, tauY, etaY)
        else:                                  
            self.GM_Y = GaussMarkov(dT, tauY, etaY)
            self.GM_Z = GaussMarkov(dT, tauZ, etaZ)
        self.vX = 0
        self.vY = 0
        self.vZ = 0

        return

    def reset(self):
        self.GM_X.reset()
        self.GM_Y.reset()
        self.GM_Z.reset()
        self.vX = 0
        self.vY = 0
        self.vZ = 0

        return

    def update(self, vXnoise=None, vYnoise=None, vZnoise=None):

        self.Vx = self.GM_X.update(vXnoise)
        self.Vy = self.GM_Y.update(vYnoise)
        self.Vz = self.GM_Z.update(vZnoise)

        return self.Vx, self.Vy, self.Vz

class SensorsModel():
    def __init__(self, aeroModel=VehicleAerodynamicsModel.VehicleAerodynamicsModel(), taugyro=VSC.gyro_tau, etagyro=VSC.gyro_eta, tauGPS=VSC.GPS_tau, etaGPSHorizontal=VSC.GPS_etaHorizontal, etaGPSVertical=VSC.GPS_etaVertical, gpsUpdateHz=VSC.GPS_rate):
        self.aeroModel = aeroModel
        self.dT = aeroModel.VehicleDynamics.dT
        self.taugyro = taugyro
        self.etagyro = etagyro
        self.tauGPS = tauGPS
        self.etaGPSHorizontal = etaGPSHorizontal
        self.etaGPSVertical = etaGPSVertical
        self.gpsUpdateHz = gpsUpdateHz
        self.trueSensors = Sensors.vehicleSensors()
        self.sensorNoisy = Sensors.vehicleSensors()
        self.sensorBiases = self.initializeBiases()
        self.sensorSigmas = self.initializeSigmas()
        self.updateTicks = 0
        self.gpsTickUpdate = 1 / (self.dT * gpsUpdateHz)
        self.gyroGM = GaussMarkovXYZ(self.dT, taugyro, etagyro)
        self.gpsGM = GaussMarkovXYZ(1 / gpsUpdateHz, tauGPS, etaGPSHorizontal, tauGPS, etaGPSHorizontal, tauGPS, etaGPSVertical)
        
        return

    def getSensorsNoisy(self):
        return self.sensorNoisy

    def getSensorsTrue(self):
        return self.trueSensors


    def initializeBiases(self, gyroBias=VSC.gyro_bias, accelBias=VSC.accel_bias, magBias=VSC.mag_bias, baroBias=VSC.baro_bias, pitotBias=VSC.pitot_bias):
        sensorBiases = Sensors.vehicleSensors()

        sensorBiases.gyro_x = gyroBias * random.uniform(-1, 1)
        sensorBiases.gyro_y = gyroBias * random.uniform(-1, 1)
        sensorBiases.gyro_z = gyroBias * random.uniform(-1, 1)
        sensorBiases.accel_x = accelBias * random.uniform(-1, 1)
        sensorBiases.accel_y = accelBias * random.uniform(-1, 1)
        sensorBiases.accel_z = accelBias * random.uniform(-1, 1)
        sensorBiases.mag_x = magBias * random.uniform(-1, 1)
        sensorBiases.mag_y = magBias * random.uniform(-1, 1)
        sensorBiases.mag_z = magBias * random.uniform(-1, 1)
        sensorBiases.baro = baroBias * random.uniform(-1, 1)
        sensorBiases.pitot = pitotBias * random.uniform(-1, 1)
        sensorBiases.gps_sog = 0
        sensorBiases.gps_cog = 0
        sensorBiases.gps_n = 0
        sensorBiases.gps_e = 0
        sensorBiases.gps_alt = 0

        return sensorBiases

    def initializeSigmas(self, gyroSigma=VSC.gyro_sigma, accelSigma=VSC.accel_sigma, magSigma=VSC.mag_sigma, baroSigma=VSC.baro_sigma, pitotSigma=VSC.pitot_sigma, gpsSigmaHorizontal=VSC.GPS_sigmaHorizontal, gpsSigmaVertical=VSC.GPS_sigmaVertical, gpsSigmaSOG=VSC.GPS_sigmaSOG, gpsSigmaCOG=VSC.GPS_sigmaCOG):
        sensorSigmas = Sensors.vehicleSensors()

        sensorSigmas.gyro_x = gyroSigma
        sensorSigmas.gyro_y = gyroSigma
        sensorSigmas.gyro_z = gyroSigma
        sensorSigmas.accel_x = accelSigma
        sensorSigmas.accel_y = accelSigma
        sensorSigmas.accel_z = accelSigma
        sensorSigmas.mag_x = magSigma
        sensorSigmas.mag_y = magSigma
        sensorSigmas.mag_z = magSigma
        sensorSigmas.baro = baroSigma
        sensorSigmas.pitot = pitotSigma
        sensorSigmas.gps_n = gpsSigmaHorizontal
        sensorSigmas.gps_e = gpsSigmaHorizontal
        sensorSigmas.gps_alt = gpsSigmaVertical
        sensorSigmas.gps_sog = gpsSigmaSOG
        sensorSigmas.gps_cog = gpsSigmaCOG

        return sensorSigmas

    def reset(self):
        self.trueSensors = Sensors.vehicleSensors()
        self.sensorNoisy = Sensors.vehicleSensors()
        self.sensorBiases = self.initializeBiases()
        self.sensorSigmas = self.initializeSigmas()
        self.gpsGM.reset()
        self.gyroGM.reset()

        return

    def update(self):
        state = self.aeroModel.VehicleDynamics.state
        dot = self.aeroModel.VehicleDynamics.dot
        self.trueSensors = self.updateSensorsTrue(self.trueSensors, state, dot)
        self.sensorNoisy = self.updateSensorsNoisy(self.trueSensors, self.sensorNoisy, self.sensorBiases, self.sensorSigmas)

        self.updateTicks += 1

        return

    def updateAccelsTrue(self, state, dot):
        #pg122
        accel_x = dot.u + (state.q * state.w) - (state.r * state.v) + (VPC.g0 * math.sin(state.pitch))
        accel_y = dot.v + (state.r * state.u) - (state.p * state.w) - (VPC.g0 * math.cos(state.pitch) * math.sin(state.roll))
        accel_z = dot.w + (state.p * state.v) - (state.q * state.u) - (VPC.g0 * math.cos(state.pitch) * math.cos(state.roll))

        return accel_x, accel_y, accel_z

    def updateGPSTrue(self, state, dot):
        #piazza
        gps_n = state.pn
        gps_e = state.pe
        gps_alt = -state.pd
        gps_sog = math.sqrt((dot.pn)*(dot.pn) + (dot.pe)*(dot.pe))
        gps_cog = math.atan2(dot.pe, dot.pn)
        

        return gps_n, gps_e, gps_alt, gps_sog, gps_cog

    
    def updateGyrosTrue(self, state):
        return state.p, state.q, state.r

    def updateMagsTrue(self, state):
        mags = MatrixMath.multiply(state.R, VSC.magfield)
        mag_x = mags[0][0]
        mag_y = mags[1][0]
        mag_z = mags[2][0]

        return mag_x, mag_y, mag_z

    def updatePressureSensorsTrue(self, state):
        #lecture note
        baro = -(VPC.rho * VPC.g0 * -state.pd) + VSC.Pground
        pitot = (VPC.rho * (state.Va ** 2)) / 2

        return baro, pitot

    def updateSensorsNoisy(self, trueSensors=Sensors.vehicleSensors(), noisySensors=Sensors.vehicleSensors(), sensorBiases=Sensors.vehicleSensors(), sensorSigmas=Sensors.vehicleSensors()):
        sensorNoisyCurrent = Sensors.vehicleSensors()
        #block diagram from lab manual
        GM_X, GM_Y, GM_Z = self.gyroGM.update()
        #Markov
        #Accel
        sensorNoisyCurrent.accel_x = trueSensors.accel_x + sensorBiases.accel_x + sensorSigmas.accel_x
        sensorNoisyCurrent.accel_y = trueSensors.accel_y + sensorBiases.accel_y + sensorSigmas.accel_y
        sensorNoisyCurrent.accel_z = trueSensors.accel_z + sensorBiases.accel_z + sensorSigmas.accel_z
        #Mag
        sensorNoisyCurrent.mag_x = trueSensors.mag_x + sensorBiases.mag_x + sensorSigmas.mag_x
        sensorNoisyCurrent.mag_y = trueSensors.mag_y + sensorBiases.mag_y + sensorSigmas.mag_y
        sensorNoisyCurrent.mag_z = trueSensors.mag_z + sensorBiases.mag_z + sensorSigmas.mag_z
        #gyro
        sensorNoisyCurrent.gyro_x = trueSensors.gyro_x + sensorBiases.gyro_x + GM_X + sensorSigmas.gyro_x
        sensorNoisyCurrent.gyro_y = trueSensors.gyro_y + sensorBiases.gyro_y + GM_Y + sensorSigmas.gyro_y
        sensorNoisyCurrent.gyro_z = trueSensors.gyro_z + sensorBiases.gyro_z + GM_Z + sensorSigmas.gyro_z
  
        #pressure
        sensorNoisyCurrent.baro = trueSensors.baro + sensorBiases.baro
        sensorNoisyCurrent.pitot = trueSensors.pitot + sensorBiases.pitot
        
        #check gps update according to the lab manual 
        # The GPS measurement should only update when the tick counter, updateTicks, is an integer multiple of the update threshold, gpsTickUpdate - lab manual
        if (self.updateTicks % self.gpsTickUpdate == 0):
            gpsBN, gpsBE, gpsALT = self.gpsGM.update()
            sensorNoisyCurrent.gps_n = trueSensors.gps_n + gpsBN + sensorSigmas.gps_n
            sensorNoisyCurrent.gps_e = trueSensors.gps_e + gpsBE + sensorSigmas.gps_e
            sensorNoisyCurrent.gps_alt = trueSensors.gps_alt + gpsALT + sensorSigmas.gps_alt
            sensorNoisyCurrent.gps_sog = trueSensors.gps_sog + sensorSigmas.gps_sog
           #not sure what to put for else: ?
            if (sensorSigmas.gps_sog !=  0):   
                sensorNoisyCurrent.gps_cog = (VPC.InitialSpeed / sensorSigmas.gps_sog)

            if (sensorNoisyCurrent.gps_cog > math.pi):
                sensorNoisyCurrent.gps_cog = math.pi
            elif (sensorNoisyCurrent.gps_cog < math.pi):
                sensorNoisyCurrent.gps_cog = -math.pi

        # Else if not, use previous noisy sensor outputs
        else:
            sensorNoisyCurrent.gps_n = noisySensors.gps_n
            sensorNoisyCurrent.gps_e = noisySensors.gps_e
            sensorNoisyCurrent.gps_alt = noisySensors.gps_alt
            sensorNoisyCurrent.gps_sog = noisySensors.gps_sog
            sensorNoisyCurrent.gps_cog = noisySensors.gps_cog

        return sensorNoisyCurrent

    def updateSensorsTrue(self, prevTrueSensors, state, dot):
        trueSensors = Sensors.vehicleSensors()
        #Accel
        trueSensors.accel_x, trueSensors.accel_y, trueSensors.accel_z = self.updateAccelsTrue(state, dot)
        #Mag
        trueSensors.mag_x, trueSensors.mag_y, trueSensors.mag_z = self.updateMagsTrue(state)
        #gyro
        trueSensors.gyro_x, trueSensors.gyro_y, trueSensors.gyro_z = self.updateGyrosTrue(state)
        trueSensors.baro, trueSensors.pitot = self.updatePressureSensorsTrue(state)

        #check gps update according to the lab manual 
        # The GPS measurement should only update when the tick counter, updateTicks, is an integer multiple of the update threshold, gpsTickUpdate - lab manual
        if (self.updateTicks % self.gpsTickUpdate == 0):
            trueSensors.gps_n, trueSensors.gps_e, trueSensors.gps_alt, trueSensors.gps_sog, trueSensors.gps_cog = self.updateGPSTrue(state, dot)
        else:
            trueSensors.gps_n = prevTrueSensors.gps_n
            trueSensors.gps_e = prevTrueSensors.gps_e
            trueSensors.gps_alt = prevTrueSensors.gps_alt
            trueSensors.gps_sog = prevTrueSensors.gps_sog
            trueSensors.gps_cog = prevTrueSensors.gps_cog

        return trueSensors