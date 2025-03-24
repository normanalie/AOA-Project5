#!/bin/bash

val=30

sudo cpupower -c all frequency-set -g performance
rm -rf measured_values/measures_$1
mkdir measured_values/measures_$1

# Boucle pour n variant de 60 à 3535 avec un pas de 50
for ((n=134; n<=1268; n+=14)); do
    echo "Exécution avec n = $n"



    # Exécute la commande avec taskset sur le cœur 1 et redirige la sortie vers un fichier
    taskset -c 1 bin/measure $n 100 $val > "/home/mathieu/Downloads/AOA-Project5/mathieu_icx/measured_values/measures_${1}/measure_${n}_100_${val}.txt" 2>&1

    # Optionnel : Ajout d'un délai entre les exécutions pour éviter une surcharge
    sleep 0.1
done
