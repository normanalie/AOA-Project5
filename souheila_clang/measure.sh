#!/bin/bash

val=10

# Boucle pour n variant de 15 à 1500 avec un pas de 15
for ((n=15; n<=1500; n+=15)); do
    echo "Exécution avec n = $n"

    # Exécute la commande avec taskset sur le cœur 1 et redirige la sortie vers un fichier
    taskset -c 1 /bin/measure $n 3 $val > "/home/benabid-guendouzi/Documents/GitHub/AOA-Project5/souheila_clang/measured_values_03/measure_${n}_3_${val}.txt" 2>&1

    # Optionnel : Ajout d'un délai entre les exécutions pour éviter une surcharge
    sleep 0.1
done

echo "Toutes les exécutions sont terminées."
