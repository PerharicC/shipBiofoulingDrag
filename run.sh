#!/usr/bin/env bash

set -e

CASES=("largeFlatPlate" "lahoFlatPlate")
mkdir -p parameters
mkdir -p results

for case in "${CASES[@]}"; do
    echo "Running case $case"
    mkdir -p parameters/$case
    python python_scripts/preprocess/parameter_dump.py $case
    python python_scripts/preprocess/parameter_setup.py $case

    paramNum=$(ls parameters/$case/parameter_config*.h -1 | wc -l)
    
    for ((i=0; i<$paramNum; i++)); do
        cp parameters/$case/parameter_config_$i.h openfoam_simualations/$case/setups.orig/common/0.orig/parameter_config.h
        cp parameters/$case/parameter_config_$i.h openfoam_simualations/$case/setups.orig/kOmegaSST/0.orig/parameter_config.h
        ./openfoam_simualations/$case/Allrun
        profilesPath=$(find -wholename "*/$case/*profiles.dat")
        python python_scripts/postprocess/extract_Cf.py $case $i $profilesPath
        ./openfoam_simualations/$case/Allclean
        rm openfoam_simualations/$case/setups.orig/common/0.orig/parameter_config.h
        rm openfoam_simualations/$case/setups.orig/kOmegaSST/0.orig/parameter_config.h

    done
done

echo "Start postprocess"

python python_scripts/postprocess/plots.py