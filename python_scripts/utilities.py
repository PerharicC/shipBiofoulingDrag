import numpy as np

KAPPA = 0.41 # von Karman constant
NU = 1.1 * 10 ** (-6)

def get_ITTC_CF(Re):
    return 0.075 / (np.log10(Re) - 2) ** 2

def get_Prandtl_CF(Re):
    return 0.074 / Re ** (1 / 5)

def get_kp(k, ut, nu = NU): 
    '''
    Calculate roughness Reynolds number
    ----------------------

    k
        roughness height
    ut
        shear velocity
    nu
        kinematic viscosity
    '''
    return k * ut / nu

def get_Up(yp, B=5, kappa = KAPPA):
    '''
    Calculate dimensionless velocity
    ----------------------

    yp
        roughness height
    B
        shear velocity
    kappa
        von Karman constant
    '''
    
    return np.log(yp) / kappa + B

def get_DeltaUp1(kp, kappa = KAPPA, C =2.5):
    '''
    Calculate rougness function of type 1
    -----------------------

    kp
        Roughness reynolds number
    kappa
        von Karman constant
    '''

    Delta_UP = np.log((1 + kp) / C) / kappa
    Delta_UP[Delta_UP < 0] = 0
    return Delta_UP

def get_ut_from_CF(U, CF):
    '''
    Calculate friction velocity from friction coefficient
    ----------------------

    U
        Velocity
    CF
        Friction drag coefficient
    '''

    return U * np.sqrt(CF / 2)

def get_CF_from_Up(Up):
    '''
    Calculate friction coefficient from dimenisonless velocity
    ----------------------

    Up
        Dimensionless velocity
    '''
    
    return 2 / Up ** 2

def get_Up_from_CF(CF):
    '''
    Calculate dimenisonless velocity from friction coefficient
    ----------------------

    CF
        Friction coefficient
    '''
    
    return np.sqrt(2 / CF)

def get_Re(U, L , nu=NU):
    return U * L / nu

def knots_to_mps(u):
    return u / 1.94384

def mps_to_knots(u):
    return u * 1.94384

def get_k_from_h_SC(h, Sc):
    return -17.53 -8.128 * Sc + 69.57 * h + 0.4501 * Sc ** 2 + 0.4165 * Sc * h - 14.81 * h ** 2 - 0.00548 * Sc ** 3 + 0.000456 * Sc**2 * h + 0.837 * Sc * h ** 2