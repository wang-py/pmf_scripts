#!/bin/bash

#frame buffer
fb=framebuffer.pdb

#xtc file
tr=$1

#gromacs
gro=$2

#coordinate buffer
cb=$3
START=0

#frame count
END=$(($4 * 20))
#calculating half steps
#decimal places
DP="scale=3;"

#time step
TS="*0.05"

#headgroup carbon atom number
ATOM_NUM=C3

for (( i=$START; i<$END; i++ ))
do
    TIME=$(echo "$DP$i$TS" | bc)
    echo 1 | gmx trjconv -f $tr -s $gro -dump $TIME -o $fb &>/dev/null

    #frame count
    fc=$((i+1))
    echo "frame $fc: " >> $cb

    #find the carbon attached to the tail
    grep -w $ATOM_NUM $fb >> $cb

    #remove framebuffer
    rm $fb
done
