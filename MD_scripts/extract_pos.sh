#!/bin/sh

#script to get all position xvgs for PMF calculations

INDEX=../topology/charged/PMF_index.ndx

XTC_FOLDER=$1

for xtc in $(ls -1 -v $XTC_FOLDER/*_data.xtc)
do
    name=${xtc%_data.xtc}
    echo 18 | gmx traj -s ${name}.tpr -f $xtc -n $INDEX -ox ${name}_water.xvg
done
