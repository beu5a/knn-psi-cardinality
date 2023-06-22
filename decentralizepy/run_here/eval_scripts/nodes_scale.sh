#!/bin/bash

cd ..
# Array of argument values (integers)
argument_values=(8 16 32 64 128)

script_name=$(basename "$0")
script_name_without_extension=${script_name%.*}

# Loop over the argument values
for arg_value in "${argument_values[@]}"
do
    echo "Running script with argument value: $arg_value"
    ./run_psiknn.sh "$arg_value" 1 $script_name_without_extension # Replace "your_script.sh" with the name of your script    
    echo "Finished running script with argument value: $arg_value"
    echo ""
done


