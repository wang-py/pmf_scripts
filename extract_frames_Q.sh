#!/bin/bash

#xtc file
tr=$1

#gromacs
gro=$2

#index file
nd=$3

#group number
GROUP_NUM=3

#output file
output=$4

echo $GROUP_NUM | gmx trajectory -f $tr -s $gro -n $nd -ox $output &>/dev/null
