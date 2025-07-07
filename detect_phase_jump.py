import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# DETECT_PHASE_JUMP: detects a phase jump and corrects it and returns the smoothed array of phases
# inputs: phi, cutoff
# output: phi_smooth
def detect_phase_jump(phi, cutoff):

    n = len(phi)
    phi_smooth = np.zeros(n)
    shift = 0

    phi_smooth[0] = phi[0]

    for i in range(1,n - 2):
        jump = phi[i] - phi[i - 1]
        if abs(jump) > cutoff:
            slope_before = phi[i] - phi[i - 1]
            slope_after  = phi[i + 1] - phi[i]

            if jump > 0 and abs(slope_after) < abs(slope_before):
                shift = shift - 1
            elif jump < 0 and abs(slope_after) < abs(slope_before):
                shift = shift + 1

        phi_smooth[i] = phi[i] + shift

return phi_smooth

# DERIVATIVE_SMOOTH: takes the derivative of smoothed phases from DETECT_PHASE_JUMP and returns
# inputs: omega, phi_smooth
# output: derivative 
def derivative_smooth(omega, phi_smooth):
    n = len(phi_smooth) # length of phi_smooth
    derivative = np.zeros(n) # array of length n

    derivative[0] = (phi_smooth[1] - phi_smooth[0]) / (omega[1] - omega[0]) # forward diff at start

    for i in range(1, n-1): # central diff
        derivative[i] = (phi_smooth[i + 1] - phi_smooth[i - 1]) / (omega[i + 1] - omega[i - 1])

    derivative[n - 1] = (phi_smooth[n - 1] - phi_smooth[n - 2]) / (omega[n - 1] - omega[n - 2]) # backward diff at end

return derivative
    