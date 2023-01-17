#!/bin/bash

# This script automates all energy minimization of snapshots
# Author: Panyue Wang (pywang@ucdavis.edu)

# Experiment folder
EXP_FOLDER=~/SAMSUNG_SSD/ComplexI/LipolyticaQ/water_in_complexI/chain_JKAHN/

# Topology file
TOPOL=$EXP_FOLDER/topology/charged/lipolytica_JKAHN_ions_SOL.top

# Index file
INDEX=$EXP_FOLDER/topology/charged/PMF_index.ndx

# EM folder
EM_DIR=$1

# EM config folder
EM_CONFIG=$EM_DIR/EM_configs

if [ ! -d $EM_CONFIG ]
then
    mkdir $EM_CONFIG
fi
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
    filename=${name%.pdb}_EM_${k}

    # create a folder for each MD
    # mkdir -p $MD_DIR/$filename/results
    
    # create tprs for MD
    gmx grompp -f $MDP -r $snap -c $snap -n $INDEX -p $TOPOL -o $EM_DIR/$filename.tpr

    # run MD
    gmx mdrun -s $EM_DIR/$filename.tpr -deffnm $EM_DIR/${filename}_data -c $EM_CONFIG/${filename}.gro

    # convert GRO to PDB and recover chain information
    echo 0 | gmx trjconv -s $EM_DIR/$filename.tpr -f $EM_CONFIG/${filename}.gro -o $EM_CONFIG/${filename}.pdb

done

# remove GRO structure files
rm $EM_CONFIG/*.gro
