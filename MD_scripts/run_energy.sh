#!/bin/bash

# This script automates all pmf MD of snapshots
# Author: Panyue Wang (pywang@ucdavis.edu)

# MDP file
MDP=water_energy.mdp

# Topology file
TOPOL=../topology/charged/lipolytica_JKAHN_ions_SOL.top

# Index file
INDEX=../topology/charged/PMF_index.ndx

# MD folder
MD_DIR=$1

# snapshot folder
SNAPS=$2

# Energy folder
ENERGY_DIR=$3

mkdir -p $ENERGY_DIR

for xtc in $(ls -1 -v $MD_DIR/*_data.xtc)
do
    # get rid of parent paths
    name=$(basename ${xtc%_2.5ns_k7500_data.xtc})

    # snaps that didn't have clashes/issues
    snap=$SNAPS/${name}.pdb

    # filenames for energy reruns
    energy_filename=$(basename ${xtc%.xtc}_energy)

    # xvg filename
    xvg_filename=$(basename ${xtc%.xtc})
    
    # create tprs for MD
    gmx grompp -f $MDP -r $snap -c $snap -n $INDEX -p $TOPOL -o $ENERGY_DIR/$energy_filename.tpr

    # run MD
    gmx mdrun -s $ENERGY_DIR/$energy_filename.tpr -rerun $xtc -v -deffnm $ENERGY_DIR/$energy_filename

    # get energies
    echo 17 18 | gmx energy -f $ENERGY_DIR/$energy_filename.edr -o $ENERGY_DIR/${xvg_filename}_water_energy.xvg

done
