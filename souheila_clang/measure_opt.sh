#!/bin/bash

# $1 = l'optimisation effectuée lors du make
# $2 = valeur de n telle que T(n) ~= 90% de L1
# $3 = valeur de n telle que T(n) ~= 50% de L3

val=10
sudo cpupower -c all frequency-set -g performance

mkdir -p /home/benabid-guendouzi/Documents/GitHub/AOA-Project5/souheila_clang/measured_values_opt
mkdir -p /home/benabid-guendouzi/Documents/GitHub/AOA-Project5/souheila_clang/measured_values_opt/$1

# Exécute la commande avec taskset sur le cœur 1 et redirige la sortie vers un fichier
taskset -c 1 /home/benabid-guendouzi/Documents/GitHub/AOA-Project5/bin/measure $2 100 $val > "/home/benabid-guendouzi/Documents/GitHub/AOA-Project5/souheila_clang/measured_values_opt/${1}/measure_$2_100_${val}.txt" 2>&1
echo "Execution en ${1} avec n=${2}"
taskset -c 1 /home/benabid-guendouzi/Documents/GitHub/AOA-Project5/bin/measure $3 100 $val > "/home/benabid-guendouzi/Documents/GitHub/AOA-Project5/souheila_clang/measured_values_opt/${1}/measure_$3_100_${val}.txt" 2>&1
echo "Execution en ${1} avec n=${3}"
sleep 0.1

echo "Toutes les exécutions sont terminées."