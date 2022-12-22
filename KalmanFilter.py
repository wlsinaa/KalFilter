import numpy as np
import scipy as scipy
from utils import CalKalmanF

######################################################################################################################################################
# Author: Sin Wing-Leong
# Reference:
# 1. Kalman Filtering: Theory and Practice Using MATLAB, Second Edition (2001) Page 116 - 125
# 2. PM2.5 analog forecast and Kalman filter post-processing for the Community Multiscale Air Quality (CMAQ) Model 
#
# Written in 2019
######################################################################################################################################################

class KF(object):

    def __init__(self) : 
        None

    #input data(observation) kalman filter and proceed in function process() in this class
    def InputPredictant(self,predictant):

        self.estimate = predictant # predictant is error of the forecast
    
    def InputObservation(self,OBS):

        self.OBS = OBS # Observation

    def InputErrorMeasure(self,error_measure):

        self.error_measure = error_measure

    def InputErrorEstimate(self,error_est):

        self.error_est = error_est

    #-------------#
    #As State at t - 1 to State to t is not changed or any transition matrix. Hope that it may be an identity matrix.
    def SetStateTransMatrix (self,state_trans_matrix):

        self.state_trans_matrix = state_trans_matrix

    #As Error at t - 1 to State to t is not changed or any transition matrix. Hope that it may be an identity matrix.
    def SetMeasureTransMatrix (self,measure_trans_matrix):
        
        self.measure_trans_matrix = measure_trans_matrix
    #-------------#

    # Get Kalman Gain
    def GetKalmanGain(self):

        kalman_gain = CalKalmanF.KalmanGain(self.error_est,self.error_measure,self.measure_trans_matrix)

        return kalman_gain

    # Get the updated estimate form kalman_gain and prior_est which is the direct model output
    def GetNewEstimate(self,kalman_gain):

        new_est = CalKalmanF.StateEstUpdate(self.estimate,kalman_gain,self.OBS,self.measure_trans_matrix)
        
        return new_est
    
    # Get updated estimate error matrix
    def GetNewErrorEstimate(self, kalman_gain):

        new_error_est = CalKalmanF.ErrorCovUpdate(kalman_gain,self.measure_trans_matrix,self.error_est)

        return new_error_est

    # Get updated information by the some inputs
    def GetUpdateInfo(self):

        # Get Kalman Gain
        KG = self.GetKalmanGain()

        # Get new estimate
        new_est = self.GetNewEstimate(KG)

        # Get new estimate error
        new_error_est = self.GetNewErrorEstimate(KG)

        return KG, new_est, new_error_est
    
    # Main procedure
    def Processing (self):

        # The Update Stage
        kalman_gain, new_est, new_error_est = self.GetUpdateInfo() #new_est is 'preivous estimate' and new_error_est is 'preivous error matrix' in next run
        
        self.kalman_gain = kalman_gain
        # estimate and error_est are updated and will used in the next run
        self.estimate = new_est
        self.error_est = new_error_est


if __name__ == '__main__':
    #test case
    init_estimate = np.array([[68.0]])
    init_error = np.array([[2.0]])
    error_mea = np.array([[4.0]])
    OBS = np.array([[75.0]])

    KalmanFilter = KF()
    KalmanFilter.InputPredictant(init_estimate)
    KalmanFilter.InputObservation(OBS)
    KalmanFilter.InputErrorMeasure(error_mea)
    KalmanFilter.InputErrorEstimate(init_error)

    KalmanFilter.SetStateTransMatrix(np.identity(1))
    KalmanFilter.SetMeasureTransMatrix(np.identity(1))
    KalmanFilter.Processing()

    print(KalmanFilter.estimate)
    print(KalmanFilter.kalman_gain)
    print(KalmanFilter.error_est)