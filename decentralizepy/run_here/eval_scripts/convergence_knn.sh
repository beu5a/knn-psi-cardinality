#!/bin/bash

cd ..
# Array of argument values (integers)
argument_values=(8 16)

# An associative array. Each argument value has its own array of knn_neighbors
declare -A knn_neighbors
knn_neighbors[8]="2 4"
knn_neighbors[16]="2 4 8"
#knn_neighbors[32]="2 4 8"
#knn_neighbors[64]="2 4 8 16"
#knn_neighbors[128]="2 4 8 16"

script_name=$(basename "$0")
script_name_without_extension=${script_name%.*}

# Loop over the argument values
for arg_value in "${argument_values[@]}"
do
    # Convert the string of knn_neighbors to an array
    IFS=' ' read -r -a knn_array <<< "${knn_neighbors[$arg_value]}"

    # Loop over the corresponding knn_neighbors
    for knn in "${knn_array[@]}"
    do
        echo "Running script with argument value: $arg_value and knn_neighbors: $knn"
        ./run_knn_2n.sh "$arg_value" 1 "$knn" $script_name_without_extension
        echo "Finished running script with argument value: $arg_value and knn_neighbors: $knn"
    done
    echo ""
done
