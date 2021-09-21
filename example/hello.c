#include <stdio.h>
#include "mpi.h"

int main (int argc, char** argv) {
  int myid;
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &myid);
  printf("Hello from %d.\n", myid);
  MPI_Finalize();
  return 0;
}
