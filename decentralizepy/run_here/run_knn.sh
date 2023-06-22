#!/bin/bash

decpy_path=../eval
#cd $decpy_path

env_python=python3
original_config=./config.ini
config_file=./tmp/config.ini
procs_per_machine=$1
machines=$2
iterations=10
test_after=5
eval_file=../eval/testingKNN.py
log_level=INFO
sub_log_dir=$3


m=0
echo M is $m
log_dir=logging2/$sub_log_dir/$procs_per_machine

if [ -d $log_dir ]; then
    rm -r $log_dir
fi
#rm -r logging/$sub_log_dir
mkdir -p $log_dir

total_procs=$((procs_per_machine * machines))
graph="./topo/${total_procs}_fully_connected.edges"  # Modify the graph variable

knn_rounds=$(echo "l(${total_procs})/l(2)" | bc -l)
knn_rounds=${knn_rounds%.*}  # Remove decimal part
knn_neighbors=6

#cp $original_config $config_file
# echo "alpha = 0.10" >> $config_file
$env_python $eval_file -ro 0 -tea $test_after -kr $knn_rounds -kn $knn_neighbors -ld $log_dir -mid $m -ps $procs_per_machine -ms $machines -is $iterations -gf $graph -ta $test_after -cf $original_config -ll $log_level -wsd $log_dir
