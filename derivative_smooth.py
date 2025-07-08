import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("/Users/elliehan/Downloads/PhaseQ1.0_sheetonly.xlsx", header=None)

omega = df.iloc[:, 0].to_numpy()
phi_smooth = df.iloc[:, 1].to_numpy() 
excel_compare = df.iloc[:, 4].to_numpy() 

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

calc_deriv = derivative_smooth(omega, phi_smooth)

comparison_df = pd.DataFrame({
    'omega': omega,
    'phi_smooth': phi_smooth,
    'Compare to Excel': excel_compare,
    'New Calculations': calc_deriv
})

print(comparison_df.head(10))