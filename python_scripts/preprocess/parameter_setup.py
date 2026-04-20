import os
import json
import sys
import itertools
import pickle
import pandas as pd

TEST_CASE = sys.argv[1]
# TEST_DIR = os.path.join(os.getcwd(), f"openfoam_simualations/{TEST_CASE}")
# ORIG_SETUP_DIRS = ["setups.orig/common/0.orig", "setups.orig/KomegaSST/0.orig"]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_parameters(case):
    with open(os.path.join(os.getcwd(), f"parameters/{case}/parameters.json"), "r") as f:
        params = json.load(f)
    
    f.close()
    return params

def get_combinations(params):
    list_params = []
    list_params_names = []
    non_list_params = {}
    for params_item in params.keys():
        if type(params[params_item]) is list:
            list_params.append(params[params_item])
            list_params_names.append(params_item)
        else:
            non_list_params[params_item] = params[params_item]
    combos = list(itertools.product(*list_params))
    p_combos = []
    for combination in combos:
        p = {}
        for name, pi in zip(list_params_names, combination):
            p[name] = pi
        for non_list_p in non_list_params.keys():
            p[non_list_p] = non_list_params[non_list_p]
        p_combos.append(p)
    return p_combos

def write_config(case, params):
    for k in range(len(params)):
        with open (os.path.join(os.getcwd(), f"parameters/{case}/parameter_config_{k}.h"), "w") as f:
            for key, value in params[k].items():
                f.write(f"{key}\t{value};\n")
        f.close()

def save_params_in_results(case, params):
    df = {name:[] for name in params[0].keys()}
    df["Cf"] = []
    for i in range(len(params)):
        for name in params[i].keys():
            df[name].append(params[i][name])
        df["Cf"].append(0.0)
    df = pd.DataFrame(df)
    with open(os.path.join(os.getcwd(), f"results/{case}.pkl"), "wb") as f:
        pickle.dump(df, f)

if __name__ == "__main__":
    parameter_combinations = get_combinations(load_parameters(TEST_CASE))
    write_config(TEST_CASE, parameter_combinations)
    save_params_in_results(TEST_CASE, parameter_combinations)