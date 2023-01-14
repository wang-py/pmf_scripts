#!/bin/bash

# This script automates all pmf MD of snapshots
# Author: Panyue Wang (pywang@ucdavis.edu)

# Experiment folder
EXP_FOLDER=~/SAMSUNG_SSD/ComplexI/LipolyticaQ/water_in_complexI/chain_JKAHN/

# Topology file
TOPOL=$EXP_FOLDER/topology/charged/lipolytica_JKAHN_ions_SOL.top

# Index file
INDEX=$EXP_FOLDER/topology/charged/PMF_index.ndx

# MD folder
MD_DIR=$1

# snapshot folder
SNAPS=$2

# MDP file
MDP=$3

# get spring constant from filename
k="${MDP#*_}"
k="${k%%.*}"
k="${k#*_}"

for snap in $(ls -1 -v $SNAPS/*.pdb)
do
    # get rid of parent paths
    name=$(basename $snap)

    # get rid of extensions
    filename=${name%.pdb}_2.5ns_${k}

    # create a folder for each MD
    # mkdir -p $MD_DIR/$filename/results
    
    # create tprs for MD
    gmx grompp -f $MDP -r $snap -c $snap -n $INDEX -p $TOPOL -o $MD_DIR/$filename.tpr

    # run MD
    gmx mdrun -s $MD_DIR/$filename.tpr -v -deffnm $MD_DIR/${filename}_data

done
