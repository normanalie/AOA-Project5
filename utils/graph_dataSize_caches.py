import os
import re
import math
import matplotlib.pyplot as plt

def extract_n_from_filename(filename):
    """
    Extrait la valeur de n à partir d'un nom de fichier de type:
    measure_<n>_3_<repm>.txt
    """
    match = re.search(r"measure_(\d+)_3_", filename)
    if match:
        return int(match.group(1))
    return None

# Récupération des valeurs de n depuis les fichiers du dossier measures_O2
folder = "measures_O2"
n_values = []
for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        n_val = extract_n_from_filename(filename)
        if n_val is not None:
            n_values.append(n_val)
# Éliminer les doublons et trier
n_values = sorted(set(n_values))

# Calcul de la taille des données pour chaque n selon T(n) = 8*n^2 + 4*n (en octets)
data_sizes = [8*(n**2) + 4*n for n in n_values]

# Limites de cache en octets
l1_limit = 64 * 1024       # 64 KiB
l2_limit = 512 * 1024      # 512 KiB
l3_limit = 3 * 1024 * 1024 # 3 MiB

def intersection_n(cache_size):
    """
    Résout 8*n^2+4*n = cache_size pour n.
    Retourne la valeur réelle, puis on appliquera math.ceil pour obtenir
    la plus petite valeur entière de n qui dépasse (ou atteint) la limite.
    """
    discriminant = math.sqrt(16 + 32 * cache_size)
    n_val = (-4 + discriminant) / 16
    return n_val

# Calcul des intersections (valeur réelle)
n_intersect_l1_real = intersection_n(l1_limit)
n_intersect_l2_real = intersection_n(l2_limit)
n_intersect_l3_real = intersection_n(l3_limit)

# Prendre la plus petite valeur entière qui dépasse la limite (math.ceil)
n_intersect_l1 = math.ceil(n_intersect_l1_real)
n_intersect_l2 = math.ceil(n_intersect_l2_real)
n_intersect_l3 = math.ceil(n_intersect_l3_real)

# Calcul des tailles de données correspondantes pour ces n
T_l1 = 8*(n_intersect_l1**2) + 4*n_intersect_l1
T_l2 = 8*(n_intersect_l2**2) + 4*n_intersect_l2
T_l3 = 8*(n_intersect_l3**2) + 4*n_intersect_l3

# Création du graphique
plt.figure(figsize=(10, 6))
plt.plot(n_values, data_sizes, label=r"$T(n)=8\,n^2+4\,n$", color='blue', marker='o')

# Lignes horizontales pour les limites de cache
plt.axhline(y=l1_limit, color='red', linestyle='--', label="L1 Cache (64 KiB)")
plt.axhline(y=l2_limit, color='green', linestyle='--', label="L2 Cache (512 KiB)")
plt.axhline(y=l3_limit, color='orange', linestyle='--', label="L3 Cache (3 MiB)")

# Marqueurs aux intersections (valeurs entières qui dépassent)
plt.scatter([n_intersect_l1], [T_l1], color='red', s=100, zorder=5, label="Intersection L1")
plt.scatter([n_intersect_l2], [T_l2], color='green', s=100, zorder=5, label="Intersection L2")
plt.scatter([n_intersect_l3], [T_l3], color='orange', s=100, zorder=5, label="Intersection L3")

# Annotation des valeurs de n d'intersection
plt.annotate(f"n = {n_intersect_l1}", (n_intersect_l1, T_l1),
             textcoords="offset points", xytext=(0,10), ha='center', color='red')
plt.annotate(f"n = {n_intersect_l2}", (n_intersect_l2, T_l2),
             textcoords="offset points", xytext=(0,10), ha='center', color='green')
plt.annotate(f"n = {n_intersect_l3}", (n_intersect_l3, T_l3),
             textcoords="offset points", xytext=(0,10), ha='center', color='orange')

plt.xlabel("n")
plt.ylabel("T(n) (octets)")
plt.title("Taille des données en fonction de n et limites de cache\n"
          "CPU: Intel(R) Core(TM) i3-4160T @ 3.10GHz\n"
          "L1: 64 KiB, L2: 512 KiB, L3: 3 MiB")
plt.legend(loc='best')
plt.grid(True)

# Enregistrement du graphique en PNG
plt.savefig("cpu_cache_summary.png", format="png", dpi=300)
plt.show()
