# superconductivity-lieb-lattice-2025
## Ellie Han, Peter Riseborough
### Description

Project updates solely from 2025

##### detect_phase_jump

An algorithm to detect abrupt jumps and use a comparison of slopes locally to determine whether the jump should be corrected by adding or subtracting 1. The idea is that if phi jumps up or down but then flattens out, then a shift will be applied to the current point. I excluded the endpoints from the loop for out of bounds reasons. There are two inputs: phi and cutoff. Phi is an array, and the cutoff is the threshold for determining the jumps. It should return an array of smoothed phi values.

Intended for easy translation into Fortran