
# Kalman FIlter and Analog
## Introduction :

This program generate result of postprocessing technique used in raw forecast model.


## Requirement:

- Python 3.7.3
- Anaconda 4.7.5 (plotly, numpy, scipy, matplotlib, pandas)

## Reference :

1. PM 2.5 analog forecast and kalman filter post-processing for CMAQ model, 2015
2. Approaches to Adaptive Filtering, 1972
3. Evaluating the Performances of Adaptive Kalman Filter Methods in GPS/INS Integration
4. Adaptive Kalman filtering based on optimal autoregressive predictive model

## File Explanation 

	- AdaptiveKalmanFilter.py - Class that is using Adaptive Kalman Filter by utils.CalKalman.py
					(Contain estimate error noise and observation noise update)

	- KalmanFilter.py - Class that is using ordinary Kalman Filter supported by utils.CalKalman.py.
				(no estimate error noise and observation noise update)

	- [utils]
		- CalAnalog.py (include function to calculate Analog method)
		- CalKalman.py (include function to calculate the variable in Kalman Filter)
		- DateHandler.py (include how to roll date and handle date value)