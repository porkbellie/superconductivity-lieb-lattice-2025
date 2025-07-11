import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

df = pd.read_excel("/Users/elliehan/Downloads/PhaseQ1.0_sheetonly.xlsx", header=None)

omega = df.iloc[:, 0].to_numpy()
phi_smooth = df.iloc[:, 1].to_numpy()
excel_compare = df.iloc[:, 4].to_numpy()

# reproduce excel values
mid_omega = 0.5 * (omega[:-1] + omega[1:])
mid_derivative = (phi_smooth[1:] - phi_smooth[:-1]) / (omega[1:] - omega[:-1])

# SMOOTH_DERIVATIVE: computes smoothed numerical derivative of phases while preserving delta functions 
# inputs: omega, phi_smooth, cutoff
# outputs: derivative
def smooth_derivative(omega, phi_smooth, cutoff=10):
    n = len(phi_smooth)
    derivative = np.zeros(n)

    derivative[0] = (phi_smooth[1] - phi_smooth[0]) / (omega[1] - omega[0])

    for i in range(1, n - 1):
        forward = abs(phi_smooth[i + 1] - phi_smooth[i])
        backward = abs(phi_smooth[i] - phi_smooth[i - 1])

        if forward < cutoff and backward < cutoff:
            derivative[i] = (phi_smooth[i + 1] - phi_smooth[i - 1]) / (omega[i + 1] - omega[i - 1])
        else:
            derivative[i] = (phi_smooth[i] - phi_smooth[i - 1]) / (omega[i] - omega[i - 1])

    derivative[n - 1] = (phi_smooth[n - 1] - phi_smooth[n - 2]) / (omega[n - 1] - omega[n - 2])

    return derivative

smooth_deriv = smooth_derivative(omega, phi_smooth)

smooth_mid = 0.5 * (omega[1:] + omega[:-1])
smooth_deriv_mid = 0.5 * (smooth_deriv[1:] + smooth_deriv[:-1])

comparison_df = pd.DataFrame({
    "omegas midpoint": mid_omega,
    "excel values": excel_compare[:len(mid_omega)],
    "midpoint diff": mid_derivative,
    "smooth diff": smooth_deriv_mid
})

print(comparison_df.head(10))

# Savitsky-Golay filter
window_length = 11
polyorder = 3
delta = np.mean(np.diff(omega))
savgol_derivative = savgol_filter(phi_smooth, window_length, polyorder, deriv=1, delta=delta)

# adaptive S-G filter
def adaptive_savgol_derivative(omega, phi, base_window=11, polyorder=3, jump_cutoff=10):
    n = len(phi)
    deriv = np.zeros(n)

    for i in range(n):
        if i == 0 or i == n - 1:
            deriv[i] = (phi[min(i + 1, n - 1)] - phi[max(i - 1, 0)]) / (omega[min(i + 1, n - 1)] - omega[max(i - 1, 0)])
            continue

        jump_fwd = abs(phi[min(i + 1, n - 1)] - phi[i])
        jump_bwd = abs(phi[i] - phi[max(i - 1, 0)])
        jump_size = max(jump_fwd, jump_bwd)

        if jump_size > jump_cutoff:
            window = max(5, base_window // 3)
        else:
            window = base_window

        window = min(window, i, n - i - 1)
        if window % 2 == 0:
            window -= 1
        if window < polyorder + 2:
            window = polyorder + 2
            if window % 2 == 0:
                window += 1

        half = window // 2
        start = max(0, i - half)
        end = min(n, i + half + 1)

        if end - start < window:
            deriv[i] = (phi[i] - phi[i - 1]) / (omega[i] - omega[i - 1])
            continue

        local_phi = phi[start:end]
        local_omega = omega[start:end]
        delta = np.mean(np.diff(local_omega))
        try:
            local_deriv = savgol_filter(local_phi, window_length=len(local_phi), polyorder=polyorder, deriv=1, delta=delta)
            deriv[i] = local_deriv[i - start]
        except Exception:
            deriv[i] = (phi[i] - phi[i - 1]) / (omega[i] - omega[i - 1])

    return deriv

adaptive_deriv = adaptive_savgol_derivative(omega, phi_smooth)

plt.figure(figsize=(10, 5))
plt.plot(mid_omega, mid_derivative, label="excel", linewidth=2)
plt.plot(mid_omega, smooth_deriv_mid, label="smooth_derivative", linewidth=2)
#plt.plot(omega, savgol_derivative, label="Savitsky-Golay", linewidth=2)
plt.plot(omega, adaptive_deriv, label="adaptive S-G", linewidth=2)
plt.title("Smoothing Comparison")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xlim(-4,4)
plt.ylim(-5,10) 
plt.show()
