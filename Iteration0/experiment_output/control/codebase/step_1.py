# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import scipy.optimize as opt
import concurrent.futures
import matplotlib.pyplot as plt
import time
import os

def damped_oscillator_model(t, A, gamma, omega, phi):
    """
    Analytical model for a damped harmonic oscillator.
    
    Args:
        t: Time array (s).
        A: Initial amplitude (m).
        gamma: Damping rate (1/s).
        omega: Angular frequency (rad/s).
        phi: Initial phase (rad).
        
    Returns:
        Displacement array (m).
    """
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi)

def fit_oscillator(osc_data):
    """
    Fits a single oscillator trajectory using non-linear least squares.
    
    Args:
        osc_data: Structured array slice for one oscillator.
        
    Returns:
        Dictionary containing fitted parameters and metadata.
    """
    t = osc_data['time']
    x = osc_data['displacement']
    n = len(t)
    freqs = np.fft.rfftfreq(n, d=(t[1] - t[0]))
    fft_vals = np.abs(np.fft.rfft(x))
    omega_init = 2 * np.pi * freqs[np.argmax(fft_vals[1:]) + 1]
    A_init = np.max(np.abs(x))
    gamma_init = 0.1
    phi_init = 0.0
    p0 = [A_init, gamma_init, omega_init, phi_init]
    bounds = ([0, 0, 0, -np.pi], [np.inf, np.inf, np.inf, np.pi])
    try:
        popt, pcov = opt.curve_fit(damped_oscillator_model, t, x, p0=p0, bounds=bounds, method='trf')
        perr = np.sqrt(np.diag(pcov))
    except Exception:
        popt = [np.nan] * 4
        perr = [np.nan] * 4
    return {'id': osc_data['oscillator_id'][0], 'popt': popt, 'perr': perr, 'ground_truth_gamma': osc_data['damping_coefficient'][0] / (2 * osc_data['mass_kg'][0]), 'ground_truth_omega': osc_data['natural_frequency'][0]}

if __name__ == '__main__':
    data_path = "/home/node/data/damped_oscillators.npy"
    data = np.load(data_path, allow_pickle=False)
    osc_ids = np.unique(data['oscillator_id'])
    osc_list = [data[data['oscillator_id'] == i] for i in osc_ids]
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(fit_oscillator, osc_list))
    np.save("data/fit_results.npy", results)
    print("Parameter estimation complete. Results saved to data/fit_results.npy")
    for res in results:
        print("Oscillator " + str(res['id']) + ": Fitted Gamma=" + str(res['popt'][1]) + ", Fitted Omega=" + str(res['popt'][2]))
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for i, ax in enumerate(axes.flatten()):
        if i < 4:
            res = results[i]
            mask = data['oscillator_id'] == res['id']
            t = data['time'][mask]
            x = data['displacement'][mask]
            ax.plot(t, x, 'k.', alpha=0.3, label='Noisy Data')
            ax.plot(t, damped_oscillator_model(t, *res['popt']), 'r-', label='Fit')
            ax.set_title("Oscillator " + str(res['id']))
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Displacement (m)")
            ax.legend()
    plt.tight_layout()
    timestamp = int(time.time())
    plot_path = os.path.join("data", "fit_summary_1_" + str(timestamp) + ".png")
    plt.savefig(plot_path, dpi=300)
    print(plot_path)