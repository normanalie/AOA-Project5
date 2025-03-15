
#ifdef OPT1

#include <math.h> // sqrt

float kernel (unsigned n, const double a[n][n], const float b[n]) {
    unsigned i, j;
    float c[n];
    float s = 0.0;

    for(j=0; j<n; j++){
        c[j] = sqrt(b[j]);
    }

    for (j=0; j<n; j++)
        for (i=0; i<n; i++)
            s += a[i][j] / c[i];

    return s;
}

#elif defined OPT2

// TODO

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
