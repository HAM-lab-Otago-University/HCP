#!/bin/bash -e
#SBATCH --time=30:00:00
#SBATCH --mem=32GB       
#SBATCH --cpus-per-task=64

module load Python/3.8.2-gimkl-2020a

python layer1-eNet.py
