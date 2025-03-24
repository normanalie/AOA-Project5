import os
import re
import glob
import matplotlib.pyplot as plt

def extract_med_cycles(filename):
    with open(filename, 'r') as file:
        for line in file:
            match = re.search(r"MED (\d+) RDTSC-cycles", line)
            if match:
                return int(match.group(1))
    return None

def extract_size(filename):
    match = re.search(r"measure_(\d+)_\d+_\d+\.txt", filename)
    if match:
        return int(match.group(1))
    return None

def main():
    folder = "measured_values"  # Remplace par le bon chemin
    files = glob.glob(os.path.join(folder, "measure_*.txt"))
    
    data = []
    for file in files:
        size = extract_size(file)
        med_cycles = extract_med_cycles(file)
        if size is not None and med_cycles is not None:
            data.append((size, med_cycles))
    
    data.sort()  # Trier par taille de tableau
    sizes, med_cycles = zip(*data)
    
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, med_cycles, marker='o', linestyle='-', color='b')
    plt.xlabel("Taille du tableau")
    plt.ylabel("Médiane cycles/itération")
    plt.title("Performance en fonction de la taille du tableau")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()