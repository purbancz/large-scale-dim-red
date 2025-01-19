#!/bin/bash
#SBATCH --job-name=geom_emb_dim_red_1node   # Job name
#SBATCH --output=%x_%j.out                  # Output file (%x = job name, %j = job ID)
#SBATCH --error=%x_%j.err                   # Error file
#SBATCH --time=48:00:00                     # Max time (hh:mm:ss)
#SBATCH --partition=plgrid-gpu-a100         # Partition name
#SBATCH --account=plglscclass24-gpu-a100    # Account name
#SBATCH --nodes=1                           # Number of nodes
#SBATCH --ntasks=1                          # Number of tasks
#SBATCH --cpus-per-task=16                  # 0 - 16
#SBATCH --mem=800G                          # 0 - 800G
#SBATCH --gres=gpu:1

# Load modules and activate the conda environment
module load Miniconda3
conda init
eval "$(conda shell.bash hook)"
conda activate dim-reduction

echo "PYTHON SCRIPT IS BEING EXECUTED"

# Run the Python script
python $HOME/dim_red/geom_emb_dim_red.py
