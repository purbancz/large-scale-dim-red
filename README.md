# Large-scale dimensionality reduction on HPC clusters

This repository contains scripts and workflows to perform large-scale dimensionality reduction tasks using HPC resources on Athena and Ares clusters. The primary goal is to enable efficient computation and parallelism for handling high-dimensional datasets. Below are the steps, commands, and setup details for this repository.

---

## Prerequisites

### Requirements
- Valid account on **Athena** or **Ares** cluster.
  ```bash
  ssh [username]@ares.cyfronet.pl
  ssh [username]@athena.cyfronet.pl
  ```
- Access to dataset.
  ```bash
  ls -l /net/pr2/projects/plgrid/plgglscclass/geometricus_embeddings/X_concatenated_all_dims.npy
  ```
- Familiarity with SLURM job scheduler.

### Environment Setup
- Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to manage Python environments.
- Load necessary modules (specific to the cluster):
  ```bash
  module load miniconda3
  ```
  on Ares or
  ```bash
  module load Miniconda3
  ```
  on Athena.

---

## Repository Structure

```
.
├── ares/                           # Directory for Ares cluster scripts and outputs
│   ├── dim_red/                    # Dimensionality reduction scripts and results
│   │   ├── output_1node_max_run0/  # Results for 1-node maximum configuration
│   │   ├── output_2nodes_run0/     # Results for 2-nodes configuration
│   │   ├── dim_red_1node.sh        # SLURM script for 1-node
│   │   ├── dim_red_2nodes.sh       # SLURM script for 2-nodes
│   │   └── geom_emb_dim_red.ipynb  # Jupyter notebook for dimensionality reduction
├── athena/                         # Directory for Athena cluster scripts and outputs
│   ├── dim_red/                    # Dimensionality reduction scripts and results
│   │   ├── output_1node_run0/      # Results for 1-node configuration
│   │   ├── output_2nodes_run0/     # Results for 2-nodes configuration
│   │   ├── dim_red_1node.sh        # SLURM script for 1-node
│   │   ├── dim_red_2nodes.sh       # SLURM script for 2-nodes
│   │   └── geom_emb_dim_red.py     # Python script for dimensionality reduction
└── README.md                       # This file
```

---

## Workflow and Commands

### 1. Setting Up the Python Environment
- (Recommended step) Configure conda to use your `$SCRATCH` storage space:
  ```bash
  conda config --add envs_dirs ${SCRATCH}/.conda/envs 
  conda config --add pkgs_dirs ${SCRATCH}/.conda/pkgs
  ```
- Create a virtual environment:
  ```bash
  conda create -n dim-reduction python=3.8 -y
  conda activate dim-reduction
  ```
- Install required libraries:
  ```bash
  conda install -c conda-forge numpy pandas seaborn matplotlib scikit-learn umap-learn pacmap trimap
  ```

### 2. Preparing the Input Data
- Check whether you have acces to the data
  ```bash
  ls -l /net/pr2/projects/plgrid/plgglscclass/geometricus_embeddings/X_concatenated_all_dims.npy
  ls -ld /net/pr2/projects/plgrid/plgglscclass/geometricus_embeddings
  ```

### 3. Running Dimensionality Reduction Locally
- Test scripts locally to ensure compatibility before deploying on the cluster:
  ```bash
  python scripts/dim_reduction.py --input data/dataset.csv --output results/reduced.csv
  ```
- You can also use jupyter notebook file to test compatibility of the code (locally or in the cluster).

### 4. Running on HPC Clusters

#### Example SLURM Script for Ares (1 Node)
Save the following script as `ares/dim_red/dim_red_1node.sh`:
```bash
#!/bin/bash
#SBATCH --job-name=geom_emb_dim_red_1node
#SBATCH --output=dim_red_1node_%j.out
#SBATCH --error=dim_red_1node_%j.err
#SBATCH --time=72:00:00
#SBATCH --partition=plgrid
#SBATCH --account=[grantname]-cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=184800

module load miniconda3
conda init
eval "$(conda shell.bash hook)"
conda activate dim-reduction

python geom_emb_dim_red.py
```

#### Example SLURM Script for Athena (2 Nodes)
Save the following script as `athena/dim_red/dim_red_2nodes.sh`:
```bash
#!/bin/bash
#SBATCH --job-name=dim_red_2nodes
#SBATCH --output=dim_red_2nodes_%j.out
#SBATCH --error=dim_red_2nodes_%j.err
#SBATCH --time=48:00:00
#SBATCH --partition=plgrid-gpu-a100
#SBATCH --account=[grantname]-gpu-a100
#SBATCH --nodes=2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=800G
#SBATCH --gres=gpu:1

module load miniconda3
conda init
eval "$(conda shell.bash hook)"
conda activate dim-reduction

python geom_emb_dim_red.py
```

#### Submitting the Job
Submit the job using:
```bash
sbatch dim_red/dim_red_1node.sh
sbatch dim_red/dim_red_2nodes.sh
```

### 5. Monitoring Job Progress
- Check all jobs status:
  ```bash
  squeue
  ```
- Check your jobs status:
  ```bash
  squeue -u $USER
  ```
- View detailed job information:
  ```bash
  sacct -j <job_id>
  ```
- Cancel the job:
  ```bash
  scancel <job_id>
  ```
- Inspect logs:
  ```bash
  less dim_red/dim_red_1node_<job_id>.out
  less dim_red/dim_red_2nodes_<job_id>.out
  ```

---

## Links and Resources
- [SLURM Job Scheduler Documentation](https://kdm.cyfronet.pl/portal/Podstawy:SLURM)
- [Ares HPC Documentation](https://docs.cyfronet.pl/display/~plgpawlik/Ares)
- [Athena HPC Documentation](https://docs.cyfronet.pl/display/~plgpawlik/Athena)

---

## Notes
- Modify memory and time requirements in the SLURM script according to the size of your dataset.
- Use multi-node setups for larger datasets and adjust `#SBATCH` directives accordingly.
- The first time you run conda it might be necessary to initialize it with command `conda init bash` (after which the shell needs to be reloaded).

---

## Authors and Acknowledgments
- Developed by [![github](https://img.shields.io/badge/GitHub-purbancz-181717.svg?style=flat&logo=github)](https://github.com/purbancz)
[![X](https://img.shields.io/badge/X-@purbancz-%23000000.svg?logo=X&logoColor=white)](https://twitter.com/purbancz)
[![linkedIn](https://custom-icon-badges.demolab.com/badge/LinkedIn-Piotr_Urbańczyk-0A66C2?logo=linkedin-white&logoColor=fff)](https://www.linkedin.com/in/piotr-urba%C5%84czyk-9943ab17a/)
[![website](https://img.shields.io/badge/Website-Piotr_Urbańczyk-5087B2.svg?style=flat&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHg9IjBweCIgeT0iMHB4IiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDI0IDI0Ij4KICAgIDxwYXRoIGQ9Ik0gMTIgMi4wOTk2MDk0IEwgMSAxMiBMIDQgMTIgTCA0IDIxIEwgMTAgMjEgTCAxMCAxNCBMIDE0IDE0IEwgMTQgMjEgTCAyMCAyMSBMIDIwIDEyIEwgMjMgMTIgTCAxMiAyLjA5OTYwOTQgeiIgZmlsbD0iI2ZmZiI+PC9wYXRoPgo8L3N2Zz4=)](https://www.copernicuscenter.edu.pl/en/person/urbanczyk-piotr-2/)
.
- Thanks to Cyfronet HPC team for their documentation.



## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
