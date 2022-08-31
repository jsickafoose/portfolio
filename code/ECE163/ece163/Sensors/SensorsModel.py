import math
import random
from ece163.Modeling import VehicleAerodynamicsModel
from ece163.Utilities import MatrixMath as mm
from ..Containers import Sensors
from ..Constants import VehiclePhysicalConstants as VPC
from ..Constants import VehicleSensorConstants as VSC
from ..Modeling import VehicleAerodynamicsModel


class GaussMarkov:
    '''
    Function to initialize the GaussMarkov code that generates the exponentially
    correlated noise which is used for the slowly varying bias drift of the
    gyros as well as the GPS position. Implements the noise model characterized
    by a first order Gauss-Markov process: dv/dt = -1/tau v + w, where w is a
    white noise process with N(0,sigma).

    Parameters: dT – time step [s]
                tau – correlation time [s]
                sigma – standard deviation of white noise process

    Returns:    None
    '''
    def __init__(self, dT=0.01, tau=1000000.0, eta=0.0):
        self.dT = dT
        self.tau = tau
        self.eta = eta # Sigma value

        self.v = 0



    '''
    Wrapper function that resets the GaussMarkov model

    Parameters: None

    Returns:    None
    '''
    def reset(self):
        self.dT = 0.01
        self.tau = 1000000.0
        self.eta = 0.0 # Sigma value

        self.v = 0



    '''
    Function that updates the Gauss-Markov process, and returns the updated
    value (as well as updating the internal value that holds until the next
    call of the function

    Parameters: vnoise – optional parameter to drive the function with a known
                         value. If None, then use random.gauss(0,sigma(eta))

    Returns:    v - new noise value (also updated internally)
    '''
    def update(self, vnoise=None):
        if vnoise is None:
            vnoise = random.gauss(0, self.eta) #vnoise = eta, eta is sigma
        
        self.v = math.exp(-self.dT/self.tau)*self.v + vnoise
        return self.v



class GaussMarkovXYZ:
    '''
    Function to aggregate three Gauss-Markov models into a triplet that
    returns the X, Y, and Z axes of the time-varying drift; if (tau, eta)
    are None, then will default to the same values for each model.

    Parameters: dT – time step [s]
                tau – correlation time [s]
                sigma – standard deviation of white noise process

    Returns:    None
    '''
    def __init__(self, dT=0.01, tauX=1000000.0, etaX=0.0, tauY=None, etaY=None, tauZ=None, etaZ=None):
        self.X = GaussMarkov(dT, tauX, etaX)    # X will always use the X values
        if tauY is None:                        # If Y values are none, Y and Z use X values
            self.Y = GaussMarkov(dT, tauX, etaX)
            self.Z = GaussMarkov(dT, tauX, etaX)
        elif tauZ is None:                      # If Z is none but Y isn't, both use Y values
            self.Y = GaussMarkov(dT, tauY, etaY)
            self.Z = GaussMarkov(dT, tauY, etaY)
        else:                                   # If neither Y nor Z is none, uses their own values
            self.Y = GaussMarkov(dT, tauY, etaY)
            self.Z = GaussMarkov(dT, tauZ, etaZ)



    '''
    Wrapper function that resets the GaussMarkovXYZ models

    Parameters: None

    Returns:    None
    '''
    def reset(self):
        ## Just resets all values to the default for X
        self.X.reset()
        self.Y.reset()
        self.Z.reset()



    '''
    Function that updates the Gauss-Markov processes, and returns the
    updated values (as well as updating the internal values that holds
    until the next call of the function.

    Parameters: vXnoise – optional parameter to drive the X function with a known value.
                          If None, then use random.gauss(0,sigma)
                vYnoise – optional parameter to drive the Y function with a known value.
                          If None, then use random.gauss(0,sigma)
                vZnoise – optional parameter to drive the Z function with a known value.
                          If None, then use random.gauss(0,sigma)

    Returns:    vX, vY, vZ - new noise values for each axis (also updated internally)
    '''
    def update(self, vXnoise=None, vYnoise=None, vZnoise=None):
        self.X.update(vXnoise)
        self.Y.update(vYnoise)
        self.Z.update(vZnoise)
        return self.X.v, self.Y.v, self.Z.v



class SensorsModel:
    '''
    Function to initialize the SensorsModel code. Will contain both the
    true sensors outputs and the noisy sensor outputs using the noise
    and biases found in the Constants.VehicleSensorConstants file.
    Biases for the sensors are set at instantiation and not updated
    further during the code run. All sensor outputs are in Engineering
    Units (it is assumed that the raw ADC counts to engineering unit
    scaling has already been done). Note that if the biases are set to
    None at instantiation, then they will be set to random values using
    uniform distribution with the appropriate bias scaling from the sensors
    constants. SensorsModel class keeps the Gauss-Markov models for gyro
    biases and GPS.

    Parameters: aeroModel – handle to the VehicleAerodynamicsModel class
                taugyro – Gauss-Markov time constant for gyros [s]
                etagyro – Gauss-Markov process noise standard deviation [rad/s]
                tauGPS – Gauss-Markov time constant for GPS [s]
                etaGPSHorizontal – Gauss-Markov process noise standard deviation [m]
                etaGPSVertical – Gauss-Markov process noise standard deviation [m]
                gpsUpdateHz – Update rate for GPS measurements [Hz]

    Returns:    None
    '''
    def __init__(self, aeroModel=VehicleAerodynamicsModel.VehicleAerodynamicsModel(), taugyro=400.0, etagyro=0.0012740903539558606, tauGPS=1100.0, etaGPSHorizontal=0.21, etaGPSVertical=0.4, gpsUpdateHz=1.0):
        ## Keeps track of AeroModel object
        self.aeroModel = aeroModel

        ## Inits the threshold, and update ticks
        self.dT = self.aeroModel.VDM.dT
        self.updateTicks = 0
        self.threshold = int(gpsUpdateHz/self.dT)

        ## Inits the GaussMarkov bias
        self.gpsGM  = GaussMarkovXYZ(self.dT, tauGPS, etaGPSHorizontal)
        self.gyroGM = GaussMarkovXYZ(self.dT, taugyro, etagyro)

        ## I'm not sure if we need to store these yet
        self.taugyro = taugyro
        self.etagyro = etagyro
        self.tauGPS = tauGPS
        self.etaGPSHorizontal = etaGPSHorizontal
        self.etaGPSVertical = etaGPSVertical
        self.gpsUpdateHz = gpsUpdateHz

        ## Inits the 4 vehicleSensor classes
        self.sensorsBiases = self.initializeBiases(VSC.gyro_bias, VSC.accel_bias, VSC.mag_bias, VSC.baro_bias, VSC.pitot_bias)
        self.sensorsSigmas = self.initializeSigmas(etagyro, VSC.accel_sigma, VSC.mag_sigma, VSC.baro_sigma, VSC.pitot_sigma, etaGPSHorizontal, etaGPSVertical, VSC.GPS_sigmaSOG, VSC.GPS_sigmaCOG)
        self.sensorsTrue  = Sensors.vehicleSensors()
        self.sensorsNoisy = Sensors.vehicleSensors()



    '''
    Function to reset the module to run again. Should reset the Gauss-Markov
    models, re-initialize the sensor biases, and reset the sensors true and
    noisy to pristine conditions

    Parameters: None

    Returns:    None
    '''
    def reset(self):
        self.taugyro = VSC.gyro_tau
        self.etagyro = VSC.gyro_eta
        self.tauGPS = VSC.GPS_tau
        self.etaGPSHorizontal = VSC.GPS_sigmaHorizontal
        self.etaGPSVertical = VSC.GPS_sigmaVertical
        self.gpsUpdateHz = 1.0

        ## Inits the threshold, and update ticks
        self.dT = self.aeroModel.VDM.dT
        self.updateTicks = 0
        self.threshold = int(self.gpsUpdateHz/self.dT)

        ## Inits the GaussMarkov bias
        self.gpsGM  = GaussMarkovXYZ(self.dT, self.tauGPS, self.etaGPSHorizontal, self.tauGPS, self.etaGPSHorizontal, self.tauGPS, self.etaGPSVertical)
        self.gyroGM = GaussMarkovXYZ(self.dT, self.taugyro, self.etagyro)

        ## Inits the 4 vehicleSensor classes
        self.sensorsBiases = self.initializeBiases(VSC.gyro_bias, VSC.accel_bias, VSC.mag_bias, VSC.baro_bias, VSC.pitot_bias)
        self.sensorsSigmas = self.initializeSigmas(self.etagyro, VSC.accel_sigma, VSC.mag_sigma, VSC.baro_sigma, VSC.pitot_sigma, self.etaGPSHorizontal, self.etaGPSVertical, VSC.GPS_sigmaSOG, VSC.GPS_sigmaCOG)
        self.sensorsTrue  = Sensors.vehicleSensors()
        self.sensorsNoisy = Sensors.vehicleSensors()



    '''
    Function to generate the biases for each of the sensors. Biases
    are set with a uniform random number from -1 to 1 that is then
    multiplied by the sigma_bias. The biases for all sensors is returned
    as a Sensors.vehicleSensors class. Note that GPS is an unbiased
    sensor (though noisy), thus all the GPS biases are set to 0.0

    Parameters: gyroBias – bias scaling for the gyros [rad/s]
                accelBias – bias scaling for the accelerometers [m/s^2]
                magBias – bias scaling for the magnetometers [nT]
                baroBias – bias scaling for the barometer [N/m^2]
                pitotBias – bias scaling for the pitot tube [N/m^2]

    Returns:    sensorBiases - class Sensors.vehicleSensors
    '''
    def initializeBiases(self, gyroBias=0.08726646259971647, accelBias=0.9810000000000001, magBias=500.0, baroBias=100.0, pitotBias=20.0):
        out = Sensors.vehicleSensors()
        # gyros
        out.gyro_x = random.uniform(-gyroBias, gyroBias)
        out.gyro_y = random.uniform(-gyroBias, gyroBias)
        out.gyro_z = random.uniform(-gyroBias, gyroBias)
        # accelerometers
        out.accel_x = random.uniform(-accelBias, accelBias)
        out.accel_y = random.uniform(-accelBias, accelBias)
        out.accel_z = random.uniform(-accelBias, accelBias)
        # magnetometers
        out.mag_x = random.uniform(-magBias, magBias)
        out.mag_y = random.uniform(-magBias, magBias)
        out.mag_z = random.uniform(-magBias, magBias)
        # pressure sensors
        out.baro = random.uniform(-baroBias, baroBias)
        out.pitot = random.uniform(-pitotBias, pitotBias)

        return out



    '''
    Function to gather all of the white noise standard deviations into
    a single vehicleSensor class object. These will be used as the input
    to generating the white noise added to each sensor when generating
    the noisy sensor data.

    Parameters: gyroSigma – gyro white noise [rad/s]
                accelSigma – accelerometer white noise [m/s^2]
                magSigma – magnetometer white noise [nT]
                baroSigma – barometer white noise [N/m]
                pitotSigma – airspeed white noise [N/m]
                gpsSigmaHorizontal – GPS horizontal white noise [m]
                gpsSigmaVertical – GPS vertical white noise [m]
                gpsSigmaSOG – GPS Speed over ground white noise [m/s]
                gpsSigmaCOG – GPS Course over ground white noise, nominal [rad]

    Returns:    sensorSigmas - class Sensors.vehicleSensors
    '''
    def initializeSigmas(self, gyroSigma=0.002617993877991494, accelSigma=0.24525000000000002, magSigma=25.0, baroSigma=10.0, pitotSigma=2.0, gpsSigmaHorizontal=0.4, gpsSigmaVertical=0.7, gpsSigmaSOG=0.05, gpsSigmaCOG=0.002):
        out = Sensors.vehicleSensors()
        # gyros
        out.gyro_x = gyroSigma
        out.gyro_y = gyroSigma
        out.gyro_z = gyroSigma
        # accelerometers
        out.accel_x = accelSigma
        out.accel_y = accelSigma
        out.accel_z = accelSigma
        # magnetometers
        out.mag_x = magSigma
        out.mag_y = magSigma
        out.mag_z = magSigma
        # pressure sensors
        out.baro = baroSigma
        out.pitot = pitotSigma
        # gps
        out.gps_n = gpsSigmaHorizontal
        out.gps_e = gpsSigmaHorizontal
        out.gps_alt = gpsSigmaVertical
        out.gps_sog = gpsSigmaSOG
        out.gps_cog = gpsSigmaCOG

        return out



    '''
    Function to update the GPS sensor state (this will be called
    to update the GPS data from the state and the derivative) at
    the required rate. Note that GPS reports back altitude as + above
    mean sea level.

    Parameters: state – class States.vehicleState, currect vehicle state
                dot – class States.vehicleState, current state derivative

    Returns:    gps_n - [North - m]
                gps_e - [East - m]
                gps_alt - [Altitude - m]
                gps_SOG - [Speed over ground, m/s]
                gps_COG - [Course over ground,rad]
    '''
    def updateGPSTrue(self, state, dot):
        gps_n   = state.pn
        gps_e   = state.pe
        gps_alt = -state.pd
        gps_SOG = math.sqrt(dot.pn**2 + dot.pe**2)
        gps_COG = math.atan2(dot.pe, dot.pn)

        return gps_n, gps_e, gps_alt, gps_SOG, gps_COG




    '''
    Function to update the accelerometer sensor. Will be called within
    the updateSensors functions.

    Parameters: state – class States.vehicleState, current vehicle state
                dot – class States.vehicleState, current state derivative

    Returns:    accel_x, accel_y, accel_z, body frame specific force [m/s^2]
    '''
    def updateAccelsTrue(self, state, dot):
        accel_x = dot.u + state.q*state.w - state.r*state.v + VPC.g0*math.sin(state.pitch)
        accel_y = dot.v + state.r*state.u - state.p*state.w - VPC.g0*math.cos(state.pitch)*math.sin(state.roll)
        accel_z = dot.w + state.p*state.v - state.q*state.u - VPC.g0*math.cos(state.pitch)*math.cos(state.roll)
        
        return accel_x, accel_y, accel_z



    '''
    Function to update the magnetometer sensor. Will be called within
    the updateSensors functions.

    Parameters: state – class States.vehicleState, current vehicle state

    Returns:    mag_x, mag_y, mag_z - body frame magnetic field [nT]
    '''
    def updateMagsTrue(self, state):
        mag = mm.multiply(state.R, VSC.magfield)

        return mag[0][0], mag[1][0], mag[2][0]



    '''
    Function to update the rate gyro sensor. Will be called within the
    updateSensors functions.

    Parameters: class States.vehicleState - current vehicle state

    Returns:    gyro_x, gyro_y, gyro_z - body frame rotation rates [rad/s]
    '''
    def updateGyrosTrue(self, state):
        return state.p, state.q, state.r



    '''
    Function to update the pressure sensors onboard the aircraft. Will
    be called within the updateSensors functions. The two pressure sensors
    are static pressure (barometer) and dynamic pressure (pitot tube).
    The barometric pressure is references off of the ground static pressure
    in VehicleSensorConstants at Pground.

    Parameters: state – class States.vehicleState, current vehicle state

    Returns:    baro
                pitot in [N/m^2]
    '''
    def updatePressureSensorsTrue(self, state):
        return (-VPC.rho*VPC.g0*-state.pd + VSC.Pground), ((VPC.rho*state.Va**2)/2)



    '''
    Function to generate the true sensors given the current state and
    state derivative. Sensor suite is 3-axis accelerometer, 3-axis
    rate gyros, 3-axis magnetometers, a barometric altimeter, a pitot
    airspeed, and GPS with an update rate specified in the
    VehicleSensorConstants file. For the GPS update, the previous value
    is returned until a new update occurs. Previous value is contained
    within prevTrueSensors.

    Parameters: prevTrueSensors – class Sensors.vehicleSensors(), previous true sensor readings (no noise)
                state – class States.vehicleState, current vehicle state
                dot – class States.vehicleState, current state derivative

    Returns:    Sensors.vehicleSensors class - true sensor outputs (no noise, no biases)
    '''
    def updateSensorsTrue(self, prevTrueSensors, state, dot):
        out = Sensors.vehicleSensors()
        if (self.updateTicks % self.threshold) != 0:
            out.gps_n   = prevTrueSensors.gps_n
            out.gps_e   = prevTrueSensors.gps_e
            out.gps_alt = prevTrueSensors.gps_alt
            out.gps_sog = prevTrueSensors.gps_sog
            out.gps_cog = prevTrueSensors.gps_cog
        else:
            out.gps_n, out.gps_e, out.gps_alt, out.gps_sog, out.gps_cog = self.updateGPSTrue(state, dot)
        
        out.accel_x, out.accel_y, out.accel_z = self.updateAccelsTrue(state, dot)
        out.mag_x, out.mag_y, out.mag_z = self.updateMagsTrue(state)
        out.gyro_x, out.gyro_y, out.gyro_z = self.updateGyrosTrue(state)
        out.baro, out.pitot = self.updatePressureSensorsTrue(state)

        return out



    '''
    Function to generate the noisy sensor data given the true sensor readings,
    the biases, and the sigmas for the white noise on each sensor. The gauss
    markov models for the gyro biases and GPS positions are updated here. The
    GPS COG white noise must be scaled by the ratio of
    VPC.initialSpeed / actual ground speed. GPS is only updated if the correct
    number of ticks have gone by to indicate that a new GPS measurement should
    be generated. The GPS COG must be limited to within +/- PI. If no GPS
    update has occurred, then the values for the GPS sensors should be copied
    from the noisySensors input to the output.

    Parameters: trueSensors – Sensors.vehicleSensors class, true values (no noise)
                noisySensors – Sensors.vehicleSensors class, previous noisy sensor values
                sensorBiases – Sensors.vehicleSensors class, fixed biases for each sensor
                sensorSigmas – Sensors.vehicleSensors class, standard deviations of white noise on each sensor

    Returns:    Sensors.vehicleSensors class - noisy sensor data
    '''
    def updateSensorsNoisy(self, trueSensors=Sensors.vehicleSensors(gyro_x=0.0, gyro_y=0.0, gyro_z=0.0, accel_x=0.0, accel_y=0.0, accel_z=0.0, mag_x=0.0, mag_y=0.0, mag_z=0.0, baro=0.0, pitot=0.0, gps_n=0.0, gps_e=0.0, gps_alt=0.0, gps_sog=0.0, gps_cog=0.0), noisySensors=Sensors.vehicleSensors(gyro_x=0.0, gyro_y=0.0, gyro_z=0.0, accel_x=0.0, accel_y=0.0, accel_z=0.0, mag_x=0.0, mag_y=0.0, mag_z=0.0, baro=0.0, pitot=0.0, gps_n=0.0, gps_e=0.0, gps_alt=0.0, gps_sog=0.0, gps_cog=0.0), sensorBiases=Sensors.vehicleSensors(gyro_x=0.0, gyro_y=0.0, gyro_z=0.0, accel_x=0.0, accel_y=0.0, accel_z=0.0, mag_x=0.0, mag_y=0.0, mag_z=0.0, baro=0.0, pitot=0.0, gps_n=0.0, gps_e=0.0, gps_alt=0.0, gps_sog=0.0, gps_cog=0.0), sensorSigmas=Sensors.vehicleSensors(gyro_x=0.0, gyro_y=0.0, gyro_z=0.0, accel_x=0.0, accel_y=0.0, accel_z=0.0, mag_x=0.0, mag_y=0.0, mag_z=0.0, baro=0.0, pitot=0.0, gps_n=0.0, gps_e=0.0, gps_alt=0.0, gps_sog=0.0, gps_cog=0.0)):
        ## Starts by generating gaussian noise
        gpsGM_x, gpsGM_y, gpsGM_z = self.gpsGM.update()
        gyroGM_x, gyroGM_y, gyroGM_z = self.gyroGM.update()

        # Makes sure it's a change GPS tick first
        out = Sensors.vehicleSensors()
        if (self.updateTicks % self.threshold) != 0:
            out.gps_n   = noisySensors.gps_n
            out.gps_e   = noisySensors.gps_e
            out.gps_alt = noisySensors.gps_alt
            out.gps_sog = noisySensors.gps_sog
            out.gps_cog = noisySensors.gps_cog
        else:
            out.gps_n   = trueSensors.gps_n   + gpsGM_x + sensorSigmas.gps_n
            out.gps_e   = trueSensors.gps_e   + gpsGM_y + sensorSigmas.gps_e
            out.gps_alt = trueSensors.gps_alt + gpsGM_z + sensorSigmas.gps_alt
            out.gps_sog = trueSensors.gps_sog + sensorSigmas.gps_sog
            out.gps_cog = trueSensors.gps_cog + sensorSigmas.gps_cog
            if out.gps_cog > math.pi:
                out.gps_cog = math.pi
            elif out.gps_cog < -math.pi:
                out.gps_cog = -math.pi

        ## Adds static biases(b0 - random.uniform(-1,1)), drifting biases(bw - random.gauss()), and gaussian noise(bt - keep )
        out.gyro_x  = trueSensors.gyro_x + sensorBiases.gyro_x + sensorSigmas.gyro_x + gyroGM_x
        out.gyro_y  = trueSensors.gyro_y + sensorBiases.gyro_y + sensorSigmas.gyro_y + gyroGM_y
        out.gyro_z  = trueSensors.gyro_z + sensorBiases.gyro_z + sensorSigmas.gyro_z + gyroGM_z
        
        out.accel_x = trueSensors.accel_x + sensorBiases.accel_x + sensorSigmas.accel_x
        out.accel_y = trueSensors.accel_y + sensorBiases.accel_y + sensorSigmas.accel_y
        out.accel_z = trueSensors.accel_z + sensorBiases.accel_z + sensorSigmas.accel_z
        
        out.mag_x   = trueSensors.mag_x + sensorBiases.mag_x + sensorSigmas.mag_x
        out.mag_y   = trueSensors.mag_y + sensorBiases.mag_y + sensorSigmas.mag_y
        out.mag_z   = trueSensors.mag_z + sensorBiases.mag_z + sensorSigmas.mag_z
        
        out.baro    = trueSensors.baro  + sensorBiases.baro
        out.pitot   = trueSensors.pitot + sensorBiases.pitot

        return out



    '''
    Wrapper function to update the Sensors (both true and noisy) using the
    state and dot held within the self.AeroModel. Note that we are passing
    in a handle to the class for this so we don’t have to explicitly use
    getters from the VehicleAerodynamics model. Sensors states are updated
    internally within self.

    Parameters: None

    Returns:    None
    '''
    def update(self):
        ++self.updateTicks
        self.sensorsTrue  = self.updateSensorsTrue(self.sensorsTrue, self.aeroModel.VDM.state, self.aeroModel.VDM.dot)
        self.sensorsNoisy = self.updateSensorsNoisy(self.sensorsTrue, self.sensorsNoisy, self.sensorsBiases, self.sensorsSigmas)



    '''
    Wrapper function to return the true sensor values

    Parameters: None

    Returns:    Sensors.vehicleSensors class - true sensor values
    '''
    def getSensorsTrue(self):
        return self.sensorsTrue



    '''
    Wrapper function to return the noisy sensor values

    Parameters: None

    Returns:    Sensors.vehicleSensors class - noisy sensor data
    '''
    def getSensorsNoisy(self):
        return self.sensorsNoisy