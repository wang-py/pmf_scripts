#!/bin/bash

# this script plots all displacement distributions and saves those figures

# folder that contains all xvgs
WINDOWS=$1

# plotting script
PLOT_SCRIPT=pos_distribution_plot.py

for window in $WINDOWS/*
do
  # get rid of parent paths
  name=$(basename $window)

  # get rid of extensions
  filename=${name%.xvg}

  python $PLOT_SCRIPT $window $filename
  mv $filename.png $WINDOWS

done
