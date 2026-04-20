import os
import sys
import numpy as np
import pickle
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
from python_scripts.utilities import NU

TEST_CASE = sys.argv[1]
SIM_NUMBER = int(sys.argv[2])
OUTPUT_PATH = sys.argv[3]

def get_Cf(U, profiles):
    if not os.path.exists(profiles):
        raise FileNotFoundError(f"profiles.dat not found: {profiles}")

    data = np.loadtxt(profiles, comments="#")
    if data.ndim != 2 or data.shape[1] < 4:
        raise ValueError("profiles.dat has unexpected format")

    x = data[:, 0]
    tau = np.sqrt(data[:, 1] ** 2 + data[:, 2] ** 2 + data[:, 3] ** 2)

    idx = np.argsort(x)
    x = x[idx]
    tau = tau[idx]

    q_kin = 0.5 * U ** 2
    cf_local = tau / q_kin

    L = float(x[-1] - x[0])
    re_l = U * L / NU
    print(L)
    return float(np.trapezoid(cf_local, x) / L)

def load_parameters(case):
    with open(os.path.join(os.getcwd(), f"results/{case}.pkl"), "rb") as f:
        params = pickle.load(f)
    f.close()
    return params

def write_result(case, params, k, Cf):
    params.loc[k, "Cf"] = Cf
    with open(os.path.join(os.getcwd(), f"results/{case}.pkl"), "wb") as f:
        params = pickle.dump(params, f)
    f.close()

def main(case, k, profiles_path):
    params = load_parameters(case)
    U = params.loc[k, "U"]
    Cf = get_Cf(U, profiles_path)
    write_result(TEST_CASE, params, k, Cf)



if __name__ == "__main__":
    profiles = os.path.join(os.getcwd(), OUTPUT_PATH)
    main(TEST_CASE, SIM_NUMBER, profiles)
    # print(get_Cf(9.77, profiles))