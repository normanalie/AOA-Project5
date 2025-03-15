#include <stdio.h>
#include <stdlib.h> // atoi, qsort
#include <stdint.h>

extern uint64_t rdtsc ();

// TODO: adjust for each kernel
extern float kernel(unsigned n, const double a[n][n], const float b[n]);

// TODO: adjust for each kernel
static void init_array (int n, double a[n][n]) {
   int i, j;

   for (i=0; i<n; i++)
      for (j=0; j<n; j++)
         a[i][j] = (double) rand() / RAND_MAX;
}

static void init_array_float (int n, float *a) {  // Modified for unidimensionnal array
   int i;
   for (i = 0; i < n; i++)
       a[i] = (float) rand() / RAND_MAX;
}

// TODO: adjust for each kernel
static void print_array (int n, double a[n][n], const char *output_file_name) {
   int i, j;

   FILE *fp = fopen (output_file_name, "w");
   if (fp == NULL) {
      fprintf (stderr, "Cannot write to %s\n", output_file_name);
      return;
   }

   for (i=0; i<n; i++)
      for (j=0; j<n; j++)
         fprintf (fp, "%f\n", a[i][j]);

   fclose (fp);
}


static void print_float(float result, const char *output_file_name) {
   FILE *fp = fopen(output_file_name, "w");
   if (fp == NULL) {
       fprintf(stderr, "Erreur : impossible d'ouvrir %s pour écriture\n", output_file_name);
       return;
   }
   fprintf(fp, "%f\n", result);
   fclose(fp);
}

int main (int argc, char *argv[]) {
   /* check command line arguments */
   if (argc != 3) {
      fprintf (stderr, "Usage: %s <size> <output file name>\n", argv[0]);
      return 1;
   }

   /* get command line arguments */
   const unsigned size = atoi (argv[1]); /* problem size */
   const char *output_file_name = argv[2];

   /* allocate arrays. TODO: adjust for each kernel */
   double (*a)[size] = malloc (size * size * sizeof a[0][0]);
   float (*b) = malloc (size * sizeof(float));
   /* init arrays */
   srand(0);
   init_array (size, a);
   init_array_float (size, b);

   /* print output */
   float result = kernel (size, a, b);
   print_float(result, output_file_name);

   /* free arrays. TODO: adjust for each kernel */
   free (a);
   free (b);

   return EXIT_SUCCESS;
}
