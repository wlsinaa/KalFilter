import numpy as np
import math
#Kalman Gain in the Matrix computation. Calculate it at each time
def KalmanGain(error_est,R_k,measure_matrix): # R_k is measure error

    denominator = GetHPHt_k(error_est,measure_matrix) + R_k

    return error_est.dot(measure_matrix.T).dot(np.linalg.inv(denominator))

#Measurement Model
def Measurement(prior_est,measure_matrix):

    return measure_matrix.dot(prior_est)

#Error covariance extrapolation
def ErrorCovUpdate(kalman_gain,measure_matrix,error_est):
    #!!!!!!!!!!!!!!!!!!!!!!!!!! should be modified
    dimention = len(error_est)

    A = np.identity(dimention) - kalman_gain.dot(measure_matrix)

    return A.dot(error_est)

#State estimate observational update
def StateEstUpdate(prior_est,kalman_gain,obs,measure_matrix):

    Hx = measure_matrix.dot(prior_est)

    return prior_est + kalman_gain.dot( obs - Hx)

#Error covariance extrapolation
def ErrorCovExtra( past_posterior_error,state_trans_matrix):

    Ax = state_trans_matrix.dot(past_posterior_error)
    return Ax.dot( state_trans_matrix.T )

#State covariance extrapolation
def StateEstExtra(past_posterior_est,state_trans_matrix):
    
    return state_trans_matrix.dot(past_posterior_est)

# Estimate Error Matrix
def GetErrorEstimate(prior_est,OBS):

    return prior_est - OBS

#(Adaptive)Error covariance extrapolation
def Adt_ErrorCovExtra(past_posterior_error,state_trans_matrix,past_NoiseCov): # Matirix P_k

    Ax = state_trans_matrix.dot(past_posterior_error)

    return np.matmul( Ax, state_trans_matrix.T ) + past_NoiseCov

# average windows
def Getposterior_Cv(V_j):

    length_windows = len(V_j)
    avg_V = 0.0
    for i in range(length_windows):
        value = V_j[i].dot(V_j[i].T)
        avg_V += value
    avg_V = avg_V/float(length_windows)

    return avg_V

def GetHPHt_k(error_est,measure_matrix): #error_est is prior

    HP_k = measure_matrix.dot(error_est)
    HPHt_k  = HP_k.dot(measure_matrix.T)

    return HPHt_k
# Update R_k(posterior) for next prediction (measure cov)
def UpdateR_k(C_v,error_est,measure_matrix):#

    HPHt_k  = GetHPHt_k(error_est,measure_matrix)

    posterior_R_k = C_v + HPHt_k

    return posterior_R_k
# Update matrix Q (noise Cov)
def UpdateQ_k(Cv, KG):
    #alpha is computed in another function
    KG_Cv = KG.dot(Cv)
    Q_k = KG_Cv.dot(KG.T)
    return Q_k

# Calculate alpha k
def Getalpha_k(Cv,posterior_R_k,error_est,measure_matrix):

    numerator = np.trace(Cv + posterior_R_k)
    denominator = GetHPHt_k(error_est,measure_matrix)
    return numerator/denominator