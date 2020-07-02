#!/bin/bash

# this script plots all displacement distributions and saves those figures

# plotting script
PLOT_SCRIPT=$1

# folder that contains all xvgs
RUNS=$2

# pulling velocity
VELOCITY=$3

# title
TITLE=$4

# save figures
SAVE_FIG=1

# run number
RUN=1

# search work file
SEARCH_WORK=search_work.txt
for run in `ls $RUNS/*pullf.xvg | sort -V`; do
    # get rid of parent paths
    # name=$(basename $run)

    # get rid of extensions
    # filename=${run%_pullf.xvg}
    filename=run${RUN}\ ${TITLE}

    python $PLOT_SCRIPT $run $VELOCITY $SAVE_FIG ${filename} >> $SEARCH_WORK
    let RUN=$RUN+1
    #mv $filename.png $RUNS

done
