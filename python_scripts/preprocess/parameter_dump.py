import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(SCRIPT_DIR)))

import json
import numpy as np
from python_scripts.utilities import knots_to_mps

TEST_CASE = sys.argv[1]


params_largeFlatPlate = {
    "U":knots_to_mps(19),
    "Ks":(np.arange(0, 500, 100)/10**6).tolist(),
    "Cs": 0.5
}

params_lahoFlatPlate = {
    "U":knots_to_mps(np.arange(4, 8, 1)).tolist(),
    "Ks":(np.asarray([135, 308, 534, 815, 1150])/10 ** 6).tolist(),
    "Cs": 0.5
}

parameters = {
    "largeFlatPlate":params_largeFlatPlate,
    "lahoFlatPlate": params_lahoFlatPlate
}

def dump_parameters(case):
    with open(os.path.join(os.getcwd(), f"parameters/{case}/parameters.json"), "w") as f:
        json.dump(parameters[case], f)
    f.close()

if __name__ == "__main__":
    dump_parameters(TEST_CASE)