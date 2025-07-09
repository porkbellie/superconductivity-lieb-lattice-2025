import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("/Users/elliehan/Downloads/PhaseQ1.0_sheetonly.xlsx", header=None)

omega = df.iloc[:, 0].to_numpy()
phi_smooth = df.iloc[:, 1].to_numpy()
excel_compare = df.iloc[:, 4].to_numpy()

mid_omega = 0.5 * (omega[:-1] + omega[1:])

midpoint_derivative = (phi_smooth[1:] - phi_smooth[:-1]) / (omega[1:] - omega[:-1])

comparison_df = pd.DataFrame({
    "ω midpoint": mid_omega,
    "Excel dϕ/dω": excel_compare[:len(midpoint_derivative)],
    "Python dϕ/dω": midpoint_derivative
})

print(comparison_df.head(10))
