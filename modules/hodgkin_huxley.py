
import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks

C_m  = 1.0
g_Na = 120.0
g_K  = 36.0
g_L  = 0.3
E_Na = 50.0
E_K  = -77.0
E_L  = -54.4

def alpha_m(V): return 0.1*(V+40)/(1-np.exp(-(V+40)/10)+1e-9)
def beta_m(V):  return 4*np.exp(-(V+65)/18)
def alpha_h(V): return 0.07*np.exp(-(V+65)/20)
def beta_h(V):  return 1/(1+np.exp(-(V+35)/10))
def alpha_n(V): return 0.01*(V+55)/(1-np.exp(-(V+55)/10)+1e-9)
def beta_n(V):  return 0.125*np.exp(-(V+65)/80)

def hodgkin_huxley(t, y, I_ext):
    V, m, h, n = y
    I_Na = g_Na * m**3 * h * (V - E_Na)
    I_K  = g_K  * n**4     * (V - E_K)
    I_L  = g_L             * (V - E_L)
    dVdt = (I_ext - I_Na - I_K - I_L) / C_m
    dmdt = alpha_m(V)*(1-m) - beta_m(V)*m
    dhdt = alpha_h(V)*(1-h) - beta_h(V)*h
    dndt = alpha_n(V)*(1-n) - beta_n(V)*n
    return [dVdt, dmdt, dhdt, dndt]

def simulate(I_ext=10.0, t_max=100.0):
    y0 = [-65.0, 0.05, 0.6, 0.32]
    t_span = (0, t_max)
    t_eval = np.linspace(0, t_max, 5000)
    sol = solve_ivp(
        hodgkin_huxley,
        t_span, y0,
        args=(I_ext,),
        t_eval=t_eval,
        method='RK45',
        rtol=1e-8
    )
    return sol

def get_regime(I_ext):
    sol = simulate(I_ext=I_ext, t_max=300.0)
    V = sol.y[0]
    mask = sol.t > 150
    V_steady = V[mask]
    pks, _ = find_peaks(V_steady, height=0, distance=20)
    n_peaks = len(pks)

    if n_peaks == 0:
        return "Resting state", "#1D9E75"
    elif n_peaks <= 8:
        return "Periodic firing", "#378ADD"
    elif n_peaks <= 20:
        return "Bursting", "#EF9F27"
    else:
        return "High-frequency / chaotic", "#D85A30"

def bifurcation_data(I_range=(0, 50), n_points=80):
    I_values = np.linspace(I_range[0], I_range[1], n_points)
    peaks_I, peaks_V = [], []
    for I in I_values:
        sol = simulate(I_ext=I, t_max=300.0)
        V = sol.y[0]
        mask = sol.t > 150
        V_steady = V[mask]
        pks, _ = find_peaks(V_steady, height=0)
        for p in pks:
            peaks_I.append(I)
            peaks_V.append(V_steady[p])
    return peaks_I, peaks_V

print("✅ Module Hodgkin-Huxley créé")
