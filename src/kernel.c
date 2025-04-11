
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

#elif OPT2 //pré-calcul de l'inverse des valeurs de b afin de réduire le nombre de calculs

#include <math.h> // sqrt



float kernel(unsigned n, const double a[n][n], const float b[n]) {
    unsigned i, j;
    float s = 0.0;

    // Pré-calcul de 1 / b[i] pour éviter les divisions
    float inv_b[n];
    for (i = 0; i < n; i++) {
        inv_b[i] = 1.0f / b[i]; //calcul en float
    }

    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            s += (float)a[i][j] * sqrtf(inv_b[i]); //je crois qu'il y a deux conversions inutiles a cause du a en double => cast en float 
        }
    }
    return s;
}

#elif OPT3 //option où on pré-calcule l'inverse de la racine des valeurs de b[] (gain énorme car le sqrt prend bcp de temps)

#include <math.h>

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

#elif OPT4 //Loop invariant code motion

#include <math.h>

float kernel(unsigned n, const double a[n][n], const float b[n]) {
    unsigned i, j;
    float s = 0.0, K;

    // Pré-calcul de 1 / sqrt(b[i]) pour éviter les divisions
    float inv_sqrt_b[n];
    for (i = 0; i < n; i++) {
        inv_sqrt_b[i] = 1.0f / sqrtf(b[i]); //calcul en float
    }

    // Calcul de la somme avec unrolling pour réduire les accès mémoire
    for (i = 0; i < n; i++) {
        K = inv_sqrt_b[i];
        for (j = 0; j < n; j++) {
            s += (float)a[i][j] * K;
        }
    }
    return s;
}

#elif OPT5 //Unrolling (faire plusieurs accès mémoires en une seule itération de boucle pour réduire le nombre de jumps etc)
// => peut-etre a enlever si on veut de la vectorisation auto

#include <math.h>

float kernel(unsigned n, const double a[n][n], const float b[n]) {
    unsigned i, j;
    float s = 0.0, K;

    // Pré-calcul de 1 / sqrt(b[i]) pour éviter les divisions
    float inv_sqrt_b[n];
    for (i = 0; i < n; i++) {
        inv_sqrt_b[i] = 1.0f / sqrtf(b[i]); //calcul en float
    }

    // Calcul de la somme avec unrolling pour réduire les accès mémoire
    for (int i = 0; i < n; i++) {
        K = inv_sqrt_b[i];
        for (int j = 0; j + 3 < n; j += 4) { // Déroulage de boucle par 4 colonnes
            s += a[i][j] * K
               + a[i][j + 1] * K
               + a[i][j + 2] * K
               + a[i][j + 3] * K;
        }
        // Traitement des colonnes restantes
        for (int j_remain = (n / 4) * 4; j_remain < n; j_remain++) {
            s += a[i][j_remain] * K;
        }
    }    
    return s;
}

#elif OPT6 //Loop tiling, on va parcourir la matrice en tirant profit de la localité spatiale (accès à des données contigues bloc par bloc)

#include <assert.h>
#include <math.h>

#define TILE_SIZE 128

float kernel(unsigned n, const double a[n][n], const float b[n]) {

    float s = 0.0f, K;
    float inv_sqrt_b[n];

    // Calcul de l'inverse de la racine carrée pour chaque élément du vecteur b
    for (unsigned i = 0; i < n; i++) {
        inv_sqrt_b[i] = 1.0f / sqrtf(b[i]);
    }

    // Boucle de tiling sur la matrice
    for (unsigned ii = 0; ii < n; ii += TILE_SIZE) {
        // Calcul de la limite du bloc, pour gérer les blocs partiels
        unsigned i_max = (ii + TILE_SIZE < n) ? (ii + TILE_SIZE) : n;
        for (unsigned jj = 0; jj < n; jj += TILE_SIZE) {
            unsigned j_max = (jj + TILE_SIZE < n) ? (jj + TILE_SIZE) : n;
            for (unsigned i = ii; i < i_max; i++) {
                float K = inv_sqrt_b[i];
                for (unsigned j = jj; j < j_max; j++) {
                    s += a[i][j] * K;
                }
            }
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
