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
 - repw=5
 - 2700 RTDSC -> On prendra alors repm=4

