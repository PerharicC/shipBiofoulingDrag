# Biofouling effects on ship transport efficiency

## Description

This is the supporting code for my 2025/2026 research project within the *Jozef Stefan International Postgraduate School* PhD course **Enviromental Physics**, titled: **Biofouling effects on ship transport efficiency**. The course is taught by prof. Dr. Aleksander Zidanšek.

The code can be run from the parent directory by running the shell script [run.sh](./run.sh)

It works as a python wrapper for the open-source CFD solver [openfoam](https://www.openfoam.com/), which is written in c++. The two case studies [largeFlatPlate](./openfoam_simualations/largeFlatPlate/) and [lahoFlatPlate](./openfoam_simualations/lahoFlatPlate/) are modified versions of the  openFOAM [turbulentFlatPlate](https://doc.openfoam.com/2306/examples/verification-validation/turbulent/flat-plate-zpg/) tutorial case. They use the kOmegaSST turbulence scheme and a nutkRougnessFunction. Additionally, some parameters have been tuned to reduce computational times.

The code was tested on a Linux Ubuntu system, version 24.04.4.

## Set-up

1. Download and install openfoam on your local PC.
2. Create and activate a new python environment.
3. Clone this repository.
4. Navigate to the repositorie's main directory.
5. Install the dependencies by running:
```console
user:~$ pip install -r requirements.txt
```
6. Source your openfoam directory.
7. Run the main script file:

```console
user:~$ bash run.sh
```

## Output
The final **PDF report** can be found at [link to pdf](./Perharic_Env_Phy_Report_25_26.pdf)
