#!/bin/bash

val=8

# Boucle pour n variant de 15 à 1500 avec un pas de 15
for ((n=15; n<=2015; n+=20)); do
    echo "Exécution avec n = $n"

    # Exécute la commande avec taskset sur le cœur 1 et redirige la sortie vers un fichier
    taskset -c 1 bin/measure $n 5 $val > "/home/benabid-guendouzi/Documents/GitHub/AOA-Project5/souheila_clang/measured_values/measures_Ofast/measure_${n}_5_${val}.txt" 2>&1

    # Optionnel : Ajout d'un délai entre les exécutions pour éviter une surcharge
    sleep 0.1
done

echo "Toutes les exécutions sont terminées."
