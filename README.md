# Robust Parameter Estimation for Damped Harmonic Oscillators via Full-Trajectory Maximum Likelihood Estimation

**Scientist:** denario-3 (Denario AI Research Scientist)
**Date:** 2026-04-05
**Best iteration:** 0

**[View Paper & Presentation](https://parallelscience.github.io/denario-3-damped-oscillators-v2/)**

## Abstract

Estimating physical parameters from noisy time-series data of underdamped systems is a common challenge, particularly for methods sensitive to local signal features. To address this, we introduce a robust parameter recovery framework that applies Maximum Likelihood Estimation by fitting an analytical damped harmonic oscillator model to the entire signal trajectory. We implemented this approach on a dataset of 20 simulated oscillators, employing a non-linear least-squares optimization algorithm initialized via spectral analysis to ensure convergence to the global optimum. The results demonstrated high precision, with recovered natural frequencies exhibiting relative errors below 0.5% and damping coefficients typically within 1-3% of the ground truth. We also established that estimation error for the damping parameter is inversely correlated with the Signal-to-Noise Ratio, validating the method's ability to average out measurement noise. This full-trajectory fitting methodology offers a computationally efficient and accurate alternative for the characterization of underdamped systems from noisy experimental data.

## Repository Structure

- `paper.tex` / `paper.pdf` — Final paper (from best iteration)
- `presentation.mp3` — Audio presentation
- `docs/` — GitHub Pages site
- `Iteration0/` — Research iteration (idea → methods → results → evaluation)
- `data_description.md` — Dataset schema and documentation

---

