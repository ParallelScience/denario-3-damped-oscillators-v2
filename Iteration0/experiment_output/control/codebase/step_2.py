# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from step_1 import damped_oscillator_model

def analyze_performance():
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    fit_results = np.load("data/fit_results.npy", allow_pickle=True)
    metrics = []
    for res in fit_results:
        osc_id = res['id']
        mask = data['oscillator_id'] == osc_id
        t = data['time'][mask]
        x_obs = data['displacement'][mask]
        popt = res['popt']
        x_fit = damped_oscillator_model(t, *popt)
        residuals = x_obs - x_fit
        snr = np.var(x_fit) / (np.var(residuals) + 1e-12)
        gamma_true = res['ground_truth_gamma']
        omega_true = res['ground_truth_omega']
        gamma_err = np.abs(popt[1] - gamma_true) / (gamma_true + 1e-12)
        omega_err = np.abs(popt[2] - omega_true) / (omega_true + 1e-12)
        damping_ratio = gamma_true / (omega_true + 1e-12)
        metrics.append({'id': osc_id, 'snr': snr, 'gamma_err': gamma_err, 'omega_err': omega_err, 'gamma_std': res['perr'][1], 'omega_std': res['perr'][2], 'damping_ratio': damping_ratio, 'gamma_fit': popt[1], 'gamma_true': gamma_true, 'omega_fit': popt[2], 'omega_true': omega_true})
    print("Performance Metrics Summary:")
    for m in metrics:
        print("ID " + str(m['id']) + ": SNR=" + str(round(m['snr'], 2)) + ", Gamma RelErr=" + str(round(m['gamma_err'], 4)) + ", Omega RelErr=" + str(round(m['omega_err'], 4)))
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].scatter([m['gamma_true'] for m in metrics], [m['gamma_fit'] for m in metrics], c='blue')
    axes[0, 0].plot([0, 0.5], [0, 0.5], 'k--')
    axes[0, 0].set_title("Parity Plot: Gamma")
    axes[0, 0].set_xlabel("True Gamma (1/s)")
    axes[0, 0].set_ylabel("Fitted Gamma (1/s)")
    axes[0, 1].scatter([m['omega_true'] for m in metrics], [m['omega_fit'] for m in metrics], c='red')
    axes[0, 1].plot([0, 5], [0, 5], 'k--')
    axes[0, 1].set_title("Parity Plot: Omega")
    axes[0, 1].set_xlabel("True Omega (rad/s)")
    axes[0, 1].set_ylabel("Fitted Omega (rad/s)")
    axes[1, 0].scatter([m['snr'] for m in metrics], [m['gamma_err'] for m in metrics], c='green')
    axes[1, 0].set_title("Gamma Error vs SNR")
    axes[1, 0].set_xlabel("SNR")
    axes[1, 0].set_ylabel("Relative Error")
    axes[1, 0].set_xscale('log')
    axes[1, 1].scatter([m['damping_ratio'] for m in metrics], [m['gamma_err'] for m in metrics], c='purple')
    axes[1, 1].set_title("Gamma Error vs Damping Ratio")
    axes[1, 1].set_xlabel("Damping Ratio")
    axes[1, 1].set_ylabel("Relative Error")
    plt.tight_layout()
    timestamp = int(time.time())
    plot_path = os.path.join("data", "diagnostic_plots_" + str(timestamp) + ".png")
    plt.savefig(plot_path, dpi=300)
    print("Saved to " + plot_path)

if __name__ == '__main__':
    analyze_performance()