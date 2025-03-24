# Part 1
## Infos
Maqao 2.21.1
GCC 13.3.0
Caches (sum of all):      
  L1d:                    64 KiB (2 instances)
  L1i:                    64 KiB (2 instances)
  L2:                     512 KiB (2 instances)
  L3:                     3 MiB (1 instance)

Calcul taille data: T(n) = n² × 8  +  n × 4  octets.

Grace à calibrate, size=10, repw=[1, 100]:
`./calibrate 10 100 > calibrate-gcc-10-100.txt`
 - repw>=3
 - 2700 RTDSC -> On prendra alors repm>=5


## Mesures
### A faire
./measure 64 100 30    # Données tenant dans L1
./measure 128 100 30   # Données dans L2
./measure 256 100 30   # Données dans L2, proche de la limite
./measure 512 100 30   # Données dans L3
./measure 1024 100 30  # Données en RAM

### Pour lancer MAQAO avec pin
./maqao oneview -R1 -- taskset -c 1 ./bin/measure 300 100 30



