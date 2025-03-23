
#ifdef OPT1

#include <math.h> // sqrt

float kernel(unsigned n, const double a[n][n], const float b[n]) {
    unsigned i, j;
    float s = 0.0;

    // Pré-calcul des sqrt(b[i]) pour éviter les recalculs
    float sqrt_b[n];
    for (i = 0; i < n; i++) {
        sqrt_b[i] = sqrt(b[i]); // Risque de NaN si b[i] < 0
    }

    // Calcul de la somme
    for (j = 0; j < n; j++) {
        for (i = 0; i < n; i++) {
            s += a[i][j] / sqrt_b[i]; // Utilisation du pré-calcul
        }
    }

    return s;
}

#elif defined OPT2

// TODO
#include <math.h> // sqrt

float kernel(unsigned n, const double a[restrict n][n], const float b[restrict n]) {
    unsigned i, j;
    float s = 0.0;

    // Pré-calcul de 1 / sqrt(b[i]) pour éviter les divisions
    float inv_sqrt_b[n];
    for (i = 0; i < n; i++) {
        inv_sqrt_b[i] = 1.0f / sqrtf(b[i]); // Évite division dans la boucle principale
    }

    // Calcul de la somme avec unrolling pour réduire les accès mémoire
    for (j = 0; j < n; j++) {
        for (i = 0; i + 3 < n; i += 4) { // Déroulage de boucle par 4
            s += a[i][j] * inv_sqrt_b[i] +
                 a[i + 1][j] * inv_sqrt_b[i + 1] +
                 a[i + 2][j] * inv_sqrt_b[i + 2] +
                 a[i + 3][j] * inv_sqrt_b[i + 3];
        }
        // Traitement des éléments restants
        for (; i < n; i++) {
            s += a[i][j] * inv_sqrt_b[i];
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
