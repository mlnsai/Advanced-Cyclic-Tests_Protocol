#!/bin/sh
#SBATCH --partition=standard
#SBATCH --time=14-00:00:00
#SBATCH -N 5
#SBATCH --ntasks-per-node=3
#SBATCH --job-name="work-I"
#SBATCH --output=Test.out
#SBATCH --error=test.err

module load /miniconda3/envs/param_krishna/bin/python

export OMP_NUM_THREADS=1        

python -m main
