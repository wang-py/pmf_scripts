#!/bin/bash

# this script plots all displacement distributions and saves those figures

# plotting script
PLOT_SCRIPT=$1

# folder that contains all xvgs
RUNS=$2

# pulling velocity
VELOCITY=$3

# save figures
SAVE_FIG=1

for run in `ls $RUNS/*pullf.xvg | sort -V`; do
  # get rid of parent paths
  name=$(basename $run)

  # get rid of extensions
  filename=${run%_pullf.xvg}

  python $PLOT_SCRIPT $run $VELOCITY $SAVE_FIG ${filename}
  #mv $filename.png $RUNS

done
