#!/bin/bash

rep=10

# Boucle pour n variant de 60 à 3535 avec un pas de 15
for ((n=30; n<=3535; n+=15)); do
    echo "Exécution avec n = $n"

    taskset -c 1 ./bin/measure $n 3 $val > "/home/linuxbox/AOA-Project5/measures-norman/measure_${n}_3_${rep}.txt" 2>&1

    sleep 0.1
done
