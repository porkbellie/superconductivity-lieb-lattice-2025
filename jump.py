import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def detect_phase_jump(phi, cutoff):

    n = length of phi
    phi_smooth = array of length n
    shift = 0

    phi_smooth[0] = phi[0]

    for i from 1 to n - 2:
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