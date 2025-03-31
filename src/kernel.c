
#ifdef OPT1 //inverser les indices des boucles pour s'accorder à la lecture ligne par ligne (row-major order)

#include <math.h> // sqrt

float kernel (unsigned n, const double a[n][n], const float b[n]) {
    unsigned i, j;
    float s = 0.0;

    for (i=0; i<n; i++)
        for (j=0; j<n; j++)
            s += a[i][j] / sqrt(b[i]);

    return s;
}

#elif defined OPT2 //pré-calcul de l'inverse de la racine carrée des valeurs de b afin de réduire le nombre de calculs

#include <math.h> // sqrt



float kernel(unsigned n, const double a[n][n], const float b[n]) {
    unsigned i, j;
    float s = 0.0;

    // Pré-calcul de 1 / sqrt(b[i]) pour éviter les divisions
    float inv_sqrt_b[n];
    for (i = 0; i < n; i++) {
        inv_sqrt_b[i] = 1.0f / sqrtf(b[i]); //calcul en float
    }

    // Calcul de la somme avec unrolling pour réduire les accès mémoire
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            s += (float)a[i][j] * inv_sqrt_b[i]; //je crois qu'il y a deux conversions inutiles a cause du a en double => cast en float 
        }
    }
    return s;
}

#else

/* original */

#include <math.h> // sqrt

float kernel (unsigned n, const double a[n][n], const float b[n]) {
    unsigned i, j;
    float s = 0.0;

    for (j=0; j<n; j++)
        for (i=0; i<n; i++)
            s += a[i][j] / sqrt(b[i]);

    return s;
}

#endif
