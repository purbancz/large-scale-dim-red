#!/bin/bash
#SBATCH --job-name=geom_emb_dim_red_1node   # Job name
#SBATCH --output=%x_%j.out                  # Output file (%x = job name, %j = job ID)
#SBATCH --error=%x_%j.err                   # Error file
#SBATCH --time=12:00:00                     # Max time (hh:mm:ss)
#SBATCH --partition=plgrid-now              # -now Partition name
#SBATCH --account=plglscclass24-cpu         # Account name
#SBATCH --nodes=1                           # Number of nodes
#SBATCH --ntasks=1                          # Number of tasks
#SBATCH --cpus-per-task=48                  # Number of CPU cores per task
#SBATCH --mem=184800                        # Memory allocation

# Load modules and activate the conda environment
module load miniconda3
conda init
eval "$(conda shell.bash hook)"
conda activate dim-reduction

echo "PYTHON SCRIPT IS BEING EXECUTED"

# Run the Python script
python $HOME/dim_red/geom_emb_dim_red.py
