import numpy as np
import scipy as scipy
from utils import CalKalmanF
import random
import matplotlib.pyplot as plt
import time
######################################################################################################################################################
# Author: Sin Wing-Leong
# Reference:
# 1. Evaluating the Performances of Adaptive Kalman Filter Methods inGPS/INS Integration 
# Written in 2019
######################################################################################################################################################

class AKF(object):

    def __init__(self) : 
        None

    #input data(observation) kalman filter and proceed in function process() in this class
    def InputPredictant(self,predictant):

        self.estimate = predictant # predictant is error of the forecast
    
    def InputObservation(self,OBS):

        self.OBS = OBS # Observation

    def InputErrorMeasureCov(self,error_measure_cov): #R_k

        self.error_measure_cov = error_measure_cov

    def InputErrorEstCov(self,error_est_cov): #Q_k

        self.error_est_cov = error_est_cov

    def InputErrorEstimate(self,error_est): 

        self.error_est = error_est
    def InputInno(self,init_inno):
        self.inno = init_inno
    #-------------#
    #As State at t - 1 to State to t is not changed or any transition matrix. Hope that it may be an identity matrix.
    def SetStateTransMatrix (self,state_trans_matrix):

        self.state_trans_matrix = state_trans_matrix

    def SetMeasureTransMatrix (self,measure_trans_matrix):
        
        self.measure_trans_matrix = measure_trans_matrix
    
    # Covariance matching technique
    def SetWindow(self,num):

        self.windows = num

    #-------------#

    # Adaptive Estimation of Innovation Sequences
    def updateInno(self,new_inno):
        old_inno = list(self.inno)
        if len(self.inno) == self.windows:
            old_inno.pop(0)
        old_inno.append(new_inno)
        self.inno = np.array(old_inno)

    def GetNewEstCov(self,KalmanGain): # Q_k is estimate covariance matrix

        Cv = CalKalmanF.Getposterior_Cv(self.inno)
        Q_k = CalKalmanF.UpdateQ_k(Cv,KalmanGain)

        return Q_k

    # Adaption of Q
    def GetNewMeaCov(self): # R_k is measure covariance matrix

        Cv = CalKalmanF.Getposterior_Cv(self.inno)
        R_k = CalKalmanF.UpdateR_k(Cv,self.error_est,self.measure_trans_matrix)

        return R_k
    # Get Kalman Gain
    def GetKalmanGain(self):

        kalman_gain = CalKalmanF.KalmanGain(self.error_est,self.error_measure_cov,self.measure_trans_matrix)

        return kalman_gain

    def EstExtra(self):

        self.estimate = CalKalmanF.StateEstExtra(self.estimate,self.state_trans_matrix)

    def ErrorExtra(self):

        self.error_est = CalKalmanF.Adt_ErrorCovExtra(self.error_est,self.state_trans_matrix,self.error_est_cov)

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
        # Transform x_t-1 to x_t for estimate and estimate error first 


        self.EstExtra()
        self.ErrorExtra()

        # The Update Stage
        kalman_gain, new_est, new_error_est = self.GetUpdateInfo() #new_est is 'preivous estimate' and new_error_est is 'preivous error matrix' in next run

        self.kalman_gain = kalman_gain

        # estimate and error_est are updated and will used in the next run
        self.estimate = new_est

        self.error_est = new_error_est

        # with updated info (Adaptive Estimation of R Based on Residual Sequences)

        v_k = self.OBS - self.measure_trans_matrix.dot(self.estimate) #The residual k v which is the difference between the real observations and its estimated values
        # update residual for updating R and Q

        self.updateInno(v_k)

        # Update R_k
        self.error_measure_cov = self.GetNewMeaCov()
        
        # Update Q_k
        self.error_est_cov = self.GetNewEstCov(kalman_gain)

if __name__ == '__main__':
    #test case
    init_estimate = np.array([[100.0],[100.0]])
    init_error = np.array(np.identity(2)*5.0)
    error_mea = np.array([[5.0]])
    OBS = np.array([[[60.0]],[[10.0]],[[60.0]],[[60.0]],[[66.0]],[[68.0]],[[69.0]],[[63.0]],[[60.0]],[[20.0]],[[30.0]],[[10.0]],[[10.0]],[[10.0]],[[10.0]],[[10.0]],[[10.0]]])
    num = 100
    random.seed(100)
    for k in range(num):
        OBS = list(OBS)
        OBS.append([[random.random()*100.0]])
    for k in range(num):
        OBS = list(OBS)
        OBS.append([[random.random()*50.0]])
    for k in range(num):
        OBS = list(OBS)
        OBS.append([[random.random()*25.0]])
    for k in range(num):
        OBS = list(OBS)
        OBS.append([[random.random()*10.0]])

    OBS = np.array(OBS)
    KalmanFilter = AKF()
    KalmanFilter.InputPredictant(init_estimate)
    KalmanFilter.InputObservation(OBS)
    KalmanFilter.InputErrorMeasureCov(error_mea)
    KalmanFilter.InputErrorEstimate(init_error)
    KalmanFilter.InputErrorEstCov(np.identity(2)*20.0)
    KalmanFilter.InputInno(np.array([[[1.0]]]))
    KalmanFilter.SetStateTransMatrix(np.identity(2))
    KalmanFilter.SetMeasureTransMatrix(np.array([[1.0,2.0]]))
    KalmanFilter.SetWindow(80)
    
    est = []
    for i in range(len(OBS)):

        KalmanFilter.InputPredictant(KalmanFilter.estimate)
        KalmanFilter.InputObservation(OBS[i])
        KalmanFilter.InputErrorMeasureCov(KalmanFilter.error_measure_cov)
        KalmanFilter.InputErrorEstimate(KalmanFilter.error_est)
        KalmanFilter.InputErrorEstCov(KalmanFilter.error_est_cov)
        KalmanFilter.Processing()

        est.append(np.array([[1.0,2.0]]).dot(KalmanFilter.estimate)[0][0])

    x =np.arange(0,len(est),step = 1.0)
    plt.scatter(x,OBS.flatten(),s = 0.2)
    plt.plot(x,est,color = 'r',linewidth = 0.5)
    plt.plot(x,[50.0]*len(x),color = 'k',linewidth = 0.1)
    plt.plot(x,[25.0]*len(x),color = 'k',linewidth = 0.1)
    plt.plot(x,[12.5]*len(x),color = 'k',linewidth = 0.1)
    plt.plot(x,[5.0]*len(x),color = 'k',linewidth = 0.1)
    plt.savefig('C:\\Users\\User\\Desktop\\2016-2018 Data\\graph\\Scatter\\'+ 'test.png',dpi= 300)
    plt.clf()