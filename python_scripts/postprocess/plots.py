import os
import sys
sys.path.append(os.path.join(os.getcwd(), "python_scripts"))

import numpy as np
import matplotlib as mpl
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from utilities import *
import similarity_law as slw
from scipy.optimize import curve_fit

RESULTS_DIR = os.path.join(os.getcwd(), "results")
plt.rcParams.update({'font.size': 20})

SFOC = 0.2 #kg/kWh
ECF_CO2 = 3.2 #kg /kg
ECF_CH4 = 0.03 * 10 ** -3

def read_pickle_data(filepath):
    with open(filepath, "rb") as f:
        data = pickle.load(f)
    return data

def roughness_function_vs_Re():
    kp = np.linspace(0, 100, 1000)
    DeltaUp = get_DeltaUp1(kp, KAPPA)
    plt.plot(kp, DeltaUp, lw = 3, color="black")
    plt.xlabel(r"$k^+$")
    plt.ylabel(r"$\Delta U^+$")
    plt.xscale("log")
    plt.xlim(left=0.1)
    plt.grid()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "deltaup_k.pdf"))
    plt.show()

def largeFlatPlate_cf():
    filepath = os.path.join(RESULTS_DIR, "largeFlatPlate.pkl")
    CFD_data = read_pickle_data(filepath)
    CFD_Ks, CFD_Cf = CFD_data["Ks"], CFD_data["Cf"]
    
    L = 230
    SL_Ks = np.arange(0, 450, 50)/10 ** 6
    SL_Cf = slw.main(CFD_data.loc[0, "U"], L, SL_Ks)
    # kp = get_kp(SL_Ks, get_ut_from_CF(CFD_data.loc[0, "U"], SL_Cf), NU)
    plt.plot(CFD_Ks*10**6, CFD_Cf*1000, "s-", color = "black", lw=2.5, label = "CFD")
    plt.plot(SL_Ks*10**6, SL_Cf*1000, "d--", color = "gray", lw = 2.5, label ="SL")
    plt.xlabel(r"$k\,[\mathrm{\mu m}]$")
    plt.ylabel(r"$C_F\times10^3$")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "largeFlatPlate.pdf"))
    plt.show()

def lahoFlatPlate_cf():
    filepath = os.path.join(RESULTS_DIR, "lahoFlatPlate.pkl")
    CFD_data = read_pickle_data(filepath)
    CFD_Ks, CFD_Cf = CFD_data["Ks"], CFD_data["Cf"]
    L = 37

    plt.figure(figsize=(10, 8))

    colors = plt.get_cmap('Grays_r')(np.linspace(0,1, len(np.unique(CFD_data["U"])) + 2))
    for i, u in enumerate(np.unique(CFD_data["U"])):
        Ks = CFD_Ks[CFD_data["U"] == u]
        Cf = CFD_Cf[CFD_data["U"] == u]
        # kp = get_kp(Ks, get_ut_from_CF(u, Cf), NU)
        # print(kp)
        SL_Cf = slw.main(u, L, np.append([0], Ks), C=2.5)
        plt.plot(Ks*10 ** 6, Cf*1000, "o-", label = f"U = {round(mps_to_knots(u))} kts", color = colors[i])
        plt.plot(np.append([0], Ks)*10 ** 6, SL_Cf*1000, "d--", color = colors[i])
    plt.xlabel(r"$k\,[\mathrm{\mu\,m}]$")
    plt.ylabel(r"$C_F\times10^3$")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "lahoFlatPlate.pdf"))
    plt.show()

def make_table_for_k_from_height():
    h = np.arange(1, 6, 1)
    sc = 50
    for j in h:
        print(sc, j, get_k_from_h_SC(j, sc))

def get_smooth_Cfs(Us, L):
    return get_ITTC_CF(get_Re(Us, L, NU))

def fit_Cf():
    filepath = os.path.join(RESULTS_DIR, "lahoFlatPlate.pkl")
    CFD_data = read_pickle_data(filepath)
    CFD_Ks, CFD_Cf, Us = CFD_data["Ks"], CFD_data["Cf"], CFD_data["U"]
    UNIQUE_Us = np.sort(np.unique(Us))
    L = 37

    plt.figure(figsize=(8, 6))

    colors = plt.get_cmap('Grays_r')(np.linspace(0,1, len(UNIQUE_Us) + 2))

    for i, u in enumerate(UNIQUE_Us):
        Ks = CFD_Ks[Us == u]
        Cf = CFD_Cf[Us == u]
        Cf_S = get_smooth_Cfs(u, L)
        popt, pcov = curve_fit(fit, Ks, Cf - Cf_S, p0=[0.002, 0,10])
        print(round(mps_to_knots(u)), popt, np.sqrt(np.diag(pcov)))
        plt.plot(Ks * 10**6, Cf-Cf_S, "o", label = f"U = {round(mps_to_knots(u))} kts", color = colors[i])
        KS_fit = np.linspace(0, 0.002, 1000)
        plt.plot(KS_fit *10**6, fit(KS_fit, *popt), lw = 2, color = colors[i])#, label = r"${}\ln\left(1-\exp({}-{}k)\right)$".format(*(np.round(popt * np.asarray([1000, 100, 1])) / np.asarray([1000, 100, 1])) ))
        print("Error:", popt[0] * (1 - np.exp(popt[1])))
    plt.xlabel(r"$k\,[\mathrm{\mu\,m}]$")
    plt.ylabel(r"$\Delta C_F$")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "lahoFlatPlate_Cf_fit.pdf"))
    plt.show()

def fit(x, a, b,c):
    return a*(1- np.exp((b -c*x)))

def lahoFlatPlate_contour():
    filepath = os.path.join(RESULTS_DIR, "lahoFlatPlate.pkl")
    CFD_data = read_pickle_data(filepath)
    CFD_Ks, CFD_Cf, Us = CFD_data["Ks"], CFD_data["Cf"], CFD_data["U"]
    UNIQUE_Us = np.sort(np.unique(Us))
    UNIQUE_Ks = np.sort(np.unique(CFD_Ks))
    L = 37

    fig, ax = plt.subplots(1, 2, figsize=(12, 8))
    ax1, ax2 = ax

    delta_Ps = np.zeros((len(UNIQUE_Us), len(UNIQUE_Ks)))
    for Ks, u, Cf in zip(CFD_Ks, Us, CFD_Cf):
        Cf_S = get_smooth_Cfs(u, L)
        delta_P = (Cf - Cf_S) / Cf_S
        delta_Ps[np.argmin(np.abs(u-UNIQUE_Us)), np.argmin(np.abs(Ks-UNIQUE_Ks))] = delta_P
    
    # delta_ms = np.multiply(delta_Ps * ECF_CO2 * SFOC, np.expand_dims(UNIQUE_Us, axis=1)**3)
    delta_ms = delta_Ps * ECF_CO2 * SFOC
    U, KS = np.meshgrid(mps_to_knots(UNIQUE_Us), UNIQUE_Ks)
    KS *= 10 ** 6

    cf = ax1.contourf(U, KS, delta_Ps.T*100, cmap = "Grays")
    CS = ax1.contour(U, KS, delta_Ps.T*100)
    ax1.clabel(CS, fontsize=10)
    cb1 = plt.colorbar(cf, ax = ax1, orientation = "horizontal")
    cb1.set_label(r"$\delta P$ [%]")
    ax1.set_xlabel("U [kts]")
    ax1.set_ylabel(r"$k\,[\mathrm{\mu\,m}]$")

    cf2 = ax2.contourf(U, KS, delta_ms.T, cmap = "Grays")
    CS2 = ax2.contour(U, KS, delta_ms.T)
    ax2.clabel(CS2, fontsize=10)
    cb2 = plt.colorbar(cf2, ax = ax2, orientation = "horizontal")
    cb2.set_label(r"$\Delta\dot{m}/P_{\mathrm{smooth}}\,[\mathrm{kg\,CO_2\,/\,kW\,h}]$")
    ax2.set_xlabel("U [kts]")
    # ax2.set_ylabel(r"$k\,[\mathrm{\mu\,m}]$")
    cb2.set_ticks(cb2.get_ticks()[::2])
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "lahoFlatPlate_contour.pdf"))
    plt.show()

def Delta_m_vs_U():
    fig, ax = plt.subplots(1, 1, figsize=(8,6))
    ax2 = ax.twinx()
    filepath = os.path.join(RESULTS_DIR, "lahoFlatPlate.pkl")
    CFD_data = read_pickle_data(filepath)
    max_ks = np.max(CFD_data["Ks"])
    L = 37
    Cf = CFD_data["Cf"][CFD_data["Ks"]==max_ks]
    U = CFD_data["U"][CFD_data["Ks"]==max_ks]
    dm = (Cf / get_smooth_Cfs(U, L)-1) * ECF_CO2 * SFOC*U**3 / 1000 * 1028
    d_price = (Cf / get_smooth_Cfs(U, L)-1) * SFOC*U**3 * 1.82 / 0.84 / 1000 * 1028 #https://www.globalpetrolprices.com/Slovenia/diesel_prices/#:~:text=The%20current%20price%20of%20diesel%20fuel%20in,based%20on%20the%20latest%20update%20from%2013%2DApr%2D2026.
    ax.plot(mps_to_knots(U), dm, lw = 3, color = "black")
    ax2.plot(mps_to_knots(U), d_price, lw = 3, color = "black")
    ax.set_xlabel("U [kts]")
    ax.set_ylabel(r"$\frac{\Delta\dot{m}}{\tilde{S}}\,[\mathrm{kg\,CO_2\,/\,m^2\,h}]$")
    ax2.set_ylabel(r"$\frac{\Delta\dot{\mathrm{price}}}{\tilde{S}}\,[\mathrm{EUR\, / \,m^2\,h}]$")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "lahoFlatPlate_price.pdf"))
    plt.show()

def lahoFlatPlate_contour_U3():
    filepath = os.path.join(RESULTS_DIR, "lahoFlatPlate.pkl")
    CFD_data = read_pickle_data(filepath)
    CFD_Ks, CFD_Cf, Us = CFD_data["Ks"], CFD_data["Cf"], CFD_data["U"]
    UNIQUE_Us = np.sort(np.unique(Us))
    UNIQUE_Ks = np.sort(np.unique(CFD_Ks))
    L = 37

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))

    delta_Ps = np.zeros((len(UNIQUE_Us), len(UNIQUE_Ks)))
    for Ks, u, Cf in zip(CFD_Ks, Us, CFD_Cf):
        Cf_S = get_smooth_Cfs(u, L)
        delta_P = (Cf - Cf_S) / Cf_S
        delta_Ps[np.argmin(np.abs(u-UNIQUE_Us)), np.argmin(np.abs(Ks-UNIQUE_Ks))] = delta_P
    
    delta_ms = np.multiply(delta_Ps * ECF_CO2 * SFOC, np.expand_dims(UNIQUE_Us, axis=1)**3) / 1000 * 1028

    U, KS = np.meshgrid(mps_to_knots(UNIQUE_Us), UNIQUE_Ks)
    KS *= 10 ** 6

    cf2 = ax.contourf(U, KS, delta_ms.T, cmap = "Grays")
    CS2 = ax.contour(U, KS, delta_ms.T)
    ax.clabel(CS2, fontsize=10)
    cb2 = plt.colorbar(cf2, ax = ax, orientation = "horizontal")
    cb2.set_label(r"$\Delta\dot{m}/\tilde{S}\,[\mathrm{kg\,CO_2\,/\,m^2\,h}]$")
    ax.set_xlabel("U [kts]")
    ax.set_ylabel(r"$k\,[\mathrm{\mu\,m}]$")
    cb2.set_ticks(cb2.get_ticks()[::2])
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "lahoFlatPlate_contour_U3.pdf"))
    plt.show()


if __name__ == "__main__":
    # roughness_function_vs_Re()
    # largeFlatPlate_cf()
    # make_table_for_k_from_height()
    # lahoFlatPlate_cf()
    # fit_Cf()
    # lahoFlatPlate_contour()
    # Delta_m_vs_U()
    lahoFlatPlate_contour_U3()