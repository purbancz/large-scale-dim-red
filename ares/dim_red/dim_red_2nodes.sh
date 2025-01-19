#!/bin/bash
#SBATCH --job-name=geom_emb_dim_red_2nodes  # Job name
#SBATCH --output=%x_%j.out                  # Output file (%x = job name, %j = job ID)
#SBATCH --error=%x_%j.err                   # Error file
#SBATCH --time=24:00:00                      # Max time (hh:mm:ss)
#SBATCH --partition=plgrid                  # Partition name
#SBATCH --account=plglscclass24-cpu         # Account name
#SBATCH --nodes=2                           # Number of nodes
#SBATCH --ntasks-per-node=1                 # Number of tasks per node
#SBATCH --cpus-per-task=16                   # Number of CPU cores per task
#SBATCH --mem=64G                           # Memory allocation per node

# Load modules and activate the conda environment
module load miniconda3
conda init
eval "$(conda shell.bash hook)"
conda activate cupy-env

echo "PYTHON SCRIPT IS BEING EXECUTED"

# Run the Python script
srun python $HOME/dim_red/geom_emb_dim_red.py
