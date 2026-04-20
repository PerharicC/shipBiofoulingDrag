import numpy as np
from utilities import *
from scipy.optimize import root


def iteration_step(CF1, U, k, nu, Up):
    ut = get_ut_from_CF(U, CF1)
    kp = get_kp(k, ut, nu)
    DeltaUp = get_DeltaUp1(kp)
    CF2 = get_CF_from_Up(Up - DeltaUp)
    return CF2

def run(n, U, L, k, maxtoll = 10 ** -5, nu = NU):
    Re = get_Re(U, L, nu)
    CF_ITTC = get_ITTC_CF(Re)
    CF_rough = CF_ITTC
    Up = get_Up_from_CF(CF_ITTC)

    for i in range(n):
        
        CF_rough_new = iteration_step(CF_rough, U, k, nu, Up)
        error = np.abs(CF_rough - CF_rough_new)
        CF_rough = CF_rough_new

        if error <= maxtoll:
            print(f"Stopping itteration after {i+1} steps. Error: {error}.")
            break

    if i == n-1:
        print(f"Simulation didn't converge after {n} steps. Final error: {error}.")

    return CF_ITTC, CF_rough

def find_Up_rough(Up, Up_SMOOTH, U, k, nu = NU,C =2.5):
    return Up - Up_SMOOTH + get_DeltaUp1(get_kp(k, U / Up, nu), C=C)

def run2(U, L, k, nu=NU, C=2.5):
    Re = get_Re(U, L, nu)
    CF_ITTC = get_ITTC_CF(Re)
    Up_SMOOTH = get_Up_from_CF(CF_ITTC)
    Up_ROUGH = root(find_Up_rough, Up_SMOOTH, args = (Up_SMOOTH, U, k, nu, C)).x
    
    if len(Up_ROUGH) != 1:
        raise ValueError("More than one root found in U^plus!")
    
    Cf = get_CF_from_Up(Up_ROUGH[0])
    return Cf


def main(U, L, k, n=100, maxtoll = 10 ** -5, nu = NU, C=2.5):
    Cf = []
    for ki in k:
        # Cf.append(run(n, U, L, ki, maxtoll=maxtoll, nu=nu)[1])
        Cf.append(run2(U, L, ki, nu, C))
    return np.asarray(Cf)