# superconductivity-lieb-lattice-2025
Ellie Han, Peter Riseborough

## Description

Project updates solely from 2025

### detect_phase_jump

A short Python algorithm to detect abrupt jumps and use a comparison of slopes locally to determine whether the jump should be corrected by adding or subtracting 1. The idea is that if phi jumps up or down but then flattens out, then a shift will be applied to the current point. I excluded the endpoints from the loop for out of bounds reasons. There are two inputs: phi and cutoff. Phi is an array, and the cutoff is the threshold for determining the jumps. It should return an array of smoothed phi values.

Intended for easy translation into Fortran

#### 2025.06.30 

Potential flaw occurs when the slopes are equal which is possible when w=0

Next steps: take derivative of smooth parts of curve to give change in DOS due to the interaction, compare to approximated interval midpoint derivative (but should be smoother), avoid removing the delta funtions

You can see the two delta functions outside the continuum straddling w=3, and the delta function of weight -2 at w=0. This corresponds to the destruction of two flat band states at w=0.

The change in the density of states also exhibits delta functions associated with the steps in the non-interacting density of states at w==/-1 and w=+/- 2. The jumps in the non-interacting density of states can be considered as the edges of sub-bands, in which case one is removing states from the edge of the sub-band and pushing them outside the sub-band.

### smooth_derivative

An algorithm that inputs the array phi_smooth from detect_phase_jump and returns the derivative of the smooth parts of the curve without removing the delta functions. There are three inputs: omega, phi_smooth, cutoff. It returns the derivatives as an array. 

This file contains a comparison of smoothing methods. The unsmoothed is produced by a simple numerical diffentiation approximation using the smoothed phi values. The first smoothed is produced by the smooth_derivative function. The second is produced by implementing a Savitzkey-Golay filter. This digital filter uses the method of least linear squares to fit adjacent clusters of data points to a low degree polynomial which means that it is able to smooth while preserving features like the delta functions. It's mostly used to smooth out noisy data in signal processing or spectroscopy, but I thought it might work here too. This is included in the SciPy package. Its source code can be found there.

I found that the Savitzky-Golay filter is smoother than the algorithm I wrote, but I think mine is still a good approximation.