#!/bin/bash
#PBS -N bt_bc_decomp
#PBS -A NCGD0011
#PBS -l select=1:ncpus=8:mem=240GB
#PBS -l walltime=02:00:00
#PBS -q casper
#PBS -j oe

module load conda
conda activate mom6-tools

python Barotropic_baroclinic_decomp.py

