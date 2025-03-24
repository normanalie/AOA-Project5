# Part 1
## Infos
Maqao 2.21.1

Caches (sum of all):                        
  L1d:                                      192 KiB (6 instances)
  L1i:                                      192 KiB (6 instances)
  L2:                                       3 MiB (6 instances)
  L3:                                       16 MiB (1 instance)

T(n)=n^2×8+n×4
où :

    n² * 8 correspond à la matrice de type double (8 octets par élément),
    n * 4 correspond au vecteur de type float (4 octets par élément),

Mon cache L3 a une taille de 16 Mio, soit 16 × 1024 = 16 384 Kio.
On veut trouver n tel que :
    T(n)≥16384 Kio

La valeur obtenue est n ≈ 1448.

Donc, pour dépasser la taille du cache L3 (16 Mio), il faut prendre n ≈ 1450 voire 1500 (pour faire 100 tours de boucle) pour être sûr.

Pour compiler la version originale : make OPT=NOOPT
Pour compiler la première version optimisée : make OPT=OPT1
Pour compiler la seconde version optimisée : make OPT=OPT2

Pour vérifier la sortie avec une taille 300 et l'enregistrer dans out.txt :
 ./check 300 out.txt

Pour calibrer avec une taille 300 le bon nombre de répétitions (max 100) de warmup à utiliser:
 ./calibrate 300 100 (à modifier)

Pour mesurer avec une taille 300, 100 répétitions de warmup (lors de la première méta) et 30 répétitions de mesure :
 ./measure 300 100 30 (à modif)

Pour exécuter avec MAQAO :
maqao oneview -R1 -- ./measure 300 100 30(à modif)