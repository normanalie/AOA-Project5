#!/bin/bash

val=10

# Boucle pour n variant de 60 à 3535 avec un pas de 50
for ((n=2145; n<=2145; n+=15)); do
    echo "Exécution avec n = $n"



    # Exécute la commande avec taskset sur le cœur 1 et redirige la sortie vers un fichier
    taskset -c 1 ../bin/measure $n 3 $val > "/home/alexandre/Documents/aoa-project/Part1/1/measured_values/alexandre/measure_${n}_3_${val}.txt" 2>&1

    # Optionnel : Ajout d'un délai entre les exécutions pour éviter une surcharge
    sleep 0.1
done
